"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
#from rango import views
#from rango import urls as rangoURL
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from django.conf import settings

from registration.backends.simple.views import RegistrationView

# Create a new class that redirects the user to the index page,
#if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return  '/rango/register_profile/'

urlpatterns = [
#    url(r'^$',views.index, name='index'),
#    url(r'^rango/', include(rangoURL.urlpatterns)),
    url(r'^rango/', include('rango.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/register/$',MyRegistrationView.as_view(),name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
