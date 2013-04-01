from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import accounts
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'views.home', name='home'),
    # url(r'^decodering/', include('foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include(accounts.urls)),
    url(r'^(?P<code>[^\.]+)/(?P<slug>[^\.]+)', ('articles.views.view_article')),
    url(r'^(?P<code>[^\.]+)/', ('articles.views.view_language')),
    url(r'^', ('articles.views.index')),
)
