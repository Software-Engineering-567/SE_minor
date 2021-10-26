from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListBarView.as_view(), name='list'),
    path('search/', views.SearchBarView.as_view(), name='search'),
    path('sort/', views.sort_bars, name='sort'),
    path('filter/', views.filter_bars, name='filter'),
    path('recommend/', views.RecommendBarView.as_view(), name='recommend'),
    path('<int:bar_id>/', views.get_bar_details, name='detail'),
]
