from realestate.models import RealEstate, Asset
from house.models import House
from building.models import Building
from terrain.models import Terrain
#from apartment.models import Apartment
from appraisal.models import Appraisal, Comment, Photo, Document, Rol

def getAppraisalFromRequest(request):

    appraisal = None

    if request.method == "POST":
        request_dictionary = request.POST
    elif request.method == "GET":
        request_dictionary = request.GET
    else:
        return None

    if 'appraisal_id' in request_dictionary:
        try:
            appraisal_id = int(request_dictionary['appraisal_id'])
            try:
                return Appraisal.objects.get(id=appraisal_id)
            except Appraisal.DoesNotExist:
                return None
        except ValueError:
            return None

def getRealEstateFromRequest(request):

    real_estate = None

    if request.method == "POST":
        request_dictionary = request.POST
    elif request.method == "GET":
        request_dictionary = request.GET
    else:
        return None

    if 'real_estate_id' in request_dictionary:
        try:
            real_estate_id = int(request_dictionary['real_estate_id'])
            try:
                return RealEstate.objects.get(id=real_estate_id)
            except RealEstate.DoesNotExist:
                return None
        except ValueError:
            return None

def getPropertyFromRequest(request):

    if request.method == "POST":
        request_dictionary = request.POST
    elif request.method == "GET":
        request_dictionary = request.GET
    else:
        return None

    properti = None
    building = None
    real_estate = None

    if 'property_type' in request_dictionary:
        try:
            property_type = int(request_dictionary['property_type'])
        except ValueError:
            return None
        if property_type == Building.TYPE_TERRENO:
            try:
                property_id = int(request_dictionary['property_id'])
                try:
                    properti = Terrain.objects.get(id=property_id)
                    real_estate = properti.real_estate
                except Terrain.DoesNotExist:
                    return None
            except ValueError:
                return None
        elif property_type == Building.TYPE_CASA:
            try:
                property_id = int(request_dictionary['property_id'])
                try:
                    properti = House.objects.get(id=property_id)
                    building = properti.building
                    real_estate = building.real_estate
                except House.DoesNotExist:
                    return None
            except ValueError:
                return None
    else:

        if 'real_estate_id' in request_dictionary:
            try:
                real_estate_id = int(request_dictionary['real_estate_id'])
                try:
                    real_estate = RealEstate.objects.get(id=real_estate_id)
                except RealEstate.DoesNotExist:
                    return None
            except ValueError:
                return None

    return {
        'property':properti,
        'building':building,
        'real_estate':real_estate
        }