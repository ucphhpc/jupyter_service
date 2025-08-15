import os

# Ensure that the IPython sessions have the correct search paths for commands
home = os.environ.get("HOME", None)
if not home:
    print("HOME env is required to run {}".format(__file__))
    exit(1)

if not os.path.exists(home):
    print("Directory specified by HOME env does not exist: {}".format(home))
    exit(2)

bin_dir = os.path.join(home, ".local/bin")
if not os.path.exists(bin_dir):
    print("local bin directory is not present, PATH is not altered")
    exit(3)

# Extract the current PATH and prepend the .local/bin
current_path = os.environ["PATH"]
print("Found current path: {}".format(current_path))
if not current_path:
    # If none is set, set a default path
    current_path = (
        "/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    )

# Ensure that the CONDA binary dir is part of the spawned Jupyter Notebook path
# such that the jupyterhub-singleuser launcher can be found by the Jupyter Docker Notebook scripts
os.environ["PATH"] = bin_dir + ":" + current_path
