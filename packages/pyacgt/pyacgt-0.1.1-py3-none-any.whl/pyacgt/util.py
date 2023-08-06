import shutil
FilePath = str
def cmd_exists(cmd:FilePath)->bool:
    """
    Checks whether or not a desired command exists.

    Parameters
    ----------
    cmd : FilePath
        a desired command

    Return
    ------
    bool
        whether or not the desired command exists.
    """    
    return shutil.which(cmd) is not None