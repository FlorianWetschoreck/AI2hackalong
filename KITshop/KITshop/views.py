from django.http.response import HttpResponse

from product_catalog.models import Product

import requests
from lxml import etree

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

    # Let us now additionally retrieve the most helpful review for this product from our C# Web Service
    # The resulting review.text will be an XML document (as specified in the ProductService web service)
    review = requests.get('http://localhost:8001/rest/products/123/MostHelpfulReview')
    
    # We create an XML document from the response 
    xmldoc = etree.fromstring(review.text)

    # We use a simple XPath query to access the user name and the text of the review
    user = xmldoc.xpath('/ps:Review/ps:User[1]/text()', namespaces={'ps':'http://schemas.datacontract.org/2004/07/ReviewService'})    
    text = xmldoc.xpath('/ps:Review/ps:ReviewText[1]/text()', namespaces={'ps':'http://schemas.datacontract.org/2004/07/ReviewService'})
    
    # Note that the variables user and text can generally contain multiple results. For this reason 
    # The results are a list of string values, which in our case only contain a single element each

    return HttpResponse(product_name + ', user ' + user[0] + ' says: ' + text[0])

def review(request, id):

    review = requests.get('http://localhost:8001/rest/reviews/' + id)
    
    # Just like above, we first retrieve an XML document 
    xmldoc = etree.fromstring(review.text)

    # We then generate an XSLT Transformation based on the XSLT file (residing in the same path as this code file)
    xslt = etree.parse('./KITShop/Review.xslt')

    # We then transform the XML document into an HTML body and return it to the client 
    transform = etree.XSLT(xslt)

    return HttpResponse(transform(xmldoc))