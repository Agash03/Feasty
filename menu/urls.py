from django.urls import path
from .views import *

urlpatterns = [
    #search
    path('search/', search_menu, name='search_menu'),
    
    #location
    path('add_address/',create_address, name='address_create'),
    path('show_address/', show_address, name='address_show'),
    path('update_address/<int:address_id>/', address_update, name='address_update'),
    path('delete_address/<int:address_id>/', address_delete, name='address_delete'),


    #food menu
    path('home/',Home.as_view()),
    path('vegmenu/',VeganMenu.as_view()),
    path('nvmenu/',NVMenu.as_view()),
    
    #cart_details
    path('add-to-cart/veg/<int:idv>/', AddToCart.as_view(), name='add_to_cart_veg'),
    path('add-to-cart/nonveg/<int:idnv>/', AddToCart.as_view(), name='add_to_cart_nonveg'),
    path('cart/', Cart.as_view(), name='cart'),
    path('remove-from-cart/<str:item_id>/',RemoveFromCart.as_view(), name='remove_from_cart'),
    
    #orders
    path('checkout/',checkout,name="checkout"),
    path('payment/',payment,name="payment"),
    path('orderplaced/', order_placed, name='order_placed'),
    path('orderdelete/<int:order_id>/',order_delete, name='order_delete'),
    path('orderhistory/', order_history, name='order_history'),


    #food_details
    path('add/',AddFood.as_view()),
    path('add-food/',food_table),
    path('update_veg/<int:id>/',food_vegtable_update,name='veg_update'),
    path('delete_veg/<int:id>/',food_vegtable_delete,name='veg_delete'),
    path('update_nv/<int:id>/',food_nvtable_update, name='nv_update'),
    path('delete_nv/<int:id>/',food_nvtable_delete, name='nv_delete'),
]