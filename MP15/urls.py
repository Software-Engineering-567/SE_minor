from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('YH15/', include('YH15.urls')),
    path('admin/', admin.site.urls),
]