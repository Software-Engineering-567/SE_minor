from django.urls import path

from . import views

urlpatterns = [
    # ex: /YH15/
    path('', views.list, name='list'),
    # ex: /YH15/5/
    path('<int:bar_id>/', views.details, name='detail'),
    # ex: /YH15/5/info/
    path('<int:bar_id>/info/', views.info, name='info'),
]
