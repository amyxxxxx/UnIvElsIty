from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),    
    path('users/<int:customuser_id>', views.customuser_detail),
    path('users/change_password/', views.change_password)
]
