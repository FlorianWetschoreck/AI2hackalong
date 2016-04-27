from django.db import models

# In this file, we specify the data model of our web application

# Defining the following class, will implictly create a database table 'Product' 
# with three columns id (primary_key), name and price. These models need to be 
# registered with the django site by including the following statement in
# the admin.py (see the corresponding file in the app product_catalog)

# admin.site.register(models.Product)

# Any added or updated models will be reflected in the underlying database by 
# running the following command on the command line (in the root directory of KITshop)

# > python manage.py makemigrations (will generate SQL statements that update the database schema)
# > python manage.py migrate (will actually execute these SQL statements)

# Through a so-called object-relational-mapper (ORM), each row in the table can be accessed 
# as a python object, and queries can be executed simply by calling functions of the Product class

# All rows/objects can be retrieved via the field Product.objects.all() 
# A query for a product with id 123 can be executed via Product.objects.filter(id=123).first()

class Product(models.Model):

    # This will generate a primary key with integer type 
    id = models.IntegerField(primary_key=True)

    # The product name is a character string with maximum 255 characters
    name = models.CharField(max_length=255)

    # The price is a float 
    price = models.FloatField()

    # By the following method, we can specify what happens if we retrieve a string representation 
    # of the object (for instance by calling str(obj))
    def __str__(self):
        return 'Product name: ' + self.name + '\n' + 'Price: ' + str(self.price) + ' Euro'