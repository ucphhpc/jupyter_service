#!/opt/conda/bin/python
import os

# Set custom Rprofile configuration path

env_name = "R_LIBS_USER"
r_libs_user = os.environ.get(env_name, None)

if not r_libs_user:
    print("{} is not set, exiting without error".format(env_name))
    exit(0)

if not isinstance(r_libs_user, str):
    print("{} is not a string, exiting error".format(env_name))
    exit(1)

r_libs_paths = []
if ":" in r_libs_user:
    r_libs_paths = r_libs_user.split(":")
else:
    r_libs_paths.append(r_libs_user)

for r_libs_path in r_libs_paths:
    # Ensure that the libs path exist
    if not os.path.exists(r_libs_path):
        print("creating {} dir: {}".format(env_name, r_libs_path))
        try:
            os.makedirs(r_libs_path)
        except IOError as err:
            print(
                "Failed to create {} dir: {}, err: {}".format(
                    env_name, r_libs_path, err
                )
            )
            exit(2)

print("{} dir: {} exists".format(env_name, r_libs_paths))
