"""Turns database errors into readable API answers instead of "500 Server Error".

  * saving a duplicate (e.g. a second theme for the same user)  -> 400
  * deleting a record that other records still use              -> 409
"""
from django.db import IntegrityError
from django.db.models import ProtectedError, RestrictedError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)      # DRF's own handling first
    if response is not None:
        return response
    if isinstance(exc, (ProtectedError, RestrictedError)):
        return Response({'detail': 'This record cannot be deleted because other records use it.'}, status=409)
    if isinstance(exc, IntegrityError):
        return Response({'detail': 'Could not save: a record with the same unique value already exists, '
                                   'or a related record is missing.'}, status=400)
    return None                                     # anything else is a real bug -> normal 500
