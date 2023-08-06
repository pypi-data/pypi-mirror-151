from gwlab_viterbi_python import GWLabViterbi, ViterbiJob, FileReference, FileReferenceList, JobStatus, TimeRange
from gwlab_viterbi_python.utils import convert_dict_keys
from gwlab_viterbi_python.utils.file_download import _get_file_map_fn, _save_file_map_fn
import pytest
from tempfile import TemporaryFile


@pytest.fixture
def setup_gwl_request(mocker):
    def mock_init(self, token, endpoint):
        pass

    mock_request = mocker.Mock()
    mocker.patch('gwlab_viterbi_python.gwlab_viterbi.GWDC.__init__', mock_init)
    mocker.patch('gwlab_viterbi_python.gwlab_viterbi.GWDC.request', mock_request)

    return GWLabViterbi(token='my_token'), mock_request


@pytest.fixture
def setup_mock_download_fns(mocker):
    def get_mock_ids(job_id, tokens):
        return [f'{job_id}{i}' for i, _ in enumerate(tokens)]

    mock_ids = mocker.Mock(side_effect=get_mock_ids)
    return (
        mocker.patch('gwlab_viterbi_python.gwlab_viterbi.GWLabViterbi._get_download_ids_from_tokens', mock_ids),
        mocker.patch('gwlab_viterbi_python.gwlab_viterbi._download_files')
    )


@pytest.fixture
def job_data():
    return [
        {
            "id": 1,
            "name": "test_name_1",
            "description": "test description 1",
            "user": "Test User1",
            "jobStatus": {
                "name": "Completed",
                "date": "2021-01-01"
            }
        },
        {
            "id": 2,
            "name": "test_name_2",
            "description": "test description 2",
            "user": "Test User2",
            "jobStatus": {
                "name": "Completed",
                "date": "2021-02-02"
            }
        },
        {
            "id": 3,
            "name": "test_name_3",
            "description": "test description 3",
            "user": "Test User3",
            "jobStatus": {
                "name": "Error",
                "date": "2021-03-03"
            }
        }
    ]


def multi_job_request(query_name, return_job_data):
    return {
        query_name: {
            "edges": [{"node": job_datum} for job_datum in return_job_data],
        }
    }


@pytest.fixture
def job_file_data():
    return [
        {
            "path": "path/to/test.png",
            "fileSize": "1",
            "downloadToken": "test_token_1",
            "isDir": False
        },
        {
            "path": "path/to/test.json",
            "fileSize": "10",
            "downloadToken": "test_token_2",
            "isDir": False
        },
        {
            "path": "path/to/test",
            "fileSize": "100",
            "downloadToken": "test_token_3",
            "isDir": True
        }
    ]


@pytest.fixture
def test_files():
    return FileReferenceList([
        FileReference(
            path='test/path_1.png',
            file_size=1,
            download_token='test_token_1',
            job_id='id1',
        ),
        FileReference(
            path='test/path_2.png',
            file_size=1,
            download_token='test_token_2',
            job_id='id1',
        ),
        FileReference(
            path='test/path_3.png',
            file_size=1,
            download_token='test_token_3',
            job_id='id2',
        ),
        FileReference(
            path='test/path_4.png',
            file_size=1,
            download_token='test_token_4',
            job_id='id2',
        ),
        FileReference(
            path='test/path_5.png',
            file_size=1,
            download_token='test_token_5',
            job_id='id3',
        ),
        FileReference(
            path='test/path_6.png',
            file_size=1,
            download_token='test_token_6',
            job_id='id3',
        ),
    ])


def test_get_job_model_from_query(setup_gwl_request, job_data):
    gwl, _ = setup_gwl_request
    single_job_data = job_data[0]

    assert gwl._get_job_model_from_query(None) is None

    expected = ViterbiJob(
        client=gwl,
        job_id=single_job_data["id"],
        name=single_job_data["name"],
        description=single_job_data["description"],
        user=single_job_data["user"],
        job_status=single_job_data["jobStatus"],
    )
    assert gwl._get_job_model_from_query(single_job_data) == expected


def test_get_job_by_id(setup_gwl_request, job_data):
    gwl, mock_request = setup_gwl_request
    mock_request.return_value = {"viterbiJob": None}
    assert gwl.get_job_by_id('job_id') is None

    single_job_data = job_data[0]
    mock_request.return_value = {"viterbiJob": single_job_data}

    job = gwl.get_job_by_id('job_id')

    mock_request.assert_called_with(
        query="""
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
        """,
        variables={
            "id": "job_id"
        }
    )

    assert job.job_id == single_job_data["id"]
    assert job.name == single_job_data["name"]
    assert job.description == single_job_data["description"]
    assert job.status == JobStatus(
        status=single_job_data["jobStatus"]["name"],
        date=single_job_data["jobStatus"]["date"]
    )
    assert job.user == single_job_data["user"]


