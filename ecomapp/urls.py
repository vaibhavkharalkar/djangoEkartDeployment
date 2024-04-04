
from ecomapp import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('product', views.product),
    path('register', views.register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('catfilter/<cid>',views.catfilter),
    path('sortfilter/<sv>',views.sortfilter),
    path('pricefilter',views.pricefilter),
    path('search',views.search),
    path('product_details/<pid>',views.product_details),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.removecart),
    path('updateqty/<x>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('fetchorder',views.fetchorder),
    path('makepayment',views.makepayment),
    path('paymentsuccess',views.paymentsuccess),
    path('contact',views.contact),
    path('about',views.about),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    

