from http.client import HTTPResponse
import os
import json
import datetime
from django.shortcuts import render, HttpResponse

from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from google.oauth2 import credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# client_secret_file should be replaced with your client secret file that is generated from google cloud project
CLIENT_SECRETS_FILE = 'static\\credentials.json'
# scopes determine the permission that we require to fetch the data from google calendar
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


# for Oauth login
class GoogleCalendarInitView(View):
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=request.build_absolute_uri('/rest/v1/calendar/redirect/')
        )
        auth_url, _ = flow.authorization_url(access_type='offline', prompt='consent')

        return HttpResponseRedirect(auth_url)

# for displaying the events from google calendar
class GoogleCalendarRedirectView(View):
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=request.build_absolute_uri('/rest/v1/calendar/redirect/')
        )
        # token is fetched from flow
        flow.fetch_token(authorization_response=request.build_absolute_uri(),
                         code=request.GET.get('code'))

        credentials_dict = flow.credentials.to_json()
        # Save the credentials to the user's profile or session for future use

        credentials_obj = credentials.Credentials.from_authorized_user_info(json.loads(credentials_dict))
        service = build('calendar', 'v3', credentials=credentials_obj)

        # Fetch list of events
        # use now variable to store current time, here 'Z' represents UTC
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        # we can add an extra argument in next line i.e 'timeMin=now' to make list only for upcoming events
        # maxResults can be changed as per choice
        events_result = service.events().list(calendarId='primary', maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        # store events in dictionary results
        results = events
        detail = {"results": results}
        # pass the a parameter detail in render function along with the template html file
        return render(request, 'res.html', detail)
        # Process the events as needed
        # Next line can be used for returning the events data in json format by commenting the previous line
        return JsonResponse({'events': events})

# for landing page
class index(View):
    def get(self, request):
        return render(request, 'index.html')