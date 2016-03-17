from django.http.response import HttpResponse

from product_catalog.models import Product

# This function will be called for every request that matches the pattern 
# BASEURL/product/XYZ/ (see mapping in urls.py)
# The part XYZ of the URL will be mapped to the argument id
# Additionally every function called via an incoming HTTP request 
# has a default parameter request that contains information about the request
# We will learn about this later. The function triggered by the request is supposed
# to return a HttpResponse object to the calling client 

def product(request, id):           
        
    # Here we simply query the object with the given ID and return a string representation
    # You can try this by running the server (python manage.py runserver) and then calling 
    # http://localhost:8000/product/123/

    product_name = str(Product.objects.filter(id=id).first())

    return HttpResponse(product_name)