from django.forms import Form

def now():
    from django.utils import timezone
    # since seconds and microseconds are not important
    # set them to zero for comparison purposes
    return timezone.now().replace(second=0, microsecond=0)

def forms_are_valid(*form: Form):
    # return true if all provided forms have no errors
    forms = list(map(lambda x: x.is_valid(), form))
    return all(forms)