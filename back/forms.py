from django import forms
from config.config import MonthNames, KeyValue
from back.models import FileObj, Shift, ShiftGroup
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Fieldset


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for visible in self.visible_fields():
        #     print(visible.field.widget.attrs)
        #     visible.field.widget.attrs['class'] = 'test-class'
        #     print(visible.field.widget.attrs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('j_month_num', css_class='form-group col-md-3 mb-0'),
                Column('j_year_num', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
                ),
            Row(
                Column('uncommon_holiday', css_class='form-group'),

                css_class='form-row'),
            Submit('submit', KeyValue.submit, css_class='form-row form-btn col-md-5 mt-2'),
        )
        self.helper.layout.css_class = 'test'


def ShiftForm_factory(username):
    class ShiftForm(forms.ModelForm):
        group = forms.ModelChoiceField(
            queryset=ShiftGroup.objects.filter(owner__username=username)
        )

    return ShiftForm
