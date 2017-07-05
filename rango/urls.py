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
import views
from django.conf.urls import include, url
from django.conf import settings


app_name = 'rango'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',views.show_category,name="show_category"),
    url(r'^add_category/$',views.add_category, name="add_category"),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',views.add_page,name="add_page"),
    url(r'^register/$',views.register, name="register"),
    url(r'^restricted/$',views.restricted, name="restricted"),
    url(r'^login/$',views.user_login,name="login"),
    url(r'^logout/$',views.user_logout, name="logout"),
    url(r'^goto/$', views.track_url, name="goto"),
    url(r'^register_profile/$', views.register_profile , name='register_profile'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile,name='profile'),
    url(r'^profiles/$', views.list_profiles, name='list_profiles'),
    url(r'^like/$', views.like_category, name='like_category'),
    url(r'^suggest/$', views.suggest_category, name='suggest_category'),
]

