from django.urls import path
from . import views
from .views import GoogleCalendarInitView, GoogleCalendarRedirectView, index

urlpatterns = [
    path('', index.as_view(), name='index'),
    # entry endpoint
    path('rest/v1/calendar/init/', GoogleCalendarInitView.as_view(), name='calendar_init'),
    # List of Events display end point
    path('rest/v1/calendar/redirect/', GoogleCalendarRedirectView.as_view(), name='calendar_redirect'),
   
]
