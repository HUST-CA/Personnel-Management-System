from django.contrib import admin

from .models import NewMember


class NewMemberAdmin(admin.ModelAdmin):
    list_filter = ('sex',)
    fieldsets = (
        ('个人信息', {'fields': ('name', 'sex', 'college', 'dormitory')}),
        ('联系方式', {'fields': ('tel', 'email')}),
        ('部门&自我介绍', {'fields': ('department', 'introduction')}),
    )
    search_fields = ('name',)
    filter_horizontal = ()

admin.site.register(NewMember, NewMemberAdmin)
