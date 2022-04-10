#! /usr/bin/env python
"""
Description: Generate an env file based off of environment variables.

Title: env_generation.py

Author: theStygianArchitect
"""
import argparse
import os
from typing import Text


def write_env_file(branch: Text):
    """Create a .env file in the working directory location.

    This function creates a .env file in the working directory
    location.

    Args:
        branch(str): The name of the git branch this is on.

    Returns:
        None.

    """
    with open('.env', 'w') as env_file_obj:
        for env in os.environ:
            if env.startswith(branch.lower()):
                key_ = env
                value = os.environ[env]
                key_ = key_.replace("%s_" % branch, '')
                env_file_obj.write("%s=%s" % (key_, value))
                env_file_obj.write('\n')


def read_env_file(env_file: Text = None):
    """Read a .env file in the working directory location.

    This function reads a .env file in the working directory
    location.

    """
    if not env_file:
        env_file = '.env'
    with open(env_file) as env_file_obj:
        for line in env_file_obj:
            line = line.rstrip().lstrip()
            if not line or line.startswith('#'):
                continue
            key_ = f"{line.split('=', 1)[0]}"
            value_ = f"{line.split('=', 1)[1]}"
            if key_ not in os.environ:
                os.environ[key_] = value_


def main():
    """Grab variables for module."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', required=True)
    args = parser.parse_args()
    write_env_file(args.branch)


if __name__ == '__main__':
    main()
