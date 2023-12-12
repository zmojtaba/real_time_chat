from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'type', 'email', 'phone', 'is_staff','is_active',"is_verified")
    list_filter = ( 'type', 'email', 'phone', 'is_staff','is_active', 'is_verified')
    search_fields = ('email', 'phone')
    ordering = ('email',)
    fieldsets = (
       ('Authentication',{
           "fields":(
              'username', 'email', 'phone', 'password' 
           ),
       }),
       ('permissions', {
           "fields": (
               'is_staff', 'is_active','is_superuser','is_verified'

           ),
       }),
   )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone' , 'password1','password2', 'is_staff', 'is_active','is_superuser','is_verified')}
         ),
    )

admin.site.register(User,CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(ProfileImage)
admin.site.register(PdfResume)