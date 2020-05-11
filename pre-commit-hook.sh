#!/usr/bin/env sh


# declare vars
test_directory_list=$(ls tests/*.py)
app_directory_list=$(ls app/*.py)
#script_name=$(basename "$0")
#current_directory=$(pwd)

# create project pre-commit
#ln -s -f "$0" "${current_directory}/.git/hooks/pre-commit"

# security code scanning
poetry run safety check
exit_code=$?

if [ ${exit_code} != 0 ];
then
    exit ${exit_code}
fi

for python_file_name in ${test_directory_list}
do
    poetry run bandit "${python_file_name}"
    exit_code=$?

    if [ ${exit_code} != 0 ];
    then
        exit ${exit_code}
    fi
done

for python_file_name in ${app_directory_list}
do
    poetry run bandit "${python_file_name}"
    exit_code=$?

    if [ ${exit_code} != 0 ];
    then
        exit ${exit_code}
    fi
done

# Unit Testing
poetry run python -m pytest tests/
exit_code=$?

if [ ${exit_code} != 0 ];
then
    exit ${exit_code}
fi

# code linting
for python_file_name in ${app_directory_list}
do
    poetry run pylint "${python_file_name}"
    exit_code=$?

    if [ ${exit_code} != 0 ];
    then
        exit ${exit_code}
    fi
done

for python_file_name in ${app_directory_list}
do
    poetry run pycodestyle --max-line-length 100 "${python_file_name}"
    exit_code=$?

    if [ ${exit_code} != 0 ];
    then
        exit ${exit_code}
    fi
done

# doc linting
for python_file_name in ${app_directory_list}
do
    poetry run pydocstyle "${python_file_name}"
    exit_code=$?

    if [ ${exit_code} != 0 ];
    then
        exit ${exit_code}
    fi
done


# code type linting
for python_file_name in ${app_directory_list}
do
    poetry run mypy "${python_file_name}" --ignore-missing-imports
    exit_code=$?

    if [ ${exit_code} != 0 ];
    then
        exit ${exit_code}
    fi
done
