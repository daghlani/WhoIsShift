from django.contrib import admin
from back.models import ShiftGroup, FileObj, ExcelColumns, Profile, Shift, Tuesday, Thursday, Friday, ShiftDay
from back.forms import ShiftForm_factory


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
    search_fields = ('user__username', 'group__name', 'in_shift', 'in_night_shift', 'in_day_shift')
    readonly_fields = ('shift_count',)
    list_filter = ('group', 'in_shift', 'shift_count',)

    @admin.display(description='PROFILE IMAGE')
    def image_tag(self, obj):
        return obj.image_tag()


# class ShiftAdmin(admin.ModelAdmin):
#     list_display = ('group', 'j_year_num', 'j_month_num')
#     readonly_fields = ('days_count', 'days_name',)
#     search_fields = list_display
#     list_filter = ('group',)


class ShiftDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'j_year_num', 'j_month_num', 'j_day_num', 'group', 'night_pr_people_list')
    readonly_fields = ('index_num', 'shift', 'group', 'type', 'j_year_num', 'j_month_num', 'j_day_num',)
    search_fields = list_display
    list_filter = ('group', 'type', 'j_year_num', 'j_month_num')


class SpecialDayAdmin(admin.ModelAdmin):
    list_display = ('group', 'people_list')
    readonly_fields = ('group',)


class ShiftAdmin(admin.ModelAdmin):
    list_display = ('group', 'j_year_num_first', 'j_month_num_first',)
    readonly_fields = ('days_count', 'days_name',)
    search_fields = list_display
    list_filter = ('group',)

    # To make limitation for non super users to see only shifts of yourself.
    def get_queryset(self, request):
        qs = super(ShiftAdmin, self).get_queryset(request)
        print(request.user)
        if request.user.is_superuser:
            return qs
        return qs.filter(group=ShiftGroup.objects.get(owner__username=request.user))

    # This is a limitation of choice ShiftGroup when user want to create shift object. (only group of yourself)
    def render_change_form(self, request, context, *args, **kwargs):
        if not kwargs['change']:
            context['adminform'].form.fields['group'].queryset = ShiftGroup.objects.filter(owner__username=request.user)
        return super(ShiftAdmin, self).render_change_form(request, context, *args, **kwargs)


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
