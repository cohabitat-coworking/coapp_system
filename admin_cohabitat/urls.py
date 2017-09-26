<<<<<<< HEAD
from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns

from coapp_system import settings
from . import views

urlpatterns = [
                  url(r'^login', views.login, name='index'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
=======
from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth import views as auth_views

from coapp_system import settings
from . import views

urlpatterns = [
                  url(r'^login', auth_views.login, name='login'),
                  url(r'^logout', auth_views.logout, {'next_page': '/admin'}, name='logout'),
                  url(r'^home', views.home, name='home'),
                  url(r'^$', auth_views.login, name='login'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
>>>>>>> b7dbd304e55ba402e2a7130abf0e95403d58b581
