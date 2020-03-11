from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
	path('find-routes/', views.FindRoutesAPI.as_view(), name='find-routes'),
	path('calculate-fare/', views.CalculateFareAPI.as_view(), name='calculate-fare'),
	path('dummy-find-routes/', views.DummyFindRoutesAPI.as_view(), name='dummy-find-routes'),
]
