from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls

from rest_framework.routers import DefaultRouter

from orders.viewsets import OrdersViewSet
from markets.viewsets import MarketsViewSet

router = DefaultRouter()
router.register("orders", OrdersViewSet)
router.register("markets", MarketsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('docs/', include_docs_urls(title='Matching Engine API'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


