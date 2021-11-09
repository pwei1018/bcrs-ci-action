# PR approve and comments - GitHub Actions

A GitHub action that approve the PR with contidition and post a given message.

## Usage

```
name: example action

on:
  pull_request:
    branches:
      - master

jobs:
  example-action:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Get PR approval
        id: pr
        run: |
          echo "::set-output name=approval::true"
          echo "::set-output name=message::This pull request looks good."
      - uses: pwei1018/bcrs-ci-action@v1.0.1
        with:
          github-token: "${{ secrets.GITHUB_TOKEN }}"
          pr-approval: "${{ steps.pr.outputs.approval }}"
          pr-message: "${{ steps.pr.outputs.message }}"

```

See examples in [example PR](https://github.com/pwei1018/bcrs-ci-actions/pulls) !

## Contributing
