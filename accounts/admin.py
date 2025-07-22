from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('mobile',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('mobile',)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('mobile', 'is_active', 'is_trial', 'is_paid')
    list_filter = ('is_active', 'is_trial', 'is_paid')
    
    fieldsets = (
        (None, {'fields': ('mobile',)}),
        ('Status Info', {'fields': ('is_active', 'is_trial', 'is_paid')}),
        ('Dates', {'fields': ('trial_expires_at', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'is_active')}
        ),
    )
    search_fields = ('mobile',)
    ordering = ('mobile',)

admin.site.register(CustomUser, CustomUserAdmin)
