pip install pip-audit
pip-audit                          # the current environment
pip-audit -r requirements.txt      # a project's pinned requirements
pip-audit -r requirements.txt --fix --dry-run   # show the upgrades it would make
