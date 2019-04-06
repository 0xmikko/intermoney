from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orders.viewsets import OrdersViewSet

router = DefaultRouter()
router.register("orders", OrdersViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
