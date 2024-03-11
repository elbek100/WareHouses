from django.contrib import admin

from warehouses.models import *

admin.site.register((Product, ProductMaterials, WareHouses, Materials))
