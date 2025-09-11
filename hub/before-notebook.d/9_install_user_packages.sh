#!/bin/bash

set -e

# Check if DEFAULT_CONDA_ENVIRONMENT is set
if [[ -z "${DEFAULT_CONDA_ENVIRONMENT}" ]]; then
    echo "DEFAULT_CONDA_ENVIRONMENT is not set, skipping user package installation"
# Because *.sh scripts are sourced by the before-notebook.d runner, we need to return on a non-error
    return 0
fi

# Check if USER_INSTALL_FROM_DIRECTORY is set
if [[ -z "${USER_INSTALL_FROM_DIRECTORY}" ]]; then
    echo "USER_INSTALL_FROM_DIRECTORY is not set, skipping user package installation"
# Because *.sh scripts are sourced by the before-notebook.d runner, we need to return on a non-error
    return 0
fi

# Check if USER_INSTALL_FROM_DIRECTORY exists
if [[ ! -d "${USER_INSTALL_FROM_DIRECTORY}" ]]; then
    echo "USER_INSTALL_FROM_DIRECTORY does not exist"
    exit 1
fi

if [[ -n "${USER_INSTALL_PYTHONUSERBASE}" ]]; then
    pip="PYTHONUSERBASE=${USER_INSTALL_PYTHONUSERBASE} PIP_PREFIX=${USER_INSTALL_PYTHONUSERBASE} pip"
else
    pip="pip"
fi

# Iterate over each file in the directory
for file in "${USER_INSTALL_FROM_DIRECTORY}"/*; do
    # Check if the file exists
    if [[ ! -f "${file}" ]]; then
        echo "File ${file} does not exist"
        continue
    fi

    # If the file name extension matches .yml
    # TODO, ensure that the conda environment file is also installed into
    # the PYTHONUSERBASE destination
    if [[ "${file}" == *.yml || "${file}" == *.yaml ]]; then
        conda env update -n "${DEFAULT_CONDA_ENVIRONMENT}" -f "${file}" --dry-run
        rc=$?
        if [[ ${rc} -ne 0 ]]; then
            echo "Failed to dry-run test ${file}, skipping its installation"
        else
            conda env update -n "${DEFAULT_CONDA_ENVIRONMENT}" -f "${file}"
            rc=$?
            if [ ${rc} -ne 0 ]; then
                echo "Failed to install ${file} - ${rc}"
            fi
        fi
    fi

    if [[ "${file}" == *.txt ]]; then
        conda run -n "${DEFAULT_CONDA_ENVIRONMENT}" "${pip}" install -r "${file}" --dry-run
        rc=$?
        if [ ${rc} -ne 0 ]; then
            echo "Failed to dry-run test ${file}, skipping its installation"
        else
            conda run -n "${DEFAULT_CONDA_ENVIRONMENT}" "${pip}" install -r "${file}"
            rc=$?
            if [ ${rc} -ne 0 ]; then
                echo "Failed to install ${file} - ${rc}"
            fi
        fi
    fi

done