# Copyright (c) 2017 VMware, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from vio.pub.msapi import extsys
from vio.pub.vim.vimapi.nova import OperateFlavors
from vio.swagger import nova_utils
from vio.pub.exceptions import VimDriverVioException

class FlavorsView(APIView):

    def post(self, request, vimid, tenantid):
        try:
            create_req = json.loads(request.body)
        except Exception as e:
            return Response(data={'error': 'Fail to decode request body.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            vim_info = extsys.get_vim_by_id(vimid)
        except VimDriverVioException as e:
            return Response(data={'error': str(e)}, status=e.status_code)

        data = {'vimId': vim_info['vimId'],
                'vimName': vim_info['name'],
                'username': vim_info['userName'],
                'password': vim_info['password'],
                'url': vim_info['url']}
        rsp = {'vimId': vim_info['vimId'],
               'vimName': vim_info['name'],
               'tenantId': tenantid}
        flavor_name = create_req.get('name', None)
        flavor_id = create_req.get('id', None)
        flavors_op = OperateFlavors.OperateFlavors()
        exist = False
        try:
            target = flavor_id or flavor_name
            flavor = flavors_op.find_flavor(data, tenantid, target)
            if flavor:
                flavor, extra_specs = flavors_op.get_flavor(
                    data, tenantid, flavor.id)
                rsp['returnCode'] = 0
                exist = True
            else:
                rsp['returnCode'] = 1
                flavor, extra_specs = flavors_op.create_flavor(
                    data, tenantid, create_req)
            flavor_dict = nova_utils.flavor_formatter(flavor, extra_specs)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        rsp.update(flavor_dict)
        if exist:
            return Response(data=rsp, status=status.HTTP_200_OK)
        else:
            return Response(data=rsp, status=status.HTTP_202_ACCEPTED)

    def get(self, request, vimid, tenantid):
        try:
            vim_info = extsys.get_vim_by_id(vimid)
        except VimDriverVioException as e:
            return Response(data={'error': str(e)}, status=e.status_code)

        data = {'vimId': vim_info['vimId'],
                'vimName': vim_info['name'],
                'username': vim_info['userName'],
                'password': vim_info['password'],
                'url': vim_info['url']}
        query = dict(request.query_params)
        flavors_op = OperateFlavors.OperateFlavors()
        try:
            flavors_result = flavors_op.list_flavors(data, tenantid, **query)
            flavors_dict = [nova_utils.flavor_formatter(flavor, extra)
                            for flavor, extra in flavors_result]
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        rsp = {'vimId': vim_info['vimId'],
               'vimName': vim_info['name'],
               'tenantId': tenantid,
               'flavors': flavors_dict}

        return Response(data=rsp, status=status.HTTP_200_OK)


class FlavorView(APIView):

    def get(self, request, vimid, tenantid, flavorid):
        try:
            vim_info = extsys.get_vim_by_id(vimid)
        except VimDriverVioException as e:
            return Response(data={'error': str(e)}, status=e.status_code)

        data = {'vimId': vim_info['vimId'],
                'vimName': vim_info['name'],
                'username': vim_info['userName'],
                'password': vim_info['password'],
                'url': vim_info['url']}

        flavors_op = OperateFlavors.OperateFlavors()
        try:
            flavor, extra_specs = flavors_op.get_flavor(data, tenantid, flavorid)
            flavor_dict = nova_utils.flavor_formatter(flavor, extra_specs)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        rsp = {'vimId': vim_info['vimId'],
               'vimName': vim_info['name'],
               'tenantId': tenantid}
        rsp.update(flavor_dict)
        return Response(data=rsp, status=status.HTTP_200_OK)

    def delete(self, request, vimid, tenantid, flavorid):
        try:
            vim_info = extsys.get_vim_by_id(vimid)
        except VimDriverVioException as e:
            return Response(data={'error': str(e)}, status=e.status_code)

        data = {'vimId': vim_info['vimId'],
                'vimName': vim_info['name'],
                'username': vim_info['userName'],
                'password': vim_info['password'],
                'url': vim_info['url']}
        flavors_op = OperateFlavors.OperateFlavors()
        try:
            flavors_op.delete_flavor(data, tenantid, flavorid)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_204_NO_CONTENT)
