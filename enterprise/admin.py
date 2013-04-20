
from django.contrib import admin

from enterprise.models import Universe, Enterprise, ActionRecord, Transaction

admin.site.register(Universe)
admin.site.register(Enterprise)
admin.site.register(ActionRecord)
admin.site.register(Transaction)
