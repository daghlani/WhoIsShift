from django.contrib import admin
from back.models import ShiftGroup, FileObj, ExcelColumns, Profile, Shift, Tuesday, Thursday, Friday, ShiftDay
# from  django.contrib.auth.models  import  Group  # new
# #...
# admin.site.unregister(Group)  # new

class FileObjAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'group_owner',)
    readonly_fields = ('id',)


class ShiftGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner',)
    readonly_fields = ('id',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'user', 'group', 'shift_count', 'in_shift', 'in_night_shift', 'in_day_shift')
    search_fields = list_display
    readonly_fields = ('shift_count',)
    list_filter = ('group', 'in_shift','shift_count',)

    @admin.display(description='PROFILE IMAGE')
    def image_tag(self, obj):
        return obj.image_tag()


class ShiftAdmin(admin.ModelAdmin):
    list_display = ('group', 'j_year_num', 'j_month_num')
    readonly_fields = ('days_count', 'days_name',)
    search_fields = list_display
    list_filter = ('group',)


class ShiftDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'j_year_num', 'j_month_num', 'j_day_num', 'group', 'night_people_list')
    readonly_fields = ('index_num', 'shift', 'group', 'type', 'j_year_num', 'j_month_num', 'j_day_num',)
    search_fields = list_display
    list_filter = ('group', 'type', 'j_year_num', 'j_month_num')


class SpecialDayAdmin(admin.ModelAdmin):
    list_display = ('group', 'people_list')
    readonly_fields = ('group',)


# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ShiftGroup, ShiftGroupAdmin)
admin.site.register(FileObj, FileObjAdmin)
admin.site.register(ExcelColumns)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(Tuesday, SpecialDayAdmin)
admin.site.register(Thursday, SpecialDayAdmin)
admin.site.register(Friday, SpecialDayAdmin)
admin.site.register(ShiftDay, ShiftDayAdmin)
