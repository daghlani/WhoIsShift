from django import forms
from config.config import MonthNames
from back.models import FileObj


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
