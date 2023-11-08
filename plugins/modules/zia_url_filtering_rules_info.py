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
module: zia_url_filtering_rules_info
short_description: "Gets all url filtering rules."
description: "Gets all rules in the URL filtering policy."
author:
  - William Guilherme (@willguibr)
version_added: "1.0.0"
requirements:
    - Zscaler SDK Python can be obtained from PyPI U(https://pypi.org/project/zscaler-sdk-python/)
options:
  username:
    description: "Username of admin user that is provisioned"
    required: true
    type: str
  password:
    description: "Password of the admin user"
    required: true
    type: str
  api_key:
    description: "The obfuscated form of the API key"
    required: true
    type: str
  base_url:
    description: "The host and basePath for the cloud services API"
    required: true
    type: str
  id:
    description: "URL Filtering Rule ID"
    required: false
    type: int
  name:
    description: "Name of the URL filtering rule"
    required: true
    type: str
"""

EXAMPLES = """
- name: Gather Information Details of all URL filtering rules
  zscaler.ziacloud.zia_url_filtering_rules_info:

- name: Gather Information Details of of a URL filtering rules
  zscaler.ziacloud.zia_firewall_filtering_rules_info:
    name: "Example"
"""

RETURN = """
# Returns information on a specified URL filtering rule
"""

from traceback import format_exc

from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.zscaler.ziacloud.plugins.module_utils.zia_client import (
    zia_argument_spec,
)
from zscaler import ZIA


def core(module: AnsibleModule):
    rule_id = module.params.get("id", None)
    rule_name = module.params.get("name", None)
    client = ZIA(
        api_key=module.params.get("api_key", ""),
        cloud=module.params.get("base_url", ""),
        username=module.params.get("username", ""),
        password=module.params.get("password", ""),
    )
    rules = []
    if rule_id is not None:
        ruleBox = client.url_filters.get_rule(rule_id=rule_id)
        if ruleBox is None:
            module.fail_json(
                msg="Failed to retrieve URL Filtering Rule ID: '%s'" % (rule_id)
            )
        rules = [ruleBox.to_dict()]
    else:
        rules = client.url_filters.list_rules().to_list()
        if rule_name is not None:
            ruleFound = False
            for rule in rules:
                if rule.get("name") == rule_name:
                    ruleFound = True
                    rules = [rule]
            if not ruleFound:
                module.fail_json(
                    msg="Failed to retrieve URL Filtering Rule Name: '%s'" % (rule_name)
                )
    module.exit_json(changed=False, data=rules)


def main():
    argument_spec = zia_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=False),
        id=dict(type="int", required=False),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
