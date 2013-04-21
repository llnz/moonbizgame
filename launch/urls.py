
from django.conf.urls.defaults import *

from django.contrib.auth.decorators import login_required

from launch.views import AvailableLaunchesList, PurchasedLaunchConfigsList, PurchaseLaunchConfig, \
    SellLaunchConfig

urlpatterns = patterns('getclassie.studio.views',
                      
    
    url(r'^(?P<enterprise>[a-zA-Z0-9_-]+)/$', login_required(PurchasedLaunchConfigsList.as_view()), name='launch_purchasedconfigs'),
    url(r'^(?P<enterprise>[a-zA-Z0-9_-]+)/available/$', login_required(AvailableLaunchesList.as_view()), name='launch_available'),
    url(r'^(?P<enterprise>[a-zA-Z0-9_-]+)/(?P<lcid>[0-9]+)/purchase$', login_required(PurchaseLaunchConfig.as_view()), name='launch_purchase_config'),
    url(r'^(?P<enterprise>[a-zA-Z0-9_-]+)/(?P<lcid>[0-9]+)/sell$', login_required(SellLaunchConfig.as_view()), name='launch_sell_config'),

    
    )