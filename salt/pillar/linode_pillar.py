#!/usr/bin/env python
# -*- mode: Python; -*-
"""This is an external pillar module for SaltStack that uses the
Linode APIv4 to construct pillar data based on tags.

:depends linode_api4

This allows you to look up the tags associated with the Linode object
of each minion. Note that this module assumes that your minion IDs
match your Linode labels.

This can be used for minion targeting with SaltStack's pillar matcher:

https://docs.saltstack.com/en/latest/ref/modules/all/salt.modules.match.html#salt.modules.match.pillar

Configuring the linode_pillar ext_pillar
========================================\
.. code-block:: yaml
ext_pillar:
  - linode_pillar:
      "token": "linodeapitokengoeshere"
      "account_name": "linodetest"
"""

import logging
log = logging.getLogger(__name__)

__virtualname__ = 'linode_pillar'
client = None

try:
    import linode_api4
    LINODE_API_LOADED = True
except ImportError:
    LINODE_API_LOADED = False

def __virtual__():
    if LINODE_API_LOADED:
        return __virtualname__
    return False

def ext_pillar(minion_id, pillar, account_name, token=None):
    client = linode_api4.LinodeClient(token)
    matched_linodes = client.linode.instances(linode_api4.Instance.label == minion_id)
    if(matched_linodes):
        linode = matched_linodes[0]
        return {"tags": {account_name: linode.tags}}
    else:
        return {"tags": {account_name: []}}
