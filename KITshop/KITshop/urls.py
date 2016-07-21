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
    

    # Here we can match urls accessed by users with a regular expression
    # The following expression matches all urls of the form BASEURL/product/XYZ
    # We can further specify a so-called view function that will handle such requests
    # Here we map this class of urls to the product function in the file view.py 
    # The inclusion of (?P<id>) means that the string matched by the following regular 
    # expression will be passed to the product-function as a parameter called id
    url(r'^product/(?P<id>\w+)/$', views.product, name='product'),

    # We add another url pattern mapping to a view function that returns the product review with a given ID
    url(r'^mostCriticalReview/(?P<id>\w+)/$', views.mostCriticalReview, name='mostCriticalReview'),
    url(r'^mostHelpfulReview/(?P<id>\w+)/$', views.mostHelpfulReview, name='mostHelpfulReview'),

    # This url and the mapping to the admin url is activated by default 
    # django conveniently provides a default backend that is available at the url 

    # BASEURL/admin/

    # If you access this url, you will be prompted for a username and password 
    # You can generate such an account by running 

    # > python manage.py createsuperuser 

    # on the command line
    # Here, I have alrady generated a superuser with the following credentials

    # username: admin
    # password: AngewandteInformatik
    url(r'^admin/', admin.site.urls),
]
