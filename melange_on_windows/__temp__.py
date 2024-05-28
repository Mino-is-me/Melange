import os, stat, subprocess, shutil

def remove_readonly(func, path, _):
    """Change the mode of path to writeable and retry the operation."""
    os.chmod(path, stat.S_IWRITE)
    func(path)