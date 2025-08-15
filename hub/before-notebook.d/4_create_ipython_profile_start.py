#!/opt/conda/bin/python
import os
import shutil
from IPython.paths import locate_profile
from IPython.core.profiledir import ProfileDir, ProfileDirError

# This before-notebook script copies scripts that should be used be run
# by default when an IPython session is started.
# For instance it is used to copy the script that defines the default PATH
# environment that the session should use.

# It requires that the IPYTHON_STARTUP_DIR env is defined as the location
# where the startup scripts that are to be copied into the profile directory
# are located.

# Ensure .ipython dir is present
if not os.environ.get("IPYTHONDIR", None):
    ipython_dir = os.path.join(
        os.environ.get("HOME", os.path.join("home", "jovyan")), ".ipython"
    )
else:
    ipython_dir = os.environ.get("IPYTHONDIR")

if not os.path.exists(ipython_dir):
    print("Creating ipython dir: {}".format(ipython_dir))
    try:
        os.makedirs(ipython_dir)
    except IOError as err:
        print("Failed to create ipython dir: {}, err: {}".format(ipython_dir, err))
        exit(1)
print("ipython dir: {} exists".format(ipython_dir))

# Create profile directory
try:
    # Creates a profile_default folder inside the ipython directory.
    p = ProfileDir.create_profile_dir_by_name(ipython_dir)
except ProfileDirError:
    print("Failed to create profile dir: {}".format(ipython_dir))
    exit(2)
else:
    print("Created profile dir: %r" % p.location)

# Ensure the profile can be found
profile_directory = None
try:
    profile_directory = locate_profile()
except IOError as err:
    print("Failed to find the IPython profile directory, err: {}".format(err))
    exit(3)

if not profile_directory:
    print("Failed to define profile_directory for IPython")
    exit(3)

startup_path = None
try:
    startup_path = os.path.join(profile_directory, "startup")
except IOError as err:
    print("Failed to locate profile directory for IPython, err: {}".format(err))
    exit(3)

if not startup_path:
    print("Failed to define start_up for IPython")
    exit(3)

if not os.path.exists(startup_path):
    try:
        os.makedirs(startup_path)
    except IOError as err:
        print(
            "Failed to create missing profile startup directory: {} "
            "for IPython, err: {}".format(startup_path, err)
        )
    exit(4)

# Ensure the correct permissions for the profile directory
user_uid = os.environ.get("NB_UID")
if not user_uid:
    print("The environment variable NB_UID is not set")
    exit(4)
user_uid = int(user_uid)

user_gid = os.environ.get("NB_GID")
if not user_gid:
    print("The environment variable NB_GID is not set")
    exit(4)
user_gid = int(user_gid)

try:
    os.chown(profile_directory, user_uid, user_gid)
except Exception as err:
    print(
        "Failed to set the ownership permissions for the directory: {}, err: {}".format(
            profile_directory, err
        )
    )
    exit(4)

for root, dirs, files in os.walk(profile_directory):
    for dir in dirs:
        os.chown(os.path.join(root, dir), user_uid, user_gid)
    for file in files:
        os.chown(os.path.join(root, file), user_uid, user_gid)

# Copy the startup files to the .ipython/profile_default/startup directory
if not os.environ.get("IPYTHON_STARTUP_DIR", None):
    print("IPYTHON_STARTUP_DIR not set, don't know which files to copy")
    exit(5)

ipython_startup_path = os.environ["IPYTHON_STARTUP_DIR"]
if not os.path.exists(ipython_startup_path):
    print(
        "The specified IPYTHON_STARTUP_DIR path: {}, does not exist".format(
            ipython_startup_path
        )
    )
    exit(6)

files = os.listdir(ipython_startup_path)
for f in files:
    f_path = os.path.join(ipython_startup_path, f)
    print("Copying: {} to {}".format(f_path, os.path.join(startup_path, f)))
    try:
        shutil.copy(f_path, startup_path)
    except Exception as err:
        print("Failed to copy: {} to {}, err {}".format(f_path, startup_path, err))
        exit(7)
