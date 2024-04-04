from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),
    path('about/', views.about),
    path('contact/', views.contactPage),
    path('products/', views.productPage),
    path('support/', views.support),
    path('details/<int:id>', views.details),
    path('categoryproducts/<int:id>',views.categoryProducts),
    path('signup/', views.signup),
    path('login/', views.userlogin, name="login"),
    path('my-account', views.myaccount, name="my-account"),
    path('logout', views.userlogout, name="logout"),
    path('cart/', views.cart, name="cart"),
    path('add_to_cart', views.add_to_cart, name="add_to_cart"),
    path('delcart/<int:id>', views.delete_cart),
    path('checkout/', views.checkout),
    path('updatecart', views.updatecart, name="updatecart"),
    path('search/', views.search, name="search"),
    path('getstate/', views.getStates),
    path('getcity/', views.getCity),
    path('sendorder/', views.sendOrder),
    path('order-history/', views.OrderHistory),
    path('complete_payment', views.complete_payment, name="complete_payment"),
    # path('profile/', views.Profile)
    # path('initiate_payment', views.initiate_payment, name="initiate_payment")


    

]+ static(settings.MEDIA_URL, 
          document_root=settings.MEDIA_ROOT)


