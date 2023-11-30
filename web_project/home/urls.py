from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings 

urlpatterns = [
    path('', views.store, name= 'store'),
    path('about/', views.about, name='about'),
    path('cart/', views.cart, name= 'cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_cart/', views.updateaddtocart, name='update_cart'),
    path('update_wishlist/', views.update_wishlist, name='update_wishlist'),
    path('movies/', views.movies, name= 'movies'),
    path('books/', views.books, name= 'books'),
    path('music/', views.music, name= 'music'),
    path('wishlist/', views.wishlist, name= 'wishlist'),
    path('shop/products/<str:name>/<str:uniqueid>', views.prod_view, name='productview'),
    path('review/<str:name>/<str:uniqueid>', views.review, name='review'),
    path('addrating/', views.review, name='review'),
    path('process_order/', views. process_order, name='process_order'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutpage, name='logout'),
    path('search/', views.search, name='search'),
    path('user_profile/', views.user_profile, name='userprofile'),
    path('saved_address/', views.saved_address, name='savedaddress'),






]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)