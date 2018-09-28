## SFLVault Server

[![Build Status](https://travis-ci.org/savoirfairelinux/sflvault-server.svg?branch=v2)](https://travis-ci.org/savoirfairelinux/sflvault-server)
[![Coverage Status](https://coveralls.io/repos/github/savoirfairelinux/sflvault-server/badge.svg?branch=v2)](https://coveralls.io/github/savoirfairelinux/sflvault-server?branch=v2)
This branch tracks the work in progress on version 2.0 of the SFLVault server.


## Generate Graph Model

```python3 manage.py graph_models -a -o docs/model.png```

## Install

Install Pipenv (https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv):
> pip install --user pipenv

Troubleshooting
* Check that ~/.local/bin is in your PATH:
> echo $PATH

If not, append this to your .bashrc:
> export PATH=$PATH:~/.local/bin

Install project's dependencies:
> pipenv install