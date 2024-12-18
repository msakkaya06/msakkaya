from tunbisapp.models import Unit

def get_select_units(request):
    units = Unit.objects.filter(super_unit=True)
    return {'select_units': units}