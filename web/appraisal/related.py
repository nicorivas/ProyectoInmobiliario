import requests
from apartment.models import Apartment
from realestate.models import RealEstate

def getSimilarRealEstate(realestate):

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
        response_results = response_json['results'][0]['geometry']['location']
        realestate.lat = response_results['lat']
        realestate.lng = response_results['lng']
        #realestate.save()

    if realestate.propertyType == RealEstate.TYPE_APARTMENT:
        if (realestate.apartment.bedrooms != None and
            realestate.apartment.bathrooms != None and
            realestate.apartment.usefulSquareMeters != None and
            realestate.apartment.terraceSquareMeters != None):

            apartments = Apartment.objects.filter(
                bedrooms=realestate.apartment.bedrooms,
                bathrooms=realestate.apartment.bathrooms,
                usefulSquareMeters__isnull=False,
                marketPrice__isnull=False).exclude(marketPrice=0)

            ds = []
            ni = 0
            for i, apt in enumerate(apartments):
                d1 = float(pow(realestate.apartment.usefulSquareMeters - apt.usefulSquareMeters,2))
                #d2 = float(pow(realestate.apartment.terraceSquareMeters - apt.terraceSquareMeters,2))
                d3 = float(pow(apt.latlng[0] - realestate.latlng[0],2)+pow(apt.latlng[1] - realestate.latlng[1],2))
                ds.append([0,0])
                ds[i][0] = apt.pk
                ds[i][1] = d1+d3

            ds = sorted(ds, key=lambda x: x[1])
            ins = [x[0] for x in ds]

            references = apartments.filter(pk__in=ins[0:20])
            return references
        else:
            print('a')
            return []
    else:
        print('b')
        return []