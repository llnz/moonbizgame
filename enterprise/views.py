
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from django.views.generic import DetailView, ListView

from enterprise.models import Enterprise

class EnterpriseDetail(DetailView):
    context_object_name = 'enterprise'
    
    def get_object(self):
        enterprise = get_object_or_404(Enterprise, slug=self.kwargs['enterprise'], owners=self.request.user)
        return enterprise

    def get_context_data(self, **kwargs):
        context = DetailView.get_context_data(self, **kwargs)
        
        context['recent_actions'] = self.object.actionrecord_set.all()[:5]
        context['recent_transactions'] = self.object.transaction_set.all()[:5]
        
        return context

class EnterpriseContextMixin(object):
    enterprise = None
    
    def dispatch(self, request, *args, **kwargs):
        self.enterprise = get_object_or_404(Enterprise, slug=self.kwargs['enterprise'], owners=self.request.user)
        return super(EnterpriseContextMixin, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(EnterpriseContextMixin, self).get_context_data(**kwargs)
        context['enterprise'] = self.enterprise
        return context

class ActionList(EnterpriseContextMixin, ListView):
    context_object_name = 'actions'
    
    def get_queryset(self):
        return self.enterprise.actionrecord_set.all()
    
class TransactionList(EnterpriseContextMixin, ListView):
    context_object_name = 'transactions'
    
    def get_queryset(self):
        return self.enterprise.transaction_set.all()
    