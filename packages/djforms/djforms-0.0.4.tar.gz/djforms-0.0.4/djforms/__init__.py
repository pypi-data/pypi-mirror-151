
from django.forms import ValidationError


def setup_settings(settings, is_prod, **kwargs):

    settings['INSTALLED_APPS'] += [
        app for app in [
            'widget_tweaks',
            'crispy_forms',
            'django_select2'
        ] if app not in settings['INSTALLED_APPS']
    ]


def get_clean_data(django_form):
    validate_form(django_form)
    return django_form.cleaned_data


def validate_form(django_form):
    if not django_form.is_valid():
        raise ArgumentValidationError(django_form)


class ArgumentValidationError(ValidationError):

    def __init__(self, form):
        self._form = form
        super(ArgumentValidationError, self).__init__(form.errors)

    @property
    def form(self):
        return self._form

    def __str__(self):
        return self.form.errors.as_text()
