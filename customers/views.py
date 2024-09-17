from django.shortcuts import render
from .models import Province, City, District, Villages
from django.http import JsonResponse

def load_cities(request):
    province = request.POST.get('province')
    cities = City.objects.filter(province_id=province)
    return JsonResponse(list(cities.values('id', 'nama')), safe=False)

def load_districts(request):
    city = request.POST.get('city')
    districts = District.objects.filter(city_id=city)
    return JsonResponse(list(districts.values('id', 'nama')), safe=False)

def load_villages(request):
    district = request.POST.get('district')
    villages = Villages.objects.filter(district_id=district)
    return JsonResponse(list(villages.values('id', 'nama')), safe=False)

