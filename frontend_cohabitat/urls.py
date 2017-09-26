
from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns

from coapp_system import settings
from . import views

urlpatterns = [
                  url(r'^index', views.index, name='index'),
                  url(r'^planos', views.planos, name='planos'),
                  url(r'^sobre', views.sobre, name='sobre'),
                  url(r'^send_email', views.send_email, name='send_email'),
                  url(r'^$', views.index, name='index'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)