def test_get_user_jobs(setup_gwl_request, job_data):
    gwl, mock_request = setup_gwl_request
    mock_request.return_value = multi_job_request('viterbiJobs', [])
    assert gwl.get_user_jobs() == []

    mock_request.return_value = multi_job_request('viterbiJobs', job_data)
    jobs = gwl.get_user_jobs(number=100)
    mock_request.assert_called_with(
        query="""
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
        """,
        variables={
            "first": 100
        }
    )

    assert jobs[0].job_id == job_data[0]["id"]
    assert jobs[0].name == job_data[0]["name"]
    assert jobs[0].description == job_data[0]["description"]
    assert jobs[0].status == JobStatus(
        status=job_data[0]["jobStatus"]["name"],
        date=job_data[0]["jobStatus"]["date"]
    )
    assert jobs[0].user == job_data[0]["user"]

    assert jobs[1].job_id == job_data[1]["id"]
    assert jobs[1].name == job_data[1]["name"]
    assert jobs[1].description == job_data[1]["description"]
    assert jobs[1].status == JobStatus(
        status=job_data[1]["jobStatus"]["name"],
        date=job_data[1]["jobStatus"]["date"]
    )
    assert jobs[1].user == job_data[1]["user"]

    assert jobs[2].job_id == job_data[2]["id"]
    assert jobs[2].name == job_data[2]["name"]
    assert jobs[2].description == job_data[2]["description"]
    assert jobs[2].status == JobStatus(
        status=job_data[2]["jobStatus"]["name"],
        date=job_data[2]["jobStatus"]["date"]
    )
    assert jobs[2].user == job_data[2]["user"]


def test_get_public_job_list(setup_gwl_request, job_data):
    gwl, mock_request = setup_gwl_request
    mock_request.return_value = multi_job_request('publicViterbiJobs', [])
    assert gwl.get_public_job_list() == []

    mock_request.return_value = multi_job_request('publicViterbiJobs', job_data)
    jobs = gwl.get_public_job_list(search="Test", time_range=TimeRange.DAY, number=100)

    mock_request.assert_called_with(
        query="""
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
        """,
        variables={
            "search": "Test",
            "timeRange": TimeRange.DAY.value,
            "first": 100
        }
    )

    assert jobs[0].job_id == job_data[0]["id"]
    assert jobs[0].name == job_data[0]["name"]
    assert jobs[0].description == job_data[0]["description"]
    assert jobs[0].status == JobStatus(
        status=job_data[0]["jobStatus"]["name"],
        date=job_data[0]["jobStatus"]["date"]
    )
    assert jobs[0].user == job_data[0]["user"]

    assert jobs[1].job_id == job_data[1]["id"]
    assert jobs[1].name == job_data[1]["name"]
    assert jobs[1].description == job_data[1]["description"]
    assert jobs[1].status == JobStatus(
        status=job_data[1]["jobStatus"]["name"],
        date=job_data[1]["jobStatus"]["date"]
    )
    assert jobs[1].user == job_data[1]["user"]

    assert jobs[2].job_id == job_data[2]["id"]
    assert jobs[2].name == job_data[2]["name"]
    assert jobs[2].description == job_data[2]["description"]
    assert jobs[2].status == JobStatus(
        status=job_data[2]["jobStatus"]["name"],
        date=job_data[2]["jobStatus"]["date"]
    )
    assert jobs[2].user == job_data[2]["user"]


def test_gwlab_files_by_job_id(setup_gwl_request, job_file_data):
    gwl, mock_request = setup_gwl_request
    mock_request.return_value = {
        "viterbiResultFiles": {
            "files": job_file_data,
        }
    }

    file_list = gwl._get_files_by_job_id('arbitrary_job_id')

    mock_request.assert_called_with(
        query="""
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
        """,
        variables={
            "jobId": "arbitrary_job_id"
        }
    )

    for i, ref in enumerate(file_list):
        job_file_data[i].pop('isDir')
        assert ref == FileReference(
            **convert_dict_keys(job_file_data[i]),
            job_id='arbitrary_job_id',
        )


def test_gwlab_get_files_by_reference(setup_mock_download_fns, setup_gwl_request, mocker, test_files):
    mock_get_ids, mock_download_files = setup_mock_download_fns
    gwl, _ = setup_gwl_request

    mock_download_files.return_value = [(f.path, TemporaryFile()) for f in test_files]

    files = gwl.get_files_by_reference(test_files)

    mock_calls = [
        mocker.call(job_id, job_files.get_tokens())
        for job_id, job_files in test_files._batch_by_job_id().items()
    ]

    mock_get_ids.assert_has_calls(mock_calls)

    assert [f[0] for f in files] == test_files.get_paths()
    mock_download_files.assert_called_once_with(
        _get_file_map_fn,
        ['id10', 'id11', 'id20', 'id21', 'id30', 'id31'],
        test_files.get_paths(),
        test_files.get_total_bytes()
    )


def test_gwlab_save_batched_files(setup_mock_download_fns, setup_gwl_request, mocker, test_files):
    mock_get_ids, mock_download_files = setup_mock_download_fns
    gwl, _ = setup_gwl_request

    gwl.save_files_by_reference(test_files, 'test_dir', preserve_directory_structure=True)

    mock_calls = [
        mocker.call(job_id, job_files.get_tokens())
        for job_id, job_files in test_files._batch_by_job_id().items()
    ]

    mock_get_ids.assert_has_calls(mock_calls)

    mock_download_files.assert_called_once_with(
        _save_file_map_fn,
        ['id10', 'id11', 'id20', 'id21', 'id30', 'id31'],
        test_files.get_output_paths('test_dir', preserve_directory_structure=True),
        test_files.get_total_bytes()
    )
