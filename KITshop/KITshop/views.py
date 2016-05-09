from django.http.response import HttpResponse

from product_catalog.models import Product

# In this week's hackalong, we integrate a legacy CORBA Shopping Cart (implemented here in JAVA) into 
# our django application 
from omniORB import CORBA

# For this, you will have to download and install the correct omniORBpy runtime for your python installation

# Admittedly, on Windows this is a little bit cumbersome. You will have to download the 
# latest binaries (e.g. for WIN64 and Python 3.5) and copy them somewhere. 
# Then you will have to set the PYTHONPATH environment variable to include ... 

# PYTHONPATH=PATH_TO_OMNIORB/lib/python;PATH_TO_OMNIORB/lib/x86_w32 

# and adjust the PATH environment variable to include ... (be careful to append and not to replace the existing values!)

# PATH=PATH_TO_OMNIORB/lib/x86_w32;PATH_TO_OMNIORB/bin/x86_w32

# If you are using Visual Studio to implement and run this project, things are a bit simpler. 
# Here you can just paste the two lines above in the environment variable section in the Debug tab 
# of the "KITshop" project properties (right-click on the KITshop project in the project explorer panel on the right)

# Once everything is set up you will first have to start an ORB instance by running orbd on the command line 
# (assuming you are having the JAVA SDK installed)

# You can then start the CORBA ShoppingCartServer on the commandline (execute: java ShoppingCartServer in the ShoppingCart directory)
# Voila! Now the shopping cart can be accessed as a remote object from within this django application

# Thinking about the three-tier architecture discussed in lecture 02, we are now using the ORB as an application server that hosts the 
# business logic of the shopping cart, while the presentation is done by the web server.


# To be able to access the shopping cart object, we first import the client stub, that was generated from the IDL description of the service
import ShoppingCartApp

# We then initialize the object request broker use the IOR string displayed by the server to obtain an object reference
orb = CORBA.ORB_init()
ior = 'IOR:000000000000002549444c3a53686f7070696e67436172744170702f53686f7070696e67436172743a312e3000000000000000010000000000000086000102000000000e3139322e3136382e302e31303700eca700000031afabcb000000002097660d2600000001000000000000000100000008526f6f74504f410000000008000000010000000014000000000000020000000100000020000000000001000100000002050100010001002000010109000000010001010000000026000000020002'

obj = orb.string_to_object(ior)
shoppingcart = obj._narrow(ShoppingCartApp.ShoppingCart)

# In a real-world setting, rather than copying an IOR string, we would register the object using a Naming Service, and then resolve the 
# name to an IOR string and object reference. This can be done via the COS naming Service that is integrated in CORBA. 


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


def addToShoppingCart(request, id):
    if Product.objects.filter(id=id).count()==0:
        response = "Sorry, we don't have a product with the ID " + id
    else:
        shoppingcart.addToShoppingCart(id, 1)
        response = "Added product to shopping cart"
    return HttpResponse(response, content_type="text/plain")


def updateAmountShoppingCart(request, id, amount):
    if Product.objects.filter(id=id).count()==0:
        response = "Sorry, we don't have a product with the ID " + id
    else:
        shoppingcart.updateAmount(id, int(amount))
        response = "Updated amount of product in shopping cart"
    return HttpResponse(response, content_type="text/plain")


def clearShoppingCart(request):   
    shoppingcart.clearShoppingCart()
    response = "Cleared shopping cart"
    return HttpResponse(response, content_type="text/plain")


def showShoppingCart(request):
   
    contents = shoppingcart.getShoppingCartContents()
    result = ""
    for x in contents: 
        result += str(x.amount) +'x product with ID ' + str(x.productID) + '\n'; 
    response = 'ShoppingCart contains: \n =====================\n' + result
    return HttpResponse(response, content_type="text/plain")