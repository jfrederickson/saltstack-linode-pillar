# Linode SaltStack External Pillar Module

An external pillar module using the Linode API for tag matching.

## Installation

```
pip install -r requirements.txt
python setup.py install
```

## Usage

*NOTE: Your minion IDs and Linode labels must match for this module to work!*

In your salt master config's `ext_pillar` section, add a config like this:

```yaml
ext_pillar:
  - linode_pillar:
      "token": "linodeapitokengoeshere"
      "account_name": "linodetest"
```

The `account_name` is an arbitrary name used to distinguish between
accounts, if you have multiple.

Then restart your salt master. Tags should then be available as pillar
values under the `tags` key. For example, if you have a Linode called
`salttest` that has the tag `web`, under an account that you've named
`linodetest`:

```
salttest:~# salt-call pillar.get tags
local:
    ----------
    linodetest:
        - web
```

You can then use this pillar data with salt's pillar matcher:

```
salt-master:~# salt -I "tags:linodetest:web" test.ping
salttest:
    True
```
