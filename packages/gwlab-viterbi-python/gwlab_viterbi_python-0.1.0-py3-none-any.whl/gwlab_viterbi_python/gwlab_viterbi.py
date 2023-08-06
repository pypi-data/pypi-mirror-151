import logging
import itertools

from gwdc_python import GWDC

from .viterbi_job import ViterbiJob
from .file_reference import FileReference, FileReferenceList
from .helpers import TimeRange
from .utils import convert_dict_keys
from .utils.file_download import _download_files, _save_file_map_fn, _get_file_map_fn
from .settings import GWLAB_VITERBI_ENDPOINT

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)


class GWLabViterbi:
    def __init__(self, token, endpoint=GWLAB_VITERBI_ENDPOINT):
        self.client = GWDC(token=token, endpoint=endpoint)
        self.request = self.client.request

    def _get_job_model_from_query(self, query_data):
        if not query_data:
            return None

        return ViterbiJob(
            client=self,
            **convert_dict_keys(
                query_data,
                {'id': 'job_id'}
            )
        )

    def get_public_job_list(self, search="", time_range=TimeRange.ANY, number=100):
        """Obtains a list of public Viterbi jobs, filtering based on the search terms
        and the time range within which the job was created.

        Parameters
        ----------
        search : str, optional
            Search terms by which to filter public job list, by default ""
        time_range : .TimeRange or str, optional
            Time range by which to filter job list, by default TimeRange.ANY
        number : int, optional
            Number of job results to return in one request, by default 100

        Returns
        -------
        list
            List of ViterbiJob instances for the jobs corresponding to the search terms and in the specified time range
        """
        query = """
            query ($search: String, $timeRange: String, $first: Int){
                publicViterbiJobs (search: $search, timeRange: $timeRange, first: $first) {
                    edges {
                        node {
                            id
                            user
                            name
                            description
                            jobStatus {
                                name
                                date
                            }
                        }
                    }
                }
            }
        """

        variables = {
            "search": search,
            "timeRange": time_range.value if isinstance(time_range, TimeRange) else time_range,
            "first": number
        }

        data = self.request(query=query, variables=variables)

        if not data['publicViterbiJobs']['edges']:
            logger.info('Job search returned no results.')
            return []

        return [self._get_job_model_from_query(job['node']) for job in data['publicViterbiJobs']['edges']]

    def get_job_by_id(self, job_id):
        """Get a Viterbi job instance corresponding to a specific job ID

        Parameters
        ----------
        job_id : str
            ID of job to obtain

        Returns
        -------
        ViterbiJob
            ViterbiJob instance corresponding to the input ID
        """
        query = """
            query ($id: ID!){
                viterbiJob (id: $id) {
                    id
                    name
                    user
                    description
                    jobStatus {
                        name
                        date
                    }
                }
            }
        """

        variables = {
            "id": job_id
        }

        data = self.request(query=query, variables=variables)

        if not data['viterbiJob']:
            logger.info('No job matching input ID was returned.')
            return None

        return self._get_job_model_from_query(data['viterbiJob'])

    def get_user_jobs(self, number=100):
        """Obtains a list of Viterbi jobs created by the user, filtering based on the search terms
        and the time range within which the job was created.

        Parameters
        ----------
        number : int, optional
            Number of job results to return in one request, by default 100

        Returns
        -------
        list
            List of ViterbiJob instances for the jobs corresponding to the search terms and in the specified time range
        """
        query = """
            query ($first: Int){
                viterbiJobs (first: $first){
                    edges {
                        node {
                            id
                            name
                            user
                            description
                            jobStatus {
                                name
                                date
                            }
                        }
                    }
                }
            }
        """

        variables = {
            "first": number
        }

        data = self.request(query=query, variables=variables)

        return [self._get_job_model_from_query(job['node']) for job in data['viterbiJobs']['edges']]

    def _get_files_by_job_id(self, job_id):
        query = """
            query ($jobId: ID!) {
                viterbiResultFiles (jobId: $jobId) {
                    files {
                        path
                        isDir
                        fileSize
                        downloadToken
                    }
                }
            }
        """

        variables = {
            "jobId": job_id
        }

        data = convert_dict_keys(self.request(query=query, variables=variables))

        file_list = FileReferenceList()
        for file_data in data['viterbi_result_files']['files']:
            if file_data['is_dir']:
                continue
            file_data.pop('is_dir')
            file_list.append(
                FileReference(
                    **file_data,
                    job_id=job_id,
                )
            )

        return file_list

    def get_files_by_reference(self, file_references):
        """Obtains file data when provided a FileReferenceList

        Parameters
        ----------
        file_references : FileReferenceList
            Contains the :class:`FileReference` objects for which to download the contents

        Returns
        -------
        list
            List of tuples containing the file path and file contents as a byte string
        """
        batched = file_references._batch_by_job_id()

        file_ids = [
            self._get_download_ids_from_tokens(job_id, job_files.get_tokens())
            for job_id, job_files in batched.items()
        ]

        file_ids = list(itertools.chain.from_iterable(file_ids))
        batched_files = FileReferenceList(itertools.chain.from_iterable(batched.values()))

        file_paths = batched_files.get_paths()
        total_size = batched_files.get_total_bytes()

        files = _download_files(_get_file_map_fn, file_ids, file_paths, total_size)

        logger.info(f'All {len(file_ids)} files downloaded!')

        return files

    def save_files_by_reference(self, file_references, root_path, preserve_directory_structure=True):
        """Save files when provided a FileReferenceList and a root path

        Parameters
        ----------
        file_references : FileReferenceList
            Contains the :class:`FileReference` objects for which to save the associated files
        root_path : str or ~pathlib.Path
            Directory into which to save the files
        preserve_directory_structure : bool, optional
            Remove any directory structure for the downloaded files, by default True
        """
        batched = file_references._batch_by_job_id()

        file_ids = [
            self._get_download_ids_from_tokens(job_id, job_files.get_tokens())
            for job_id, job_files in batched.items()
        ]

        file_ids = list(itertools.chain.from_iterable(file_ids))
        batched_files = FileReferenceList(itertools.chain.from_iterable(batched.values()))

        file_paths = batched_files.get_output_paths(root_path, preserve_directory_structure)
        total_size = batched_files.get_total_bytes()

        _download_files(_save_file_map_fn, file_ids, file_paths, total_size)

        logger.info(f'All {len(file_ids)} files saved!')

    def _get_download_id_from_token(self, job_id, file_token):
        """Get a single file download id for a file download token

        Parameters
        ----------
        job_id : str
            Job id which owns the file token

        file_token : str
            Download token for the desired file

        Returns
        -------
        str
            Download id for the desired file
        """
        return self._get_download_ids_from_tokens(job_id, [file_token])[0]

    def _get_download_ids_from_tokens(self, job_id, file_tokens):
        """Get many file download ids for a list of file download tokens

        Parameters
        ----------
        job_id : str
            Job id which owns the file token

        file_tokens : list
            Download tokens for the desired files

        Returns
        -------
        list
            List of download ids for the desired files
        """
        query = """
            mutation ResultFileMutation($input: GenerateFileDownloadIdsInput!) {
                generateFileDownloadIds(input: $input) {
                    result
                }
            }
        """

        variables = {
            "input": {
                "jobId": job_id,
                "downloadTokens": file_tokens
            }
        }

        data = self.request(query=query, variables=variables)

        return data['generateFileDownloadIds']['result']
