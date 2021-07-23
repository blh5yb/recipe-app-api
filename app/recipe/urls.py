from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
router.register('tags', views.TagViewSet)  # register viewset with router

app_name = 'recipe'  # reverse function can look up correct url

urlpatterns = [
    path('', include(router.urls))  # all routes created by default router will be included in path
]
