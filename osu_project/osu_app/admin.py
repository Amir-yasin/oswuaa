from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import * 

# Register your models here.



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['first_name','last_name','username','phone_number', 'email', 'user_type','gender']
    search_fields = ['username','email', 'phone_number']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type','gender',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type','gender',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SP_Profile)
admin.site.register(ST_Profile)
admin.site.register(Category)


