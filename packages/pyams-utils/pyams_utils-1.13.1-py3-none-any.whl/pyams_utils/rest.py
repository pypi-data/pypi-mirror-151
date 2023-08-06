#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_utils.rest module

This module provides CORS requests handlers, as well as OpenAPI
documentation for all defined Cornice REST endpoints.
"""

import sys
from cgi import FieldStorage

from colander import Date, Mapping, SchemaNode, SequenceSchema, String, Tuple, TupleSchema, drop, \
    null
from cornice import Service
from cornice.service import get_services
from cornice_swagger import CorniceSwagger
from cornice_swagger.converters.schema import ArrayTypeConverter, ObjectTypeConverter, \
    StringTypeConverter
from pyramid.httpexceptions import HTTPServerError
from pyramid.interfaces import IRequest

from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces.rest import ICORSRequestHandler


__docformat__ = 'restructuredtext'

from pyams_utils import _


@adapter_config(required=IRequest,
                provides=ICORSRequestHandler)
class CORSRequestHandler:
    """Base CORS request handler"""

    def __init__(self, request):
        self.request = request

    def handle_request(self, allowed_methods=None):
        """Add requested headers to current request"""
        request = self.request
        req_headers = request.headers
        resp_headers = request.response.headers
        resp_headers['Access-Control-Allow-Credentials'] = 'true'
        resp_headers['Access-Control-Allow-Origin'] = \
            req_headers.get('Origin', request.host_url)
        if 'Access-Control-Request-Headers' in req_headers:
            resp_headers['Access-Control-Allow-Headers'] = \
                req_headers.get('Access-Control-Request-Headers', 'Origin')
        if 'Access-Control-Request-Method' in req_headers:
            try:
                service = request.current_service
                resp_headers['Access-Control-Allow-Methods'] = \
                    ', '.join(service.cors_supported_methods)
            except AttributeError as exc:
                if allowed_methods:
                    resp_headers['Access-Control-Allow-Methods'] = ', '.join(allowed_methods)
                else:
                    test_mode = sys.argv[-1].endswith('/test')
                    if not test_mode:
                        raise HTTPServerError from exc


def handle_cors_headers(request, allowed_methods=None):
    """Handle CORS headers on REST service

    :param request: original request
    :param allowed_methods: list, tuple or set of allowed HTTP methods; if None, list of
        allowed methods will be extracted from Cornice service handlers.
    """
    handler = ICORSRequestHandler(request, None)
    if handler is not None:
        handler.handle_request(allowed_methods)


class StringListSchema(SequenceSchema):
    """Strings list schema field"""
    value = SchemaNode(String(),
                       title=_("Item value"),
                       missing=drop)


class StringListTypeConverter(ArrayTypeConverter):
    """Strings list type converter"""


class PropertiesMapping(Mapping):
    """Properties schema"""

    name = 'properties'

    def serialize(self, node, appstruct):
        if appstruct is null:
            return {}
        return appstruct

    def deserialize(self, node, cstruct):
        return cstruct


class PropertiesMappingTypeConverter(ObjectTypeConverter):
    """Properties mapping type converter"""


class DateRangeSchema(TupleSchema):
    """Dates range schema type"""
    after = SchemaNode(Date(),
                       title=_("Range beginning date"),
                       missing=null)
    before = SchemaNode(Date(),
                        title=_("Range ending date (excluded)"),
                        missing=null)


class DateRangeTypeConverter(ArrayTypeConverter):
    """Date range type converter"""


class FileUploadType(String):
    """File upload type"""

    def deserialize(self, node, cstruct):
        """File upload deserializer"""
        if isinstance(cstruct, FieldStorage):
            return cstruct
        return super().deserialize(node, cstruct)


class FileUploadTypeConverter(StringTypeConverter):
    """File upload type converter"""


# update Cornice-Swagger types converters
CorniceSwagger.custom_type_converters.update({
    Tuple: ArrayTypeConverter,
    StringListSchema: StringListTypeConverter,
    PropertiesMapping: PropertiesMappingTypeConverter,
    DateRangeSchema: DateRangeTypeConverter,
    FileUploadType: FileUploadTypeConverter
})


swagger = Service(name='OpenAPI',
                  path='/__api__',
                  description="OpenAPI documentation")


@swagger.options()
def openapi_options(request):
    """OpenAPI OPTIONS verb handler"""
    return handle_cors_headers(request)


@swagger.get()
def openapi_specification(request):  # pylint: disable=unused-argument
    """OpenAPI specification"""
    doc = CorniceSwagger(get_services())
    doc.summary_docstrings = True
    return doc.generate('PyAMS', '1.0')
