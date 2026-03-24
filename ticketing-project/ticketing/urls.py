from django.urls import path
from .views import request_list_view, request_create_view, request_update_view

urlpatterns = [
    path('', request_list_view, name='request_list'),
    path('create/', request_create_view, name='request_create'),
    path('<int:pk>/edit/', request_update_view, name='request_update'),
]
