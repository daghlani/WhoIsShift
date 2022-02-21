from django import forms
from config.config import MonthNames, KeyValue
from back.models import FileObj, Shift, ShiftGroup


# from django.core.validators import FileExtensionValidator
# from config.config import excel_file_extension


# class UploadExcelForm(forms.Form):
#     excel_file = forms.FileField(required=True, label='Excel File',
#                                  validators=[FileExtensionValidator(allowed_extensions=[excel_file_extension])])


class DatePickerForm(forms.Form):
    month = forms.IntegerField(label=MonthNames.month, widget=forms.Select(choices=MonthNames.JALALI_MONTH_CHOICES))
    year = forms.IntegerField(label=MonthNames.year, widget=forms.Select(choices=MonthNames.JALALI_YEAR_CHOICES))


class FileEditForm(forms.ModelForm):
    class Meta:
        model = FileObj
        exclude = ('group_owner', 'id',)


class ShiftForm(forms.ModelForm):
    uncommon_holiday = forms.MultipleChoiceField(
        label=KeyValue.uncommon_holiday,
        choices=MonthNames.JALALI_DAY_CHOICES,
        required=False
    )

    # def __init__(self, user=None, **kwargs):
    #     super(ShiftForm, self).__init__(**kwargs)
    #     if user:
    #         self.fields['group'].queryset = ShiftGroup.objects.filter(owner__username=user)

    class Meta:
        model = Shift
        exclude = ('days_count', 'days_name', 'people_list', 'uncommon_holiday', 'group',)


def ShiftForm_factory(username):
    class ShiftForm(forms.ModelForm):
        group = forms.ModelChoiceField(
            queryset=ShiftGroup.objects.filter(owner__username=username)
        )

    return ShiftForm
