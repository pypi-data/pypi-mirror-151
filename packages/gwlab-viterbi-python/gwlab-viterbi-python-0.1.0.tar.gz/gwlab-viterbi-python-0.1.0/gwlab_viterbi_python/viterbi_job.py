import logging
from .utils import file_filters
from .helpers import JobStatus


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)


class ViterbiJob:
    """
    ViterbiJob class is useful for interacting with the Viterbi jobs returned from a call to the GWCloud API.
    It is primarily used to store job information and obtain files related to the job.

    Parameters
    ----------
    client : ~gwcloud_python.gwcloud.GWCloud
        A reference to the GWCloud object instance from which the ViterbiJob was created
    job_id : str
        The id of the Viterbi job, required to obtain the files associated with it
    name : str
        Job name
    description : str
        Job description
    user : str
        User that ran the job
    job_status : dict
        Status of job, should have 'name' and 'date' keys corresponding to the status code and when it was produced
    kwargs : dict, optional
        Extra arguments, stored in `other` attribute
    """

    DEFAULT_FILE_LIST_FILTERS = {
        'ini': file_filters.ini_filter,
        'candidates': file_filters.candidates_filter
    }

    def __init__(self, client, job_id, name, description, user, job_status, **kwargs):
        self.client = client
        self.job_id = job_id
        self.name = name
        self.description = description
        self.user = user
        self.status = JobStatus(status=job_status['name'], date=job_status['date'])
        self.other = kwargs

    def __repr__(self):
        return f"ViterbiJob(name={self.name}, job_id={self.job_id})"

    def __eq__(self, other):
        if isinstance(other, ViterbiJob):
            return (
                self.job_id == other.job_id and
                self.name == other.name and
                self.user == other.user
            )
        return False

    def get_full_file_list(self):
        """Get information for all files associated with this job

        Returns
        -------
        .FileReferenceList
            Contains FileReference instances for each of the files associated with this job
        """
        result = self.client._get_files_by_job_id(self.job_id)
        return result

    @classmethod
    def register_file_list_filter(cls, name, file_list_filter_fn):
        """Register a function used to filter the file list.
        This will create three methods on the class using this filter function:

        - get_{name}_file_list
        - get_{name}_files
        - save_{name}_files

        where {name} is the input name string.

        Parameters
        ----------
        name : str
            String used to name the added methods
        file_list_filter_fn : function
            A function that takes in the full file list and returns only the desired entries from the list
        """
        _register_file_list_filter(name, file_list_filter_fn)
        cls.DEFAULT_FILE_LIST_FILTERS[f'{name}'] = file_list_filter_fn


def _register_file_list_filter(name, file_list_filter_fn):
    spaced_name = name.replace('_', ' ')

    def _get_file_list_subset(self):
        full_list = self.get_full_file_list()
        return full_list.filter_list(file_list_filter_fn)

    file_list_fn_name = f'get_{name}_file_list'
    file_list_fn = _get_file_list_subset
    file_list_fn.__doc__ = f"""Get information for the {spaced_name} files associated with this job

        Returns
        -------
        .FileReferenceList
            Contains FileReference instances holding information on the {spaced_name} files
    """
    setattr(ViterbiJob, file_list_fn_name, file_list_fn)

    def _get_files(self):
        file_list = _get_file_list_subset(self)
        return self.client.get_files_by_reference(file_list)

    files_fn_name = f'get_{name}_files'
    files_fn = _get_files
    files_fn.__doc__ = f"""Download the content of all the {spaced_name} files.

        **WARNING**:
        *As the file contents are stored in memory, we suggest being cautious about the size of files being downloaded.
        If the files are large or very numerous, it is suggested to save the files and read them as needed instead.*

        Returns
        -------
        list
            List containing tuples of the file path and associated file contents
    """
    setattr(ViterbiJob, files_fn_name, files_fn)

    def _save_files(self, root_path, preserve_directory_structure=True):
        file_list = _get_file_list_subset(self)
        return self.client.save_files_by_reference(file_list, root_path, preserve_directory_structure)

    save_fn_name = f'save_{name}_files'
    save_fn = _save_files
    save_fn.__doc__ = f"""Download and save the {spaced_name} files.

        Parameters
        ----------
        root_path : str or ~pathlib.Path
            The base directory into which the files will be saved
        preserve_directory_structure : bool, optional
            Save the files in the same structure that they were downloaded in, by default True
    """
    setattr(ViterbiJob, save_fn_name, save_fn)


for name, file_filter in ViterbiJob.DEFAULT_FILE_LIST_FILTERS.items():
    _register_file_list_filter(name, file_filter)
