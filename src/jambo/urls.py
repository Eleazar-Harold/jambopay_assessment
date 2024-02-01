from django.urls import path

from . import views

app_name='jambo'
urlpatterns = [
    path('', views.user_business_list_view, name='list'),
    path('create/', views.user_business_create, name='create'),
]