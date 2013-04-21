from django.db import models

class Launch(models.Model):
    universe = models.ForeignKey('enterprise.Universe')
    company = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    when_igt = models.DateTimeField(db_index=True)
    
    class Meta:
        ordering = ['when_igt',]
    
    def can_purchase_config(self, chosen_config):
        '''Can purchase a config
        
        Checks to see if possible, returns true if possible
        '''
        for config in self.launchconfig_set.filter(sold=True).all():
            if config.id == chosen_config.id:
                continue
            if config.config_group != chosen_config.config_group:
                return False
        
        return True
    
    def available_configs(self):
        purchased_configs = self.launchconfig_set.filter(sold=True).order_by('config_group', 'config_position').all()[:1]
        if len(purchased_configs):
            return self.launchconfig_set.filter(config_group=purchased_configs[0].config_group).all()
        return self.launchconfig_set.all()
    
    def __unicode__(self):
        return u'%s %s on %s (%s)' % (self.company, self.product, self.when_igt, self.universe)
    
class LaunchConfig(models.Model):
    launch = models.ForeignKey(Launch)
    config_group = models.IntegerField()
    config_position = models.IntegerField()
    destination = models.CharField(max_length=200)
    max_mass = models.IntegerField()
    price = models.IntegerField()
    sold = models.BooleanField(default=False)
    purchaser = models.ForeignKey('enterprise.Enterprise', blank=True, null=True, db_index=True)
    
    def __unicode__(self):
        return u'Launch %s, dest: %s (%s, %s)' % (self.launch, self.destination, 
                                                  self.config_group, self.config_position)
    

