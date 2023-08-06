def _file_suffix(file_path, suffix):
    return file_path.suffix == f'.{suffix}'


def _file_dir(file_path, directory):
    return directory in file_path.parts[:-1]


def _file_name(file_path, name):
    return name in file_path.name


def _file_stem(file_path, stem):
    return stem in file_path.stem


def ini_file(file_path):
    """Checks to see if the given file path points to an ini file

    Parameters
    ----------
    file_path : ~pathlib.Path
        File path to check

    Returns
    -------
    bool
        True if path points to a ini file, False otherwise
    """
    return _file_suffix(file_path, 'ini')


def candidates_file(file_path):
    """Checks to see if the given file path points to the candidates file

    Parameters
    ----------
    file_path : ~pathlib.Path
        File path to check

    Returns
    -------
    bool
        True if path points to candidates file, False otherwise
    """
    return _file_name(file_path, 'results_a0_phase_loglikes_scores.dat')
