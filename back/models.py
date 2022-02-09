from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.validators import FileExtensionValidator
from config.config import MonthNames, excel_file_extension, KeyValue

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class ShiftGroup(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, unique=True)
    name = models.CharField(max_length=50, validators=[alphanumeric], null=False, blank=False)
    pr_name = models.CharField(max_length=100, null=True, blank=True)
    prefix = models.CharField(max_length=4)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.name


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
