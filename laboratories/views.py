from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from .models import Laboratory, Service, Branch 

# Create your views here.
def laboratory(request):
    
    laboratories = Laboratory.objects.all()
    laboratory_count = laboratories.count()
    context = {
        'laboratories':   laboratories,
        'laboratory_count': laboratory_count,
    }
    return render(request, 'laboratory/laboratory_listings.html', context)


def laboratory_detail(request, pk=None):
    
    laboratory = get_object_or_404(Laboratory, pk=pk)
            
    context = {
        'laboratory': laboratory
    }
    return render(request, 'laboratory/laboratory_details.html', context)
