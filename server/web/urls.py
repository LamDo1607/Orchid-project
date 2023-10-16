from django.conf.urls import url

from . import views
from orchid.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap
}

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^404/$', views.notfound, name='notfound'),
    url(r'^histories/$', views.histories),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^users/$', views.users), 
    url(r'^gallery/$', views.gallery),
    url(r'^changepassword/$', views.changepassword),
    url(r'^register/$', views.register),
    url(r'^camera/$', views.camera),
    url(r'^webcam/$', views.webcam),
    url(r'^orchid/$', views.orchid),
    url(r'^location/$', views.location),
    url(r'^orgs/$', views.orgs),
    url(r'^species/$', views.species),
    url(r'^predict/$', views.predict),
    url(r'^profile/$', views.profile),
    url(r'^systeminfo/$', views.system_info),
    url(r'^upload/$', views.upload),
    url(r'^redirect/$', views.Redirect),
    url(r'^activity/$', views.activity),
    url(r'^log/$', views.log),
]
handler404 = views.notfound
