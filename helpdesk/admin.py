from django.contrib import admin
from .models import *

admin.site.register(HelpTopic)
admin.site.register(Ticket)
admin.site.register(TicketComment)
admin.site.register(TicketAttachment)
# Register your models here.
