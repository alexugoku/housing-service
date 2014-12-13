from django.conf.urls import patterns, include, url

from django.contrib import admin
from accommodations.views import login_view, logout_view, camine, admin_panel

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'accommodations.views.index', name='index'),
    url(r'^camine/$', camine, name='camine'),
    url(r'^admin_panel/$', admin_panel, name='admin_panel'),
    url(r'^$', 'accommodations.views.index', name='camin'),
    url(r'^accounts/login/$', login_view, name='login'),
    url(r'^accounts/logout/$', logout_view, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)
