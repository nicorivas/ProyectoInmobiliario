from django.contrib import admin

from .models import Building
from .models import Apartment

admin.site.register(Building)
admin.site.register(Apartment)
