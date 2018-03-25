from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'name'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    
]
