from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("device/",include(("device.urls","device"),namespace="device")),
    path("admin/", admin.site.urls),
]
