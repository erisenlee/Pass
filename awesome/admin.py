from django.contrib import admin
from .models import Account,Tag
# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'description', 'display_tag', 'user','is_active','created_at',)
    list_filter = ('is_active','created_at')
    date_hierarchy = 'created_at'
    empty_value_display = '???'
    
    

class TagAdmin(admin.ModelAdmin):
    list_display = ('name','is_active','created_at')
    list_filter = ('is_active','created_at')


admin.site.register(Account, AccountAdmin)
admin.site.register(Tag, TagAdmin)
