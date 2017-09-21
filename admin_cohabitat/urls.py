from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth import views as auth_views

from coapp_system import settings
from . import views

urlpatterns = [
                  url(r'^login', auth_views.login, name='login'),
                  url(r'^logout', views.login, name='logout'),
                  url(r'^home', views.home, name='logout'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
