from realestate.models import RealEstate, Asset
from house.models import House
from building.models import Building
from terrain.models import Terrain
#from apartment.models import Apartment
from appraisal.models import Appraisal, Comment, Photo, Document, Rol

def propertyData(rd):

    current = None
    appraisal = None
    if 'appraisal_id' in rd:
        try:
            appraisal_id = int(rd['appraisal_id'])
            try:
                appraisal = Appraisal.objects.get(id=appraisal_id)
            except Appraisal.DoesNotExist:
                appraisal = None
        except ValueError:
            appraisal = None

    real_estate = None
    if 'real_estate_id' in rd:
        try:
            real_estate_id = int(rd['real_estate_id'])
            try:
                real_estate = RealEstate.objects.get(id=real_estate_id)
            except RealEstate.DoesNotExist:
                real_estate = None
        except ValueError:
            real_estate = None

    building = None
    if 'building_id' in rd:
        try:
            building_id = int(rd['building_id'])
            try:
                building = Building.objects.get(id=building_id)
            except Building.DoesNotExist:
                building = None
        except ValueError:
            building = None

    house = None
    apartment = None
    apartment_building = None

    if building:

        if building.propertyType == Building.TYPE_CASA:
            house = building.house
            current = house

        if building.propertyType == Building.TYPE_EDIFICIO:
            apartment_building = building.apartmentbuilding
            if 'apartment_id' in rd:
                try:
                    apartment_id = int(rd['apartment_id'])
                    try:
                        apartment = apartment_building.apartment_set.get(id=apartment_id)
                        current = apartment
                    except:
                        apartment = None
                        current = apartment_building
                except ValueError:
                    apartment = None
                    current = apartment_building
            else:
                apartment = None
                current = apartment_building
        else:
            apartment_building = None

    terrain = None
    if 'terrain_id' in rd and real_estate:
        try:
            terrain_id = int(rd['terrain_id'])
            try:
                terrain = real_estate.terrains.get(id=terrain_id)
                current = terrain
            except Terrain.DoesNotExist:
                terrain = None
        except ValueError:
            terrain = None  

    selected = None
    terrain_selected = None
    if terrain and 'property_selected_id' in rd:
        try:
            terrain_selected_id = int(rd['property_selected_id'])
            try:
                terrain_selected = terrain.terrain_set.get(id=terrain_selected_id)
                selected = terrain_selected
            except Terrain.DoesNotExist:
                terrain_selected = None
        except ValueError:
            terrain_selected = None

    building_selected = None
    house_selected = None
    if house and 'property_selected_id' in rd:
        try:
            house_selected_id = int(rd['property_selected_id'])
            try:
                house_selected = house.house_set.get(id=house_selected_id)
                selected = house_selected
                building_selected = house_selected.building
            except Terrain.DoesNotExist:
                house_selected = None
        except ValueError:
            house_selected = None

    apartment_building_selected = None
    if apartment_building and not apartment and 'property_selected_id' in rd:
        try:
            apartment_building_selected_id = int(rd['property_selected_id'])
            try:
                apartment_building_selected = apartment_building.apartmentbuilding_set.get(id=apartment_building_selected_id)
                selected = apartment_building_selected
                building_selected = apartment_building_selected.building
            except Terrain.DoesNotExist:
                apartment_building_selected = None
        except ValueError:
            apartment_building_selected = None

    apartment_selected = None
    if apartment and 'property_selected_id' in rd:
        try:
            apartment_selected_id = int(rd['property_selected_id'])
            try:
                apartment_selected = apartment.apartment_set.get(id=apartment_selected_id)
                selected = apartment_selected
                building_selected = apartment_selected.apartment_building.building
            except Terrain.DoesNotExist:
                apartment_selected = None
        except ValueError:
            apartment_selected = None

    return {
        'appraisal':appraisal,
        'real_estate':real_estate,
        'building':building,
        'house':house,
        'apartment_building':apartment_building,
        'apartment':apartment,
        'terrain':terrain,
        'current':current,
        'terrain_selected':terrain_selected,
        'building_selected':building_selected,
        'house_selected':house_selected,
        'apartment_building_selected':apartment_building_selected,
        'apartment_selected':apartment_selected,
        'selected':selected
        }