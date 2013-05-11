
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from django.views.generic import DetailView, ListView

from launch.models import Launch, LaunchConfig
from enterprise.views import EnterpriseContextMixin
from enterprise.models import ActionRecord, Transaction
from django.http import Http404, HttpResponseRedirect
import random

class AvailableLaunchesList(EnterpriseContextMixin, ListView):
    context_object_name = 'launches'
    template_name = 'launch/availablelaunches_list.html'
    
    def get_queryset(self):
        universe = self.enterprise.universe
        return Launch.objects.filter(universe=universe, when_igt__gt=universe.current_time).all()
    
    
class PurchasedLaunchConfigsList(EnterpriseContextMixin, ListView):
    context_object_name = 'launchconfigs'
    template_name = 'launch/purchasedlaunches_list.html'
    
    def get_queryset(self):
        return LaunchConfig.objects.filter(purchaser=self.enterprise).all()
    
class PurchaseLaunchConfig(EnterpriseContextMixin, DetailView):
    context_object_name = 'launchconfig'
    template_name = 'launch/config_purchase.html'
    
    def get_object(self, queryset=None):
        lcobj = get_object_or_404(LaunchConfig, launch__universe=self.enterprise.universe, 
                                 id=int(self.kwargs['lcid']), sold=False)
        if not lcobj.launch.can_purchase_config(lcobj):
            raise Http404()
        
        return lcobj
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        self.object.sold = True
        self.object.purchaser = self.enterprise
        self.object.save()
        
        action = ActionRecord(enterprise=self.enterprise, when_igt=self.enterprise.universe.current_time,
                              description='Purchased launch of %s kg to %s on a %s %s at %s for %s' % (
                                                        self.object.max_mass, self.object.destination,
                                                        self.object.launch.company, 
                                                        self.object.launch.product, 
                                                        self.object.launch.when_igt, self.object.price))
        action.save()
        self.enterprise.add_transaction(details='Purchase of launch on %s' % self.object.launch.when_igt, 
                                  acc_type='Expense', amount=-self.object.price)
        
        
        return HttpResponseRedirect(reverse('launch_purchasedconfigs', 
                                            kwargs={'enterprise': self.enterprise.slug}))
    
class SellLaunchConfig(EnterpriseContextMixin, DetailView):
    context_object_name = 'launchconfig'
    template_name = 'launch/config_sell.html'
    
    def get_object(self, queryset=None):
        lcobj = get_object_or_404(LaunchConfig, launch__universe=self.enterprise.universe, 
                                 id=int(self.kwargs['lcid']), sold=True, purchaser=self.enterprise)
        if not lcobj.launch.can_purchase_config(lcobj):
            raise Http404()
        
        return lcobj
    
    def get_context_data(self, **kwargs):
        context = EnterpriseContextMixin.get_context_data(self, **kwargs)
        
        price = int(self.object.price * (0.6 
                                         + 0.1 * random.random() 
                                         + 0.035 * min(10, (self.object.launch.when_igt - self.enterprise.universe.current_time).days)
                                         + 0.25 * random.random() * max(0, 2 - (self.object.launch.when_igt - self.enterprise.universe.current_time).days)))
        context['price'] = price
        price_name = 'launchconfig-%s-offer' % self.object.id
        self.request.session[price_name] = price
        
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        price_name = 'launchconfig-%s-offer' % self.object.id
        price = int(request.session.get(price_name, 1))
        
        self.object.sold = True
        self.object.purchaser = None
        self.object.save()
        
        action = ActionRecord(enterprise=self.enterprise, when_igt=self.enterprise.universe.current_time,
                              description='Sold launch of %s kg to %s on a %s %s at %s for %s' % (
                                                        self.object.max_mass, self.object.destination,
                                                        self.object.launch.company, 
                                                        self.object.launch.product, 
                                                        self.object.launch.when_igt, price))
        action.save()
        self.enterprise.add_transaction(details='Sale of launch on %s' % self.object.launch.when_igt, 
                                  acc_type='Sale', amount=price)
        
        return HttpResponseRedirect(reverse('launch_purchasedconfigs', 
                                            kwargs={'enterprise': self.enterprise.slug}))
    