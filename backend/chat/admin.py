from django.contrib import admin
from .models import *


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):

    list_display  = ['starter', 'receiver', 'start_time']

# admin.site.register(ConversationAdmin)
admin.site.register(Message)
