#!/opt/conda/bin/python
import os


def exists(path):
    return os.path.exists(expanduser(path))


def expanduser(path):
    return os.path.expanduser(path)


def makedirs(path):
    try:
        os.makedirs(expanduser(path))
        return True, "Created: {}".format(path)
    except IOError as err:
        return False, "Failed to create the directory path: {} - {}".format(path, err)


def write(path, content, mode="w", mkdirs=False):
    dir_path = os.path.dirname(path)
    if not exists(dir_path) and mkdirs:
        if not makedirs(dir_path):
            return False
    try:
        with open(path, mode) as fh:
            fh.write(content)
        return True
    except IOError as err:
        print("Failed to save file: {} - {}".format(path, err))
    return False


if __name__ == "__main__":
    default_profile_file_path = expanduser(os.path.join("~", ".profile"))
    welcome_msg_append = """
    echo '\nThe available environments in this Notebook are:\n'
    conda env list
    """
    welcome_wrote = write(default_profile_file_path, welcome_msg_append, mode="a")
    if not welcome_wrote:
        print(
            "Failed to append the welcome message: {}".format(default_profile_file_path)
        )
        exit(-2)
    print(
        "Wrote the welcome message to the bashrc file: {}".format(
            default_profile_file_path
        )
    )
