#!/usr/bin/env python3

import os
import sys
import re
from github import Github


def get_env_var(env_var_name, echo_value=False):
    """Try to get the value from a environmental variable.

    If the values is 'None', then a ValueError exception will
    be thrown.

    Args:
        env_var_name (string): The name of the environmental variable.
        echo_value (bool): Print the resulting value

    Returns:
        string: the value from the environmental variable.
    """
    value = os.environ.get(env_var_name)

    if value == None:
        raise ValueError(
            f'The environmental variable {env_var_name} is empty!')

    if echo_value:
        print(f"{env_var_name} = {value}")

    return value


# Check if the number of input arguments is correct
if len(sys.argv) != 3:
    raise ValueError('Invalid number of arguments!')

# Get the GitHub token
token = sys.argv[1]
print(f'token: {token}')

# Get the list of valid labels
compare_result = sys.argv[2]
print(f'Vaults match: {compare_result}')

# Get needed values from the environmental variables
repo_name = get_env_var('GITHUB_REPOSITORY')
github_ref = get_env_var('GITHUB_REF')

# Create a repository object, using the GitHub token
repo = Github(token).get_repo(repo_name)

# Try to extract the pull request number from the GitHub reference.
try:
    pr_number = int(re.search('refs/pull/([0-9]+)/merge', github_ref).group(1))
    print(f'Pull request number: {pr_number}')
except AttributeError:
    raise ValueError(
        f'The Pull request number could not be extracted from the GITHUB_REF = {github_ref}')

# Create a pull request object
pr = repo.get_pull(pr_number)

# Check if there were at least one valid label
# Note: In both cases we exit without an error code and let the check to succeed. This is because GitHub
# workflow will create different checks for different trigger conditions. So, adding a missing label won't
# clear the initial failed check during the PR creation, for example.
# Instead, we will create a pull request review, marked with 'REQUEST_CHANGES' when no valid label was found.
# This will prevent merging the pull request until a valid label is added, which will trigger this check again
# and will create a new pull request review, but in this case marked as 'APPROVE'

if compare_result == 'true':
    # If there were valid labels, then create a pull request request review, approving it
    pr.create_review(body='This pull request does not need to update 1password vault.',
                     event='APPROVE')
else:
    # If there were not valid labels, then create a pull request review, requesting changes
    pr.create_review(body='This pull request need to update 1password vault. ',
                     event='REQUEST_CHANGES')
