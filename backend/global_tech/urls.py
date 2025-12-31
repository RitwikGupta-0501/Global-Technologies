"""
URL configuration for global_tech project.

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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from product.api import router as product_router

api = NinjaAPI(
    title="Global Tech API", description="API for Next.js Frontend", version="1.0.0"
)
api.add_router("/products", product_router)

urlpatterns = [
    path("admin/", admin.site.urls),  # URL for Admin page (handled by base django)
    path("api/", api.urls),  # URL for the api (handled by django ninja)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
