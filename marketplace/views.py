from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import UserProfile
from .context_processors import get_cart_counter, get_cart_amounts
from service.models import Service, ConsultationItem, Consultation
from orders.forms import OrderForm
from doctors.models import  Doctor, OpeningHour
from django.db.models import Prefetch
from .models import Cart 
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# from django.contrib.gis.geos import GEOSGeometry
# from django.contrib.gis.measure import D # ``D`` is a shortcut for ``Distance``
# from django.contrib.gis.db.models.functions import Distance

from datetime import date, datetime
# from orders.forms import OrderForm


def marketplace(request):
    doctors = Doctor.objects.filter(is_approved=True, user__is_active=True)
    doctor_count = doctors.count()
    context = {
        'doctors': doctors,
        'doctor_count': doctor_count,
    }
    return render(request, 'marketplace/doctor_listings.html', context)


def doctor_detail(request, doctor_slug):
    doctor = get_object_or_404(Doctor, doctor_slug=doctor_slug)

    consultationItems = ConsultationItem.objects.order_by('type__name').filter(owner=doctor, is_available=True)
    

    opening_hours = OpeningHour.objects.filter(doctor=doctor).order_by('day', 'from_hour')
    
    # Check current day's opening hours.
    today_date = date.today()
    today = today_date.isoweekday()
    
    current_opening_hours = OpeningHour.objects.filter(doctor=doctor, day=today)
    if request.user.is_authenticated:
            cart_items = Cart.objects.filter(user=request.user)
    else:
            cart_items = None
    context = {
        'doctor': doctor,
        'consultationItems': consultationItems,
        'cart_items': cart_items,
        'opening_hours': opening_hours,
        'current_opening_hours': current_opening_hours,
    }
    return render(request, 'marketplace/doctor_details.html', context)


def add_to_cart(request, item_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                consultationitem = ConsultationItem.objects.get(id=item_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user,  consultationitem= consultationitem)
                    # Increase the cart sessin
                    chkCart.session += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart session', 'cart_counter': get_cart_counter(request), 'ses': chkCart.session, 'cart_amount': get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user,  consultationitem= consultationitem, session=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the item to the cart', 'cart_counter': get_cart_counter(request), 'ses': chkCart.session, 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


def decrease_cart(request, item_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the  item exists
            try:
                consultationitem = ConsultationItem.objects.get(id=item_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, consultationitem=consultationitem)
                    if chkCart.session > 1:
                        # decrease the cart quantity
                        chkCart.session -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.session = 0
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'ses': chkCart.session, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


@login_required(login_url = 'login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been deleted!', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart Item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})


def search(request):
    # if not 'address' in request.GET:
    #     return redirect('marketplace')
    # else:
    #     address = request.GET['address']
    #     latitude = request.GET['lat']
    #     longitude = request.GET['lng']
    #     radius = request.GET['radius']
    #     keyword = request.GET['keyword']

    #     # get doctor ids that has the  item the user is looking for
    #     fetch_doctors_by_consultationitems = ConsultationItem.objects.filter(type__icontains=keyword, is_available=True).values_list('owner', flat=True)
        
    #     doctors = Doctor.objects.filter(Q(id__in=fetch_doctors_by_consultationitems) | Q(doctor_slug__icontains=keyword, is_approved=True, user__is_active=True))
    #     if latitude and longitude and radius:
    #         pnt = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))

    #         doctors = Doctor.objects.filter(Q(id__in=fetch_doctors_by_consultationitems) | Q(doctor_slug__icontains=keyword, is_approved=True, user__is_active=True),
    #         user_profile__location__distance_lte=(pnt, D(km=radius))
    #         ).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")

    #         for d in doctors:
    #             d.kms = round(d.distance.km, 1)
    #     doctor_count = doctors.count()
    if not 'address' in request.GET:
         return redirect('marketplace')
    else:
        
        location = request.GET['address']
        keyword = request.GET['keyword']
        
        # doctors = Doctor.objects.filter(is_approved=True, user__is_active=True).filter(Q(specialty__name=keyword) | Q(state_of_practice__icontains=location)).distinct()  
        
        doctors = Doctor.objects.filter(is_approved=True, user__is_active=True).filter(Q(specialty__name__icontains=keyword, state_of_practice__icontains=location)).distinct()  
        
        doctors_count = doctors.count() 
        
        print(doctors)  
        context = {
            
            'doctors': doctors,
            'doctors_count':  doctors_count,
                
            }


        return render(request, 'marketplace/search_listings.html', context) #context


@login_required(login_url='login')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    
    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        #'phone': request.user.phone_number,
        'email': request.user.email,
        'address': user_profile.address,
        'country': user_profile.country,
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_code': user_profile.pin_code,
    }
    form = OrderForm(initial=default_values)
    context = {
        'form': form,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/checkout.html', context)