from django.urls import path
from .views import *

urlpatterns = [
    path('signup/',signup),
    path('',loginpage),
    path('logout/',logoutuser),
    path('details/',user_details,name='user_details'),
    path('update/<int:id>/', user_update, name='user_update'),
    path('delete/<int:id>/', user_delete, name='user_delete'),
    path('password_change/', PasswordChangeView.as_view(template_name='password_change.html', success_url='/password_change_done/'), name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    ]
