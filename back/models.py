from django.db import models
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.validators import FileExtensionValidator
from config.config import MonthNames, excel_file_extension, KeyValue

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
min_len_4 = MinLengthValidator(limit_value=4)
min_len_19 = MinLengthValidator(limit_value=19)


class ShiftGroup(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, unique=True)
    name = models.CharField(max_length=50, validators=[alphanumeric], null=False, blank=False)
    pr_name = models.CharField(max_length=100, null=True, blank=True)
    prefix = models.CharField(max_length=4, validators=[min_len_4])
    owner = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    normal_req = models.IntegerField(verbose_name=KeyValue.normal_req, default=4)
    tuesday_req = models.IntegerField(verbose_name=KeyValue.tuesday_req, default=3)
    thursday_req = models.IntegerField(verbose_name=KeyValue.thursday_req, default=2)
    friday_req = models.IntegerField(verbose_name=KeyValue.friday_req, default=1)
    formally_holiday_req = models.IntegerField(verbose_name=KeyValue.formally_holiday_req, default=1)
    shift_count_limit = models.IntegerField(verbose_name=KeyValue.shift_count_limit, default=5)
    phone_number = models.IntegerField(verbose_name=KeyValue.shift_count_limit, default=9090)

    class Meta:
        permissions = (
            ("can_see_management", "can_see_management"),
            ("can_add_shift_on_page", "can_add_shift_on_page"),
        )

    def __str__(self):
        return str(self.name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default=' ')
    last_name = models.CharField(max_length=30, default=' ')
    group = models.ForeignKey(ShiftGroup, on_delete=models.CASCADE, default=None)
    in_shift = models.BooleanField(default=True)
    in_night_shift = models.BooleanField(default=True)
    in_day_shift = models.BooleanField(default=True)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(default='', blank=True)
    shift_count = models.IntegerField(verbose_name=KeyValue.shift_count, default=0)

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="80" height="80" />' % self.avatar)

    def __str__(self):
        return self.user.username

    def _username(self):
        return self.user.username


class ExcelColumns(models.Model):
    name = models.CharField(max_length=30, default='sample_name')
    columns = models.TextField(default='sample column1|sample_column2|sample column3')

    def column_to_list(self):
        return self.columns.split('|')

    def __str__(self):
        return self.name


class FileObj(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, unique=True)
    month = models.IntegerField(verbose_name=MonthNames.month, choices=MonthNames.JALALI_MONTH_CHOICES, null=True,
                                blank=True)
    year = models.IntegerField(verbose_name=MonthNames.year, choices=MonthNames.JALALI_YEAR_CHOICES, null=True,
                               blank=True)
    group_owner = models.ForeignKey(ShiftGroup, on_delete=models.CASCADE, unique=False)
    storage_path = 'files/excels/'
    shift_number = models.IntegerField(verbose_name=KeyValue.shift_num, null=False, blank=False)
    related_column = models.ForeignKey(ExcelColumns, on_delete=models.CASCADE, unique=False)

    class Meta:
        permissions = (
            ("can_update_file", "can_update_file"),
            ("can_see_file", "can_update_file"),
        )

    def change_filename(self, filename):
        return '%s%s_%s_%s.%s' % (str(self.storage_path), str(self.group_owner.prefix), str(self.year),
                                  str(self.month), excel_file_extension)

    file = models.FileField(upload_to=change_filename, default='',
                            validators=[FileExtensionValidator(allowed_extensions=[excel_file_extension])])

    def __str__(self):
        return str(self.file.name).strip(self.storage_path).strip('.')


class SpecialDay(models.Model):
    group = models.OneToOneField(ShiftGroup, on_delete=models.CASCADE, default=None)
    people_list = models.TextField(default=None)
    back_people_list = models.TextField(default=None)

    class Meta:
        abstract = True  # Set this model as Abstract


class Tuesday(SpecialDay):
    def __str__(self):
        return self.group.name


class Thursday(SpecialDay):
    def __str__(self):
        return self.group.name


class Friday(SpecialDay):
    def __str__(self):
        return self.group.name


class Shift(models.Model):
    j_year_num_first = models.IntegerField(verbose_name=MonthNames.year_first, choices=MonthNames.JALALI_YEAR_CHOICES,
                                           null=True, blank=True)
    j_year_num_last = models.IntegerField(verbose_name=MonthNames.year_last, choices=MonthNames.JALALI_YEAR_CHOICES,
                                          null=True, blank=True)
    j_month_num_first = models.IntegerField(verbose_name=MonthNames.month_first,
                                            choices=MonthNames.JALALI_MONTH_CHOICES, null=True, blank=True)
    j_month_num_last = models.IntegerField(verbose_name=MonthNames.month_last, choices=MonthNames.JALALI_MONTH_CHOICES,
                                           null=True, blank=True)
    j_day_num_first = models.IntegerField(verbose_name=MonthNames.day_first, null=True, blank=True)
    j_day_num_last = models.IntegerField(verbose_name=MonthNames.day_last, null=True, blank=True)
    group = models.ForeignKey(ShiftGroup, on_delete=models.CASCADE, default=None)
    people_list = models.TextField()
    days_count = models.IntegerField()
    days_name = models.TextField()
    formally_holiday_first = models.TextField(blank=True, null=True)
    formally_holiday_last = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{} - {} - {}'.format(str(self.group), str(self.j_year_num_first), str(self.j_month_num_first))


class ShiftDay(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    index_num = models.IntegerField(default=-1)
    j_day_num = models.IntegerField(verbose_name=MonthNames.day, default=-1)
    j_month_num = models.IntegerField(verbose_name=MonthNames.month)
    j_year_num = models.IntegerField(verbose_name=MonthNames.year)
    group = models.ForeignKey(ShiftGroup, on_delete=models.CASCADE)
    night_people_list = models.TextField()
    night_pr_people_list = models.TextField()
    day_people_list = models.TextField(null=True, blank=True)
    day_pr_people_list = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=19, validators=[min_len_19], unique=True)
    is_formally_holiday = models.BooleanField(default=False)
    day_responsible = models.CharField(max_length=30, default=None, null=True)
    night_responsible = models.CharField(max_length=30, default=None, null=True)

    def __str__(self):
        return self.type
