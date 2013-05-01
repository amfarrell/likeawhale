from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'views.home', name='home'),
    # url(r'^decodering/', include('foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:

    # Uncomment the next line to enable the admin:
#    url(r'^login/', views.log_in),
#    url(r'^log_in/', views.log_in),
    url(r'^has_seen/', views.has_seen),
    url(r'^has_translated/', views.has_translated),
    url(r'^pretest/', views.pretest),
#    url(r'^', views.log_in),
) 
