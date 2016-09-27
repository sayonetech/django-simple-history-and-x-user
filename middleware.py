from re import sub

from rest_framework.authtoken.models import Token
from simple_history.models import HistoricalRecords

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


User = get_user_model()


class MockRequest(object):
    user = None


class HistoryRequestMiddleware(object):
    """
    Just overriding the HistoricalRecords middleware

    Expose request to HistoricalRecords.

    This middleware sets request as a local thread variable, making it
    available to the model-level utilities to allow tracking of the
    authenticated user making a change.
    """

    def process_request(self, request):
        try:
            # For x-user
            x_user_token = request.META['HTTP_X_REQUESTED_WITH']

            token_obj = Token.objects.get(key=x_user_token)
            user_token = request.META['HTTP_AUTHORIZATION']
            if x_user_token in user_token:
                # When user and x-user is the same, handle here
                pass

            mock_request = MockRequest()
            mock_request.user = token_obj.user
            if token_obj.user.is_staff:
                MockRequest.user = token_obj.user
                HistoricalRecords.thread.request = mock_request
            else:
                HistoricalRecords.thread.request = request

        except:
            # For normal user
            HistoricalRecords.thread.request = request

    def process_response(self, request, response):
        MockRequest.user = None
        if hasattr(HistoricalRecords.thread, 'request'):
            del HistoricalRecords.thread.request
        return response
