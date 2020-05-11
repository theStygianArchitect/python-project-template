#! /usr/bin/env python
"""
Description: Generate an env file based off of environment variables.

Title: env_generation.py

Author: theStygianArchitect
"""
import argparse
import os


def write_env_file(branch):
    """Create a .env file in the working directory location.

    This function creates a .env file in the working directory
    location.

    Args:
        branch(str): The name of the git branch this is on.

    Returns:
        Nothing.

    """
    with open('.env', 'w') as env_file_obj:
        for env in os.environ:
            if env.startswith(branch.lower()):
                key_ = env
                value = os.environ[env]
                key_ = key_.replace("%s_" % branch, '')
                env_file_obj.write("%s=%s" % (key_, value))
                env_file_obj.write('\n')


def main():
    """Grab variables for module."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', required=True)
    args = parser.parse_args()
    write_env_file(args.branch)


if __name__ == '__main__':
    main()
