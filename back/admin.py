from django.contrib import admin
from back.models import ShiftGroup, FileObj, ExcelColumns, Profile, Shift


class FileObjAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'group_owner',)
    readonly_fields = ('id',)


class ShiftGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner',)
    readonly_fields = ('id',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'in_shift', 'in_night_shift', 'in_day_shift')
    search_fields = list_display
    list_filter = ('group', 'in_shift',)


class ShiftAdmin(admin.ModelAdmin):
    list_display = ('group', 'j_year_num', 'j_month_num')
    readonly_fields = ('days_count', 'days_name',)
    search_fields = list_display
    list_filter = ('group',)


# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ShiftGroup, ShiftGroupAdmin)
admin.site.register(FileObj, FileObjAdmin)
admin.site.register(ExcelColumns)
admin.site.register(Shift, ShiftAdmin)
