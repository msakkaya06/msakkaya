from django.shortcuts import render

# Create your views here.
def index(req):
    return render(req,'idariburo/idariburo_index.html')

def unit_assignment(req):
    return render(req,'idariburo/idariburo_unit_assignment.html')