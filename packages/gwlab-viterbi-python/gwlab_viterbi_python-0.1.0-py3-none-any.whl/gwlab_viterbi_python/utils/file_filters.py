from . import identifiers
from functools import partial, reduce


def _filter_file_list(identifier, file_list):
    return [f for f in file_list if identifier(f.path)]


def _match_all(identifier_list, file_list):
    return reduce(lambda res, f: _filter_file_list(f, res), identifier_list, file_list)


def ini_filter(file_list):
    """Takes an input file list and returns a subset of that file list containing:

    - Any ini file

    Parameters
    ----------
    file_list : .FileReferenceList
        A list of FileReference objects which will be filtered

    Returns
    -------
    .FileReferenceList
        Subset of the input FileReferenceList containing only the paths that match the above config file criteria
    """
    return _filter_file_list(identifiers.ini_file, file_list)


def candidates_filter(file_list):
    """Takes an input file list and returns a subset of that file list containing:

    - Any file named 'results_a0_phase_loglikes_scores.dat'

    Parameters
    ----------
    file_list : .FileReferenceList
        A list of FileReference objects which will be filtered

    Returns
    -------
    .FileReferenceList
        Subset of the input FileReferenceList containing only the paths that match the above config file criteria
    """
    return _filter_file_list(identifiers.candidates_file, file_list)


def custom_path_filter(file_list, directory=None, name=None, extension=None):
    """Takes an input file list and returns a subset of that file list containing:

    - Any file that has any enclosing directory matching the `directory` argument
    - Any file that has any part of its filename matching the `name` argument
    - Any file that has an extension matching the `extension` argument

    Parameters
    ----------
    file_list : .FileReferenceList
        A list of FileReference objects which will be filtered
    directory : str, optional
        Directory to match, by default None
    name : str, optional
        Part of filename to match, by default None
    extension : str, optional
        File extension to match, by default None

    Returns
    -------
    .FileReferenceList
        Subset of the input FileReferenceList containing only the paths that match the above corner plot file criteria
    """
    identifier_list = []
    if directory:
        identifier_list.append(partial(identifiers._file_dir, directory=str(directory)))
    if name:
        identifier_list.append(partial(identifiers._file_stem, stem=str(name)))
    if extension:
        identifier_list.append(partial(identifiers._file_suffix, suffix=str(extension)))

    return _match_all(identifier_list, file_list)


def sort_file_list(file_list):
    """Sorts a file list based on the 'path' key of the dicts. Primarily used for equality checks.

    Parameters
    ----------
    file_list : .FileReferenceList
        A list of FileReference objects which will be filtered

    Returns
    -------
    .FileReferenceList
        A FileReferenceList containing the same members as the input,
        sorted by the path attribute of the FileReference objects
    """
    return sorted(file_list, key=lambda f: f.path)
