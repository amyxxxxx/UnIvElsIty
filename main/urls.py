from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('To_do_list/', views.To_do_list),
    path('to_do_list_detail/<int:to_do_list_id>', views.to_do_list_detail),
    path('to_do_list/', views.to_do_list),
]
