from django.contrib import admin
from . import models

# Here we register the Product data model with the django site 
admin.site.register(models.Product)
