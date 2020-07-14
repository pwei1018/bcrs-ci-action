#!/usr/bin/env python3

import os
import sys
import re
from github import Github


def get_env_var(env_var_name, echo_value=False):
    """Get the value from a environmental variable. """
    value = os.environ.get(env_var_name)

    if value is None:
        raise ValueError(
            f'The environmental variable {env_var_name} is empty!')

    if echo_value:
        print(f"{env_var_name} = {value}")

    return value


def get_pr(github_token):
    """Get the value from a environmental variable. """
    # Get needed values from the environmental variables
    repo_name = get_env_var('GITHUB_REPOSITORY')
    github_ref = get_env_var('GITHUB_REF')

    # Create a repository object, using the GitHub token
    repo = Github(github_token).get_repo(repo_name)

    # Try to extract the pull request number from the GitHub reference.
    try:
        pr_number = int(
            re.search('refs/pull/([0-9]+)/merge', github_ref).group(1))
        print(f'Pull request number: {pr_number}')
    except AttributeError:
        raise ValueError(
            f'The Pull request number could not be extracted from the GITHUB_REF = {github_ref}')

    return repo.get_pull(pr_number)


# Check if the number of input arguments is correct
if len(sys.argv) != 4:
    raise ValueError('Invalid number of arguments!')

# Get the environment variables
github_token = sys.argv[1]
pr_approval = sys.argv[2]
pr_message = sys.argv[3]

pr = get_pr(github_token)

if pr_approval == 'true':
    pr.create_review(body=pr_message, event='APPROVE')
else:
    pr.create_review(body=pr_message, event='REQUEST_CHANGES')
