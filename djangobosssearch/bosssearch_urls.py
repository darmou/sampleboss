'''
URL patterns for the search and search results page.
'''

from django.conf.urls import patterns, url, include

urlpatterns = patterns('djangobosssearch.views',
    url(r'^$', 'bosssearch', name='bosssearch')
)
