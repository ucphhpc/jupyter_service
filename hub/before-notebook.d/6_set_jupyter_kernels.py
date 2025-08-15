#!/opt/conda/bin/python
import json
import os
from fcntl import flock, LOCK_EX
from jupyter_client import kernelspec

PYTHON_LANGUAGE = "python"
kernels = []
kernelspecs = kernelspec.find_kernel_specs()
for k_name in kernelspecs:
    kernels.append({"name": k_name, "spec": kernelspec.get_kernel_spec(k_name)})

current_environment = os.environ.copy()
jupyter_kernel_envs = {}
# Extract the jupyter kernel environment variables
# Expects the format of the kernel specific environment variables to
# be JUPYTER_KERNEL_<kernel_name>_<variable_name>=<value>
for key in current_environment:
    if key.startswith("JUPYTER_KERNEL_"):
        kernel_environment_var = key.replace("JUPYTER_KERNEL_", "")
        kernel_name = kernel_environment_var.split("_")[0].lower()

        environment_key = kernel_environment_var.split("_")[1]
        environment_value = current_environment[key]
        jupyter_kernel_envs[kernel_name] = {environment_key: environment_value}

# Update the kernel spec environment for each kernel
for kernel in kernels:
    name = kernel["name"]
    spec = kernel["spec"]

    # Get the kernel environment variables
    kernel_environment = jupyter_kernel_envs.get(name, {})
    for key in kernel_environment:
        spec.env.update({key: kernel_environment[key]})

    # Add the kernel environment variables to the kernel spec file
    if spec.env:
        kernel_path = os.path.join(spec.resource_dir, "kernel.json")
        kernel_lock_path = os.path.join(spec.resource_dir, "kernel.json.lock")
        with open(kernel_lock_path, "a") as lock_file:
            flock(lock_file.fileno(), LOCK_EX)
            with open(kernel_path, "w") as kernel_file:
                kernel_dict = spec.to_dict()
                json.dump(kernel_dict, kernel_file, indent=4)
