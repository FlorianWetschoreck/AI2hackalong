from django.http.response import HttpResponse

from product_catalog.models import Product

# Considering the classical Model-View-Controller pattern as presented in lecture 02, 
# you may find the contents of the file views.py in the django framework a bit confusing.
# The functions in this file handle the requests of users, possibly accessing 
# data from the data model (in models.py) and generating a web page to be sent to the client as a response.
# While the latter part naturally maps to the common understanding of the View component, the actual logic of 
# what happens when a request is made is actually implemented here as well, although we would usually associate
# this with the Controller component in the MVC pattern.

# The name views.py is nevertheless justified because here we determine what view is to be presented to the user. 
# The actual generation of the content to be sent as a response can either be done manually (see simple example below) 
# or we can use django's  sophisticated template mechanism (we will explain this in a later hackathon). 

# Since in django the controller is effectively integrated in the views.py, while templates are mostly used to generate 
# the actual user interface, django's specific flavor of the MVC architectural pattern is sometimes called 
# Model-Template-View (MTV), see the explanation of this in the FAQ here:
# https://docs.djangoproject.com/en/1.9/faq/general/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view-and-the-view-the-template-how-come-you-don-t-use-the-standard-names

# So, how does this work in our concrete example?

# We want to generate a product page for a given product ID. This is done by the 
# following function which will be called for every request that matches the pattern 
# BASEURL/product/XYZ/ (see the corresponding expression in urls.py)

# The part XYZ of the URL will be mapped to the argument id
# Every function that is called as a result of an incoming HTTP request
# has a default parameter request that contains information about the actual HTTP request.
# We will learn more about this later when we discuss HTTP in more detail. The function 
# is supposed to return a HttpResponse object to the calling client. In our example we just 
# return a string representation of the product, which should be displayed by the user's 
# browser as plain text.

def product(request, id):           
        
    # Here we simply query the object with the given ID and return a result text (as plain text)
    # You can try this by running the server (python manage.py runserver) and then calling 
    # http://localhost:8000/product/123/

    # We check whether there is a product with this ID and generate the response text
    if Product.objects.filter(id=id).count()==0:
        response = "Sorry, we don't have a product with the ID " + id
    else:
        response = str(Product.objects.filter(id=id).first())

    return HttpResponse(response, content_type="text/plain")