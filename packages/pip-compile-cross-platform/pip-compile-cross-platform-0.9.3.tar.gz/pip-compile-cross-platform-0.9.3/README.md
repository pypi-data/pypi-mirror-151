# `pip-compile-cross-platform`

🚨 This is early-stage software, it's currently recommended to verify outputted changes 🚨

## Usage

1. `pip install --user pip-compile-cross-platform`
2. `pip-compile-cross-platform requirements.in`

## Description

[`pip-compile`](https://github.com/jazzband/pip-tools) is an incredible tool built by
[the Jazzband crew](https://jazzband.co/). However, there's one main limitation: [cross-environment usage is
unsupported](https://github.com/jazzband/pip-tools#cross-environment-usage-of-requirementsinrequirementstxt-and-pip-compile).

> As the resulting requirements.txt can differ for each environment, users must execute pip-compile on each Python
> environment separately to generate a requirements.txt valid for each said environment.

`pip-compile-cross-platform` is planned to act as a stand-in replacement for `pip-compile` that **can** produce a
single, source-of-truth `requirements.txt` file that can be used in any target environment.

Note that compatibility with `pip-compile` is still weak, and [help to improve the state of
compatibility would be much appreciated](https://gitlab.com/mitchhentges/pip-compile-cross-platform/-/issues/1).

## How it works

Environment-specific dependencies are defined using [environment markers](https://peps.python.org/pep-0496/).
`pip-compile` processes environment markers up-front according to the current environment.
[`poetry`](https://github.com/python-poetry/poetry), **another** fantastic project, can export a `requirements.txt`
file while tracking the state of all environment markers.

Essentially, `pip-compile-cross-platform` is a thin wrapper around `poetry` that mimicks the interface of `pip-compile`.
