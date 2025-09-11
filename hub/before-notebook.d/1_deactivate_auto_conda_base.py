#!/usr/bin/env python3
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


def load_content(path):
    try:
        with open(path, "r") as fh:
            return fh.read()
    except IOError as err:
        print("Failed to read file: {} - {}".format(path, err))
    return False


if __name__ == "__main__":
    default_profile_file_path = expanduser(os.path.join("~", ".profile"))
    if not exists(default_profile_file_path):
        print(
            "Default profile file does not exist: {}".format(default_profile_file_path)
        )
        exit(0)

    # Append to the profile file that the default base conda environment should not be activated
    profile_file_content = load_content(default_profile_file_path)
    if not profile_file_content:
        exit(-1)

    deactivate_command = "conda config --set auto_activate_base false"
    if deactivate_command in profile_file_content:
        print(
            "Default conda base environment activation already present in profile file: {}".format(
                default_profile_file_path
            )
        )
        exit(0)

    wrote = write(default_profile_file_path, "\n{}\n".format(deactivate_command), "a")

    if not wrote:
        print(
            "Failed to write the conda deactivate command to the profile file: {}".format(
                default_profile_file_path
            )
        )
        exit(-1)

    print(
        "Added conda deactivate base to the profile file: {}".format(
            default_profile_file_path
        )
    )
    exit(0)
