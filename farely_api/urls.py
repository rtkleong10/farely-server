from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
	path('interpret-location/', views.InterpretLocationAPI.as_view(), name='interpret-location'),
	path('find-routes/', views.FindRoutesAPI.as_view(), name='find-routes'),
]
