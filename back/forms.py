from django import forms
from config.config import MonthNames, KeyValue
from back.models import FileObj, Shift, ShiftGroup
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Fieldset, Div
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# from django.core.validators import FileExtensionValidator
# from config.config import excel_file_extension


# class UploadExcelForm(forms.Form):
#     excel_file = forms.FileField(required=True, label='Excel File',
#                                  validators=[FileExtensionValidator(allowed_extensions=[excel_file_extension])])


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = KeyValue.username
        self.fields['password1'].label = KeyValue.password1
        self.fields['password2'].label = KeyValue.password2

    first_name = forms.CharField(label=KeyValue.first_name, max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(label=KeyValue.last_name, max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(label=KeyValue.email, max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class ProfileForm(forms.Form):
    group = forms.ModelChoiceField(label=KeyValue.group, queryset=ShiftGroup.objects.all(),
                                   required=True)
    in_shift = forms.BooleanField(label=KeyValue.in_shift, required=False, initial=True)


class DatePickerForm(forms.Form):
    month = forms.IntegerField(label=MonthNames.month, widget=forms.Select(
        choices=MonthNames.JALALI_MONTH_CHOICES, attrs={'class': 'month_field form-select-sm'}))
    year = forms.IntegerField(label=MonthNames.year, widget=forms.Select(choices=MonthNames.JALALI_YEAR_CHOICES, attrs={
        'class': 'year_field form-select-sm'}))


class FileEditForm(forms.ModelForm):
    class Meta:
        model = FileObj
        exclude = ('group_owner', 'id',)


class ShiftForm0(forms.ModelForm):
    formally_holiday_first = forms.MultipleChoiceField(
        label=KeyValue.formally_holiday,
        choices=MonthNames.JALALI_DAY_CHOICES,
        required=False
    )
    formally_holiday_last = forms.MultipleChoiceField(
        label=KeyValue.formally_holiday,
        choices=MonthNames.JALALI_DAY_CHOICES,
        required=False
    )

    # dat = forms.DateField(
    #     widget=forms.TextInput(
    #         attrs={'type': 'date'}
    #     )
    # )

    # def __init__(self, user=None, **kwargs):
    #     super(ShiftForm, self).__init__(**kwargs)
    #     if user:
    #         self.fields['group'].queryset = ShiftGroup.objects.filter(owner__username=user)

    class Meta:
        model = Shift
        exclude = (
            'days_count', 'days_name', 'people_list', 'formally_holiday_first', 'formally_holiday_last', 'group',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for visible in self.visible_fields():
        #     print(visible.field.widget.attrs)
        #     visible.field.widget.attrs['class'] = 'test-class'
        #     print(visible.field.widget.attrs)

        self.helper = FormHelper()
        # self.helper.layout = Layout(
        #     Row(
        #         Column('j_year_num_first', css_class='form-group col-md-3 mb-0'),
        #         Column('j_year_num_last', css_class='form-group col-md-3 mb-0'),
        #         css_class='form-row'
        #         ),
        #     Row(
        #         Column('j_month_num_first', css_class='form-group col-md-3 mb-0'),
        #         Column('j_month_num_last', css_class='form-group col-md-3 mb-0'),
        #         css_class='form-row'
        #     ),
        #     Row(
        #         Column('j_day_num_first', css_class='form-group col-md-3 mb-0'),
        #         Column('j_day_num_last', css_class='form-group col-md-3 mb-0'),
        #         css_class='form-row'
        #     ),
        #     Row(
        #         Column('formally_holiday_first', css_class='form-group'),
        #         Column('formally_holiday_last', css_class='form-group'),
        #
        #         css_class='form-row'),
        #     Submit('submit', KeyValue.submit, css_class='form-row form-btn col-md-5 mt-2'),
        # )
        self.helper.layout = Layout(
            Row(
                Column('j_year_num_first', css_class='form-group col-md-1 mb-0'),
                Column('j_month_num_first', css_class='form-group col-md-1 mb-0'),
                Column('j_day_num_first', css_class='form-group col-md-1 mb-0'),
                Column('formally_holiday_first', css_class='form-group '),
                # Column('formally_holiday_first', css_class='form-group-formally'),

                css_class='form-row'
            ),
            Row(
                Column('j_year_num_last', css_class='form-group col-md-2 mb-0'),
                Column('j_month_num_last', css_class='form-group col-md-2 mb-0'),
                Column('j_day_num_last', css_class='form-group col-md-2 mb-0'),
                Column('formally_holiday_last', css_class='form-group col-md-6'),
                # Column('dat', css_class='form-group col-md-6'),

                css_class='form-row'
            ),
            Submit('submit', KeyValue.submit, css_class='form-row form-btn col-md-5 mt-2'),
        )
        self.helper.layout.css_class = 'test'


def ShiftForm_factory(username):
    class ShiftForm(forms.ModelForm):
        group = forms.ModelChoiceField(
            queryset=ShiftGroup.objects.filter(owner__username=username)
        )

    return ShiftForm


class ShiftForm(forms.ModelForm):
    formally_holiday_first = forms.MultipleChoiceField(
        label=KeyValue.formally_holiday,
        choices=MonthNames.JALALI_DAY_CHOICES,
        required=False
    )
    formally_holiday_last = forms.MultipleChoiceField(
        label=KeyValue.formally_holiday,
        choices=MonthNames.JALALI_DAY_CHOICES,
        required=False
    )

    start_date = JalaliDateField(label=KeyValue.start_date,
                                 widget=AdminJalaliDateWidget(attrs={'placeholder': '1400-12-21'}))
    end_date = JalaliDateField(label=KeyValue.end_date,
                               widget=AdminJalaliDateWidget(attrs={'placeholder': '1401-01-21'}))

    class Meta:
        model = Shift
        exclude = (
            'days_count', 'days_name', 'people_list', 'formally_holiday_first', 'formally_holiday_last', 'group',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('start_date', css_class='form-group col-md-1 mb-0'),
                Column('end_date', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('formally_holiday_first', css_class='form-group '),
                Column('formally_holiday_last', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Submit('submit', KeyValue.submit, css_class='form-row form-btn col-md-5 mt-2'),
        )
        self.helper.layout.css_class = 'test'

# class testForm(forms.Form):
#     dat = JalaliDateField(label='date',  # date format is  "yyyy-mm-dd"
#                     widget=AdminJalaliDateWidget  # optional, to use default datepicker
#                     )
