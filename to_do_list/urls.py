"""to_do_list URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework import permissions #new
from rest_framework.decorators import schema
from drf_yasg.views import get_schema_view #new
from drf_yasg import openapi

import main #api

schema_view = get_schema_view(
    openapi.Info(
        title="TO-DO LIST API",
        default_version="v1",
        description="Api documentation for our to-do list api",
        terms_of_service="",
        contact=openapi.Contact(email="fayvz.xo@gmail.com"),
        license=openapi.License(name = "MIT License")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include ('main.urls')),
    path('v1/', include('account.urls')),
     #documentation
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
    name='schema-redoc'),
]