from django.contrib import admin

from .models import Message
# Register your models here.



class MessageAdmin(admin.ModelAdmin):
    list_display= ['msg_sender', 'msg_receiver', 'msg']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['msg_sender', 'msg_receiver']

admin.site.register(Message, MessageAdmin)
