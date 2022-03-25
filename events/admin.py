from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import Application


class ApplicationCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = Application
        fields = ("name",)

    def clean_password2(self) -> str:
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True) -> Application:
        # Save the provided password in hashed format
        application = super().save(commit=False)
        application.set_password(self.cleaned_data["password1"])
        if commit:
            application.save()
        return application


class ChangeApplicationForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Application
        fields = ("name", "password", "is_active", "is_admin")


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = ApplicationCreationForm
    add_form = ChangeApplicationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("name", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        (None, {"fields": ("name", "password")}),
        ("Permissions", {"fields": ("is_admin",)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("name", "password1", "password2"),
            },
        ),
    )
    search_fields = ("name",)
    ordering = ("name",)
    filter_horizontal = ()


admin.site.register(Application, UserAdmin)
admin.site.unregister(Group)
