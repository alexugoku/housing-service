from django.conf.urls import patterns, include, url

from django.contrib import admin
from accommodations.views import login_view, logout_view

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'accommodations.views.index', name='index'),
    url(r'^$', '', name='cerere'),
    url(r'^$', 'accommodations.views.index', name='camin'),
    url(r'^accounts/login/$', login_view, name='login'),
    url(r'^accounts/logout/$', logout_view, name='logout'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
