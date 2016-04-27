# AI2hackalong
This branch contains the solution of the first #django hackalong of AI2 2016. 

The goal was to take the bare example of the django web application in the 
master branch and implement a simple product catalog that will form the basis 
of our KITshop. For this we need to implement a simple data model, generate 
the database schema, and then implement a view component that generates a 
maximally simple representation of the products in our product catalog.

You can test this solution by changing to the directory KITShop and then 
running from the command line:

> python manage.py runserver

This will start a webserver on your local machine and you can then navigate to
the product catalog by accessing, e.g., the following URLs:

http://127.0.0.1:8000/product/123/ 
http://127.0.0.1:8000/product/42/ 

The key points of the implementation are located (and explained) in the 
files:

KITshop/urls.py 
KITshop/views.py 
product_catalog/models.py 


