#
# Copyright (c) 2015-2022 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_security.rest module

This module defines components which are used to improve security of REST services
using CORS requests.
"""

import sys

from persistent import Persistent
from pyramid.httpexceptions import HTTPServerError, HTTPServiceUnavailable
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_security.interfaces import ISecurityManager
from pyams_security.interfaces.rest import CORS_CONFIGURATION_KEY, ICORSSecurityInfo
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_utility


__docformat__ = 'restructuredtext'


@factory_config(ICORSSecurityInfo)
class CORSSecurityInfo(Persistent, Contained):
    """CORS security persistent info"""

    restrict_origins = FieldProperty(ICORSSecurityInfo['restrict_origins'])
    allowed_origins = FieldProperty(ICORSSecurityInfo['allowed_origins'])

    def check_origin(self, request):
        """Check origin of CORS request"""
        if not self.restrict_origins:
            return
        origin = request.headers.get('Origin', request.host_url)
        if (origin == request.host_url) or (origin in (self.allowed_origins or ())):
            return
        raise HTTPServiceUnavailable('Forbidden origin')

    @staticmethod
    def set_headers(request):
        """Set CORS headers of provided request"""
        req_headers = request.headers
        resp_headers = request.response.headers
        resp_headers['Access-Control-Allow-Credentials'] = 'true'
        resp_headers['Access-Control-Allow-Origin'] = \
            req_headers.get('Origin', request.host_url)
        if 'Access-Control-Request-Headers' in req_headers:
            resp_headers['Access-Control-Allow-Headers'] = \
                req_headers.get('Access-Control-Request-Headers', 'origin')
        if 'Access-Control-Request-Method' in req_headers:
            try:
                service = request.current_service
                resp_headers['Access-Control-Allow-Methods'] = \
                    ', '.join(service.cors_supported_methods)
            except AttributeError as exc:
                test_mode = sys.argv[-1].endswith('/test')
                if not test_mode:
                    raise HTTPServerError from exc


@adapter_config(required=ISecurityManager, provides=ICORSSecurityInfo)
def security_manager_cors_configuration_factory(context):
    """Security manager CORS configuration factory"""
    return get_annotation_adapter(context, CORS_CONFIGURATION_KEY, ICORSSecurityInfo)


def check_cors_origin(request, **kwargs):  # pylint: disable=unused-argument
    """Cornice service origin validator"""
    sm = get_utility(ISecurityManager)  # pylint: disable=invalid-name
    cors_info = ICORSSecurityInfo(sm)
    cors_info.check_origin(request)


def set_cors_headers(request, **kwargs):  # pylint: disable=unused-argument
    """Set REST CORS headers"""
    sm = get_utility(ISecurityManager)  # pylint: disable=invalid-name
    cors_info = ICORSSecurityInfo(sm)
    cors_info.set_headers(request)
