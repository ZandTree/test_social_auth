from django import forms
from django.contrib import admin
from django.contrib.auth.admin import AdminPasswordChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext as _

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
        # ,'is_active','is_admin','groups')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = "Your Email Address"

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password2 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        # othewise password set fails
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Password",
                                         help_text="Raw passwords are not stored, so there is no way to see "
                                                   "this user's password, but you can change the password "
                                                   "using <a href=\"password/\">this form</a>.")

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin', 'groups')

    def clean_password(self):
        return self.initial['password']


class UserAdmin(BaseUserAdmin):
    search_fields = ('email',)
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'is_superuser','is_admin', 'is_active',)
    list_filter = ('is_admin', 'is_active')

    # add key 'classes' with value [collapse ] to toggle Important Dates
    fieldsets = (
        (_('User'), {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_admin', 'is_superuser', 'is_active', 'groups', 'user_permissions',)}),
        (_('Important dates'), {'classes': ['collapse'], 'fields': ('last_login', 'date_joined')}),
        (_('Have fun'), {'fields': ()})
    )

    # for changing a existed user <== UserCreationForm
    add_fieldsets = (
        (('Add Your User'), {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    ordering = ('email',)
    # filter_vertical = ('groups','user_permissions')
    filter_horizontal = ('groups', 'user_permissions')  # for the right widget


admin.site.register(User, UserAdmin)
