
from django.conf.urls.defaults import *

from django.contrib.auth.decorators import login_required

from enterprise.views import EnterpriseDetail, ActionList, TransactionList, CreateGame

urlpatterns = patterns('getclassie.studio.views',
                      
    url(r'^start$', login_required(CreateGame.as_view()), name='enterprise_start_game'),
    url(r'^(?P<enterprise>[a-zA-Z0-9_-]+)/$', login_required(EnterpriseDetail.as_view()), name='enterprise_details'),
    url(r'^(?P<enterprise>[a-zA-Z0-9_-]+)/actions/$', login_required(ActionList.as_view()), name='enterprise_action_log'),
    url(r'^(?P<enterprise>[a-zA-Z0-9_-]+)/transactions/$', login_required(TransactionList.as_view()), name='enterprise_transaction_log'),

    
    )