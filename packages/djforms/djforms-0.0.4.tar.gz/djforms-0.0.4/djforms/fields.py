
from django.conf import settings
from django.forms import DateField

from djforms.widgets import DatePickerInput


class DatePickerField(DateField):

    widget = DatePickerInput

    input_formats = settings.DATE_INPUT_FORMATS
