from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('', include('portal.urls')),
    path('', include('admin_page.urls')),
    path('', include('staff.urls'))
]

handler404 = "portal.views.page_not_found_view"