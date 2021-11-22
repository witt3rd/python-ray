# Python Setup

We use `pyenv` to manage Python versions and `pipenv` to manage project dependencies and virtual environments as described in the following article:

- [How to Manage your Python Projects with Pipenv & Pyenv](https://www.rootstrap.com/blog/how-to-manage-your-python-projects-with-pipenv-pyenv/)

TLDR:

Install Pyenv:

```bash
curl https://pyenv.run | bash
```

Ensure your .profile, .bashrc, etc. is configured properly:

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
```

Refresh your shell.

Update Pyenv:

```bash
pyenv update
```

Install and use a Python version (globally):

```bash
pyenv install --list # list all available versions
pyenv install 3.9.9 # or whatever version you want
pyenv global 3.9.9 # or whatever version you want
pyenv version # check current version
```

Install Pipenv:

```bash
pip install --user pipenv
```

To activate:

```bash
pipenv shell
```

Select the Pipenv version of the Python interpreter in VS Code from the Command Palette (Ctrl+Shift+P).
