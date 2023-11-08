#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Zscaler Technology Alliances, <zscaler-partner-labs@z-bd.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: zia_traffic_forwarding_vpn_credentials_facts
short_description: "Gets VPN credentials that can be associated to locations"
description:
  - "Gets VPN credentials that can be associated to locations"
author:
  - William Guilherme (@willguibr)
version_added: "1.0.0"
requirements:
    - Zscaler SDK Python can be obtained from PyPI U(https://pypi.org/project/zscaler-sdk-python/)
extends_documentation_fragment:
    - zscaler.ziacloud.fragments.credentials_set
    - zscaler.ziacloud.fragments.provider
options:
  id:
    description:
      - VPN credential id
    required: false
    type: int
  fqdn:
    description: "Fully Qualified Domain Name. Applicable only to UFQDN or XAUTH (or HOSTED_MOBILE_USERS) auth type."
    required: false
    type: str

"""

EXAMPLES = """

- name: Retrieve Details of All ZPN Credentials.
  zscaler.ziacloud.zia_traffic_forwarding_vpn_credentials_facts:

- name: Retrieve Details of Specific ZPN Credentials By fqdn.
  zscaler.ziacloud.zia_traffic_forwarding_vpn_credentials_facts:
    fqdn: "sjc-1-37@acme.com"

- name: Retrieve Details of Specific ZPN Credentials By ID.
  zscaler.ziacloud.zia_traffic_forwarding_vpn_credentials_facts:
    id: 222

"""


from traceback import format_exc

from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.zscaler.ziacloud.plugins.module_utils.zia_client import (
    ZIAClientHelper,
)


def core(module):
    client = ZIAClientHelper(module)
    vpn_id = module.params.get("id", None)
    fqdn = module.params.get("fqdn", None)
    credentials = []
    if vpn_id is not None or fqdn is not None:
        if vpn_id is not None:
            credentialBox = client.traffic.get_vpn_credential(credential_id=vpn_id)
        else:
            credentialBox = client.traffic.get_vpn_credential(fqdn=fqdn)
        if credentialBox is None:
            module.fail_json(msg="Failed to retrieve vpn credential ID: '%s'" % (id))
        credentials = [credentialBox.to_dict()]
    else:
        credentials = client.traffic.list_vpn_credentials().to_list()
    module.exit_json(changed=False, data=credentials)


def main():
    argument_spec = ZIAClientHelper.zia_argument_spec()
    argument_spec.update(
        fqdn=dict(type="str", required=False),
        id=dict(type="int", required=False),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
