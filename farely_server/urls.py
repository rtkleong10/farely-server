"""farely_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from django.views.static import serve
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

favicon_view = RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)

urlpatterns = [
	path('api/', include('farely_api.urls')),
	path('favicon.ico/', favicon_view),

	# Docs
	re_path(r'^docs/farely_api/$', serve, {'document_root': os.path.join(BASE_DIR, 'html/farely_api'), 'path': 'index.html'}, name="docs-farely_api-index"),
    re_path(r'^docs/farely_api/(.+)$', serve, {'document_root': os.path.join(BASE_DIR, 'html/farely_api')}, name="docs-farely_api"),
	re_path(r'^docs/farely_server/$', serve, {'document_root': os.path.join(BASE_DIR, 'html/farely_server'), 'path': 'index.html'}, name="docs-farely_server-index"),
    re_path(r'^docs/farely_server/(.+)$', serve, {'document_root': os.path.join(BASE_DIR, 'html/farely_server')}, name="docs-farely_server"),
]