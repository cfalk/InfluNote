from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'InfluNote.views.content_page', {"content":"home"}),
    url(r'^search/?$', 'InfluNote.views.search_song'),
)
