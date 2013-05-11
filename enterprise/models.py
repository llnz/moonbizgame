from django.db import models
from django.utils import timezone
from django.core.cache import cache

class Universe(models.Model):
    '''This is a universe in the game
    
    It can be shared by many players'''
    
    current_time = models.DateTimeField()
    mode = models.CharField(max_length=50)
    
    def __unicode__(self):
        return u'Universe %s (%s)' % (self.id, self.mode)
    

class Enterprise(models.Model):
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    owners = models.ManyToManyField('auth.User')
    
    created_irl = models.DateTimeField(default=timezone.now)
    created_igt = models.DateTimeField()
    mode = models.CharField(max_length=50)
    start_cash = models.IntegerField()
    
    universe = models.ForeignKey(Universe)
    
    def add_transaction(self, amount, details, acc_type):
        curr_balance = self.get_balance()
        new_balance = curr_balance + amount
        transaction = Transaction(enterprise=self, when_igt=self.universe.current_time, 
                                  amount=amount, details=details, 
                                  acc_type=acc_type, balance=new_balance)
        transaction.save()
        
        #set cache
        cache.set("balance-%s" % self.id, new_balance)
        
    def get_balance(self):
        
        key = "balance-%s" % self.id
        #get from cache
        balance = cache.get(key)
        
        #else
        if balance is None:
            try:
                balance = self.transaction_set.all()[0].balance
            except KeyError:
                balance = 0
            #set cache
            cache.set(key, balance)
        
        return balance
    
    def __unicode__(self):
        return self.name
    
class ActionRecord(models.Model):
    enterprise = models.ForeignKey(Enterprise)
    when_igt = models.DateTimeField()
    when_irl = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    
    def __unicode__(self):
        return '%s - %s - %s' % (self.enterprise.name, self.when_igt, self.description)
    
    class Meta:
        ordering = ['-when_irl',]
    
class Transaction(models.Model):
    enterprise = models.ForeignKey(Enterprise)
    when_igt = models.DateTimeField()
    when_irl = models.DateTimeField(default=timezone.now)
    amount = models.IntegerField()
    details = models.CharField(max_length=200)
    acc_type = models.CharField(max_length=50)
    balance = models.IntegerField()
    
    def __unicode__(self):
        return '%s - %s - %s - %s' % (self.enterprise.name, self.when_igt, self.details, self.amount)
    
    class Meta:
        ordering = ['-when_irl',]
