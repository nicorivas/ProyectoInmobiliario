import requests
from apartment.models import Apartment
from house.models import House
from realestate.models import RealEstate
from building.models import Building
from apartmentbuilding.models import ApartmentBuilding

def getSimilarRealEstate(request):

    print(request.GET)
    realestate = RealEstate.objects.get(id=request.GET['real_estate_id'])

    building = Building.objects.get(id=request.GET['building_id'])

    if (realestate.lng == 0.0 or realestate.lat == 0.0):
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        url_address = '?address={} {}, {}, {}'.format(
            realestate.addressStreet,
            realestate.addressNumber,
            realestate.addressCommune,
            realestate.addressRegion)
        url_key = '&key=AIzaSyDgwKrK7tfcd9kCtS9RKSBsM5wYkTuuc7E'
        response = requests.get(url+''+url_address+''+url_key)
        response_json = response.json()
        if len(response_json['results']) > 0:
            response_results = response_json['results'][0]['geometry']['location']
            realestate.lat = response_results['lat']
            realestate.lng = response_results['lng']
        realestate.save()

    if 'apartment_id' in request.GET:
        if request.GET['apartment_id'] != '':
            apartment_building = ApartmentBuilding.objects.get(id=request.GET['apartment_building_id'])
            apartment = Apartment.objects.get(id=request.GET['apartment_id'])
            if (apartment.bedrooms != None and
                apartment.bathrooms != None and
                apartment.usefulSquareMeters != None and
                apartment.terraceSquareMeters != None):

                apartments = Apartment.objects.filter(
                    bedrooms=realestate.apartment.bedrooms,
                    bathrooms=realestate.apartment.bathrooms,
                    usefulSquareMeters__isnull=False,
                    terraceSquareMeters__isnull=False,
                    marketPrice__isnull=False).exclude(marketPrice=0)

                ds = []
                ni = 0
                for i, apt in enumerate(apartments):
                    d1 = float(pow(apartment.usefulSquareMeters - apt.usefulSquareMeters,2))
                    d2 = float(pow(apartment.terraceSquareMeters - apt.terraceSquareMeters,2))
                    d3 = float(pow(apt.latlng[0] - realestate.latlng[0],2)+pow(apt.latlng[1] - realestate.latlng[1],2))
                    ds.append([0,0])
                    ds[i][0] = apt.pk
                    ds[i][1] = d1+d2+d3

                ds = sorted(ds, key=lambda x: x[1])
                ins = [x[0] for x in ds]

                references = apartments.filter(pk__in=ins[0:20])
                return references
            else:
                print('nada')
                return []
    elif 'house_id' in request.GET:
        if request.GET['house_id'] != '':
            house = House.objects.get(id=request.GET['house_id'])
            house.bathrooms=3
            house.bedrooms=4
            house.builtSquareMeters=89
            house.terrainSquareMeters=90
            house.save
            if (house.bedrooms != None and
                house.bathrooms != None and
                house.builtSquareMeters != None and
                house.terrainSquareMeters != None):

                houses = House.objects.filter(
                    bedrooms=house.bedrooms,
                    bathrooms=house.bathrooms,
                    builtSquareMeters__isnull=False,
                    terrainSquareMeters__isnull=False,
                    marketPrice__isnull=False)

                ds = []
                ni = 0
                print(houses)
                for i, hs in enumerate(houses):
                    #o_price_per_terrain_surface = realestate.house.marketPrice/realestate.house.terrainSquareMeters
                    #o_price_per_total_surface = realestate.house.marketPrice/realestate.totalSquareMeters
                    #i_price_per_terrain_surface = house.marketPrice/house.terrainSquareMeters
                    #i_price_per_total_surface = house.marketPrice/house.realestate_ptr.totalSquareMeters
                    #f1 = float(pow(o_price_per_terrain_surface-i_price_per_terrain_surface,2))
                    #f2 = float(pow(o_price_per_total_surface-i_price_per_total_surface,2))

                    d1 = float(pow(house.terrainSquareMeters - hs.terrainSquareMeters,2))
                    d2 = float(pow(house.builtSquareMeters - hs.builtSquareMeters,2))
                    d3 = 1000000000.0*float(pow(hs.building.real_estate.latlng[0] - realestate.latlng[0],2)
                                            +pow(hs.building.real_estate.latlng[1] - realestate.latlng[1],2))

                    ds.append([0,0])
                    ds[i][0] = hs.pk
                    ds[i][1] = d1+d2+d3
                ds = sorted(ds, key=lambda x: x[1])
                ins = [x[0] for x in ds]

                references = houses.filter(pk__in=ins[0:20])
                return references
            else:
                print('nothing')
                return []
        else:
            return []