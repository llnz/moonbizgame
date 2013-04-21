
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.http import HttpResponseRedirect

from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.base import View

from moonbizgame import game

from enterprise.models import Enterprise, Universe, ActionRecord, Transaction
from enterprise.forms import EnterpriseAddForm

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
    
class CreateGame(CreateView):
    form_class = EnterpriseAddForm
    template_name='enterprise/create_game.html'
    
    def get_success_url(self):
        return reverse('enterprise_details', kwargs={'enterprise': self.object.slug})
    
    def form_valid(self, form):
        thetime = timezone.now()
        thetime = thetime.replace(hour=0, minute=0, second=0, microsecond=0)
        universe = Universe(current_time=thetime, mode='Arcade')
        universe.save()
        form.instance.universe = universe
        form.instance.created_igt = universe.current_time
        form.instance.mode = "Arcade"
        
        slug = slugify(form.instance.name)
        retry = 1
        while Enterprise.objects.filter(slug=slug).count() != 0:
            slug = slugify(form.instance.name + ' ' + retry)
            retry += 1
        
        form.instance.slug = slug
        
        response = CreateView.form_valid(self, form)
        
        form.instance.owners.add(self.request.user)
        
        action = ActionRecord(enterprise=form.instance, when_igt=universe.current_time,
                              description='Enterprise %s started' % form.instance.name)
        action.save()
        transaction = Transaction(enterprise=form.instance, when_igt=universe.current_time,
                                  details='Initial Investment', 
                                  acc_type='Equity', amount=form.instance.start_cash)
        transaction.save()
        
        game.start_game(form.instance)
        
        return response
    
class EndTurn(EnterpriseContextMixin, View):
    
    def get(self, request, *args, **kwargs):
        game.end_turn(self.enterprise)
        
        return HttpResponseRedirect(reverse('enterprise_details', kwargs={'enterprise': self.enterprise.slug}))

class Portal(ListView):
    template_name='home.html'
    context_object_name = 'enterprises'
    
    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Enterprise.objects.filter(owners=self.request.user).all()
        else:
            return Enterprise.objects.none()
