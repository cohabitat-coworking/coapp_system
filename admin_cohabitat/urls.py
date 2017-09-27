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
                  url(r'^config', views.config, name='config'),
                  url(r'^recursos', views.resources, name='resources'),
                  url(r'^planos', views.plans, name='plans'),
                  url(r'^itens', views.itens, name='items'),
                  url(r'^menu', views.menu, name='menu'),
                  url(r'^agenda', views.menu, name='menu'),
                  url(r'^clientes', views.menu, name='menu'),
                  url(r'^$', auth_views.login, name='login'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
