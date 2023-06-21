from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router1 = DefaultRouter()

router.register('books', views.BookViewSet)
router1.register('patrons', views.PatronViewSet)
app_name = 'library'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(router1.urls)),
]