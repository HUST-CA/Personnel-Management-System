from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from account.models import Member, Department


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Member
        fields = ('email', 'name', 'tel')

    def clean_password2(self):
        """Check that the two password entries match"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """Save the provided password in hashed format"""
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field."""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Member
        fields = '__all__'

    def clean_password(self):
        """Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the
        field does not have access to the initial value"""
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'tel', 'sex', 'department', 'grade', 'is_admin', 'is_superuser')
    list_filter = ('is_admin', 'sex', 'department', 'grade')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('个人信息(必填)', {'fields': ('name', 'tel')}),
        ('个人信息(选填)', {'fields': ('sex', 'department', 'grade')}),
        ('权限', {'fields': ('is_admin', 'is_superuser')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute.
    # UserAdmin overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'tel', 'password1', 'password2')}
         ),
    )
    search_fields = ('name',)
    ordering = ('email',)
    filter_horizontal = ()


class MemberInline(admin.StackedInline):
    model = Member
    extra = 3


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'leader',)
    inlines = [MemberInline, ]


# Register the new UserAdmin.
admin.site.register(Member, UserAdmin)
# Since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

admin.site.register(Department, DepartmentAdmin)

admin.site.site_header = '人事管理系统'
admin.site.site_title = '人事管理系统'
