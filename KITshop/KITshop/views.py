from django.http.response import HttpResponse

from product_catalog.models import Product

import stomp

# We first create a connection to the ActiveMQ Stomp endpoint 
conn = stomp.Connection([('localhost', 61613)])
conn.start()
conn.connect()


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


def order(request, id):                   
    # Calling this URL will trigger an order of a product by sending a message to an ActiveMQ 
    # message queue. In our example, we have an additional JAVA Client that waits for order messages 
    # and simply prints them on the console

    # Prior to running this example, you should ... 
    # 1.) Start an ActiveMQ broker by running "activemq start" in the bin directory 
    #       of the activemq installation (available in this repository)
    # 2.) Run the JAVA client that waits for messages. For this, install JDK 8 and the NetBeans IDE
    #       Then open, compile and run the project in the directory "OrderProcessor" in NetBeans
    # 3.) Install the python stomp ActiveMQ client module stomp.py by running "pip install stomp.py" on the console

    # You can the try this example by running the server (python manage.py runserver) and then call 
    # http://localhost:8000/order/123/

    # We first query the name of the product
    product_name = str(Product.objects.filter(id=id).first())

    # We then send an order message to the KITShop_OrderBook Queue 
    conn.send(body='Order of ' + product_name, destination='KITShop_OrderBook')

    # and disconnect 
    conn.disconnect()

    return HttpResponse('Thank you for your order!')