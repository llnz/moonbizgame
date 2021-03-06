from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from enterprise.views import Portal

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'moonbizgame.views.home', name='home'),
    # url(r'^moonbizgame/', include('moonbizgame.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    (r'^browserid/', include('django_browserid.urls')),
    
    url(r'^$', Portal.as_view(), name='home'),
    url(r'^credits$', TemplateView.as_view(template_name='credits.html'), name='credits'),
    
    url(r'^enterprise/', include('enterprise.urls')),
    url(r'^launch/', include('launch.urls')),
    
    
)
