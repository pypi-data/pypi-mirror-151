# Automata Meta Info

## Packaging
`python3 -m build`

## Meta Info in difference "environment" contexts
Development obtains meta info from setup.cfg, while in live (deployed) environment obtains info from installed package Meta Info.

## Development 

### Development (Deployment) Prerequisites
1. `python3 -m pip install --upgrade pip`
2. `pip3 install virtualenv`

### Development (Deployment)
1. `pb` (efficient mode) or `python3 -m build`
2. `python3 -m venv /tmp/automata/meta-info-test`
3. `cd /tmp/automata/meta-info-test`
4. `pa` (efficient mode @ dir) or `source bin/activate`
5. `pip3 install ~/projects/code/automata-projects/automata-meta-info/dist/*.tar.gz`

### Development (Deployment) Iterating
1. `cd /tmp/automata/meta-info-test`
2. `pip3 install --upgrade ~/projects/code/automata-projects/automata-meta-info/dist/*.tar.gz`

### Development (Deployment) Clean
1. `deactivate`
2. `rm -fr /tmp/automata/meta-info-test` 