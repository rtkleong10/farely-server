"""Contains the urls for the Farely API.

Handles the routing for the api views.
"""

from django.urls import path
from . import apis

app_name = 'api'

urlpatterns = [
	path('find-routes/', apis.FindRoutesApi.as_view(), name='find-routes'),
]
