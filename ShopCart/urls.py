"""
URL configuration for ShopCart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog import views   # assuming your Django app name is 'blog'
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main Pages
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),

    # Collections & Products
    path('collections/', views.collections, name='collections'),
    path('collections/<str:name>/', views.collectionsview, name='collectionsview'),
    path('collections/<str:cname>/<str:pname>/', views.product_details, name='product_details'),

    # Cart
    path('addtocart/', views.add_to_cart, name='addtocart'),
    path('cart/', views.cart_page, name='cart'),
    path('remove_cart/<str:cid>/', views.remove_cart, name='remove_cart'),

    # Favourites
    path('fav/', views.fav_page, name='fav'),
    path('fav_view/', views.fav_view_page, name='fav_view_page'),
    path('remove_fav/<str:fid>/', views.remove_fav, name='remove_fav'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
