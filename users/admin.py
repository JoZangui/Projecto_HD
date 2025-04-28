from django.contrib import admin

from .models import Agents

admin.site.site_header = "Agente Admin"
admin.site.site_title = "Agente Admin Portal"
admin.site.index_title = "Welcome to the Agente Admin Portal"
admin.site.register(Agents)
