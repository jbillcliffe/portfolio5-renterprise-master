from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

"""
URL configuration for renterprise project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


urlpatterns = [
    path('', include('menu.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('items/', include('items.urls')),
    path('orders/', include('orders.urls')),
    path('profiles/', include('profiles.urls')),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt", content_type="text/plain")
    ),
    path(
        "sitemap.xml",
        TemplateView.as_view(
            template_name="sitemap.xml", content_type="text/plain")
    )
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)

handler404 = 'renterprise.views.handler404'

# https://books.agiliq.com/projects/django-admin-cookbook/en/latest/change_text.html
admin.site.site_header = "Renterprise Administration"
admin.site.site_title = "Renterprise Portal"
admin.site.index_title = "Welcome to Renterprise Administration Portal"
