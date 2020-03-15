"""
This module contains the urls for the Farely API.
"""

from django.urls import path
from . import apis

app_name = 'api'

urlpatterns = [
	path('find-routes/', apis.FindRoutesApi.as_view(), name='find-routes'),
	path('dummy-find-routes/', apis.DummyFindRoutesApi.as_view(), name='dummy-find-routes'),
]
