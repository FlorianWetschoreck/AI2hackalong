"""KITshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [

    # The urls.py file contains a mapping between URLs accessed by web clients and the 
    # functions that handle the corresponding HTTP Requests. In the context of the MVC pattern, 
    # you could thus see this as a part of the controller, i.e. the component that manages what is
    # to be displayed to the user

    # We can match urls accessed by users with a regular expression
    # The following expression matches all urls of the form BASEURL/product/XYZ
    # We can further specify a so-called view function that will handle such requests (see views.py)

    # Here we map a class of urls to the product function in the file view.py 
    # The inclusion of (?P<id>) means that the string matched by the following regular 
    # expression will be passed to the product-function as a parameter called id
    url(r'^product/(?P<id>\w+)/$', views.product, name='product'),
    url(r'^addToShoppingCart/(?P<id>\w+)/$', views.addToShoppingCart, name='addToShoppingCart'),
    url(r'^showShoppingCart/', views.showShoppingCart, name='showShoppingCart'),

    # This url and the mapping to the admin url is activated by default 
    # django conveniently provides a default backend that is available at the url 

    # BASEURL/admin/

    # If you access this url, you will be prompted for a username and password 
    # You can generate such an account by running 

    # > python manage.py createsuperuser 

    # on the command line. I have alrady generated a superuser for you which you can use 
    # with the following credentials: 

    # username: admin
    # password: AngewandteInformatik

    url(r'^admin/', admin.site.urls),
]
