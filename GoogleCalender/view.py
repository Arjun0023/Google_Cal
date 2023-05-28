# calendar_integration/views.py

import json
import requests
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response

class GoogleCalendarInitView(APIView):
    def get(self, request):
        redirect_url = 'https://accounts.google.com/o/oauth2/auth'
        params = {
            'response_type': 'code',
            'client_id': settings.GOOGLE_CALENDAR_CLIENT_ID,
            'redirect_uri': settings.GOOGLE_CALENDAR_REDIRECT_URI,
            'scope': 'https://www.googleapis.com/auth/calendar.readonly',
        }
        return redirect(f'{redirect_url}?{urlencode(params)}')

class GoogleCalendarRedirectView(APIView):
    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return HttpResponseBadRequest('Authorization code not found.')
        token_url = 'https://oauth2.googleapis.com/token'
        data = {
            'code': code,
            'client_id': settings.GOOGLE_CALENDAR_CLIENT_ID,
            'client_secret': settings.GOOGLE_CALENDAR_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_CALENDAR_REDIRECT_URI,
            'grant_type': 'authorization_code',
        }
        response = requests.post(token_url, data=data)
        token_data = json.loads(response.text)
        access_token = token_data.get('access_token')
        events_url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        response = requests.get(events_url, headers=headers)
        events_data = json.loads(response.text)

        return Response(events_data)
