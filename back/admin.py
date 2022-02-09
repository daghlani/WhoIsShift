from django.contrib import admin
from back.models import ShiftGroup, FileObj, ExcelColumns


class FileObjAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'group_owner',)
    readonly_fields = ('id',)


class ShiftGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner',)
    readonly_fields = ('id',)


# Register your models here.
admin.site.register(ShiftGroup, ShiftGroupAdmin)
admin.site.register(FileObj, FileObjAdmin)
admin.site.register(ExcelColumns)
