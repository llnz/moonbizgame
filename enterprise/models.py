from django.db import models
from django.utils import timezone

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
    
    def __unicode__(self):
        return '%s - %s - %s - %s' % (self.enterprise.name, self.when_igt, self.details, self.amount)
    
    class Meta:
        ordering = ['-when_irl',]
