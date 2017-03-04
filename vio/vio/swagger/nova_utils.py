# Copyright (c) 2017 VMware, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import six


def server_formatter(server):
    # TODO: finish all attributes
    return {
        "id": server.id,
        "name": server.name,
        "tenantId": server.project_id,
        "boot": "",
        "nicArray": {},
        "volumeArray": [v['id'] for v in server.attached_volumes],
        "availabilityZone": server.availability_zone,
        "flavorId": server.flavor['id'],
        "metadata": [{'keyName': k, 'value': v}
                     for k, v in six.iteritems(server.metadata)],
        "securityGroups": [i['name'] for i in server.security_groups],
        "serverGroup": "",
    }


def flavor_formatter(flavor, extra_specs):
    return {
        "id": flavor.id,
        "name": flavor.name,
        "vcpu": flavor.vcpus,
        "memory": flavor.ram,
        "disk": flavor.disk,
        "ephemeral": flavor.ephemeral,
        "swap": flavor.swap,
        "isPublic": flavor.is_public,
        "extraSpecs": extra_specs_formatter(extra_specs)
    }


def extra_specs_formatter(extra_specs):
    return {
    }
