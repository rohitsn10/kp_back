"""
URL configuration for configure project.

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

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.urls import re_path
from configure.views import index
urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('user_profile/',include('user_profile.urls')),
    path('land_module/',include('land_module.urls')),
    path('activity_module/',include('activity_module.urls')),
    path('project_module/',include('project_module.urls')),
    path('document_control/',include('document_control.urls')),
    path('material_management/', include('material_management.urls')),
    path('annexures_module/',include('annexures_module.urls')),
    path('quality_inspection/',include('quality_inspection.urls')),
    path('hoto_module/',include('hoto_module.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    re_path(r'^.*$', never_cache(TemplateView.as_view(template_name="index.html"))),
]