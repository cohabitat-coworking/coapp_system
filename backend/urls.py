from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns

from coapp_system import settings
from . import views

urlpatterns = [

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/contracts/(?P<user_id>[0-9]+)',
                      views.ContractList.as_view()),
                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/contact_infos/(?P<contact_id>[0-9]+)',
                      views.ContactInfoDetail.as_view()),
                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/contact_infos', views.ContactInfoList.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/contact_types', views.ContactTypeList.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/rooms/(?P<room_id>[0-9]+)/images',
                      views.RoomImageUpload.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/rooms/(?P<room_id>[0-9]+)',
                      views.RoomDetail.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/rooms/images/(?P<image_id>[0-9]+)',
                      views.RoomImageDetail.as_view()),
                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/rooms', views.RoomsList.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/room_types', views.RoomTypesList.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/resources/(?P<resource_id>[0-9]+/images)',
                      views.ResourceImageUpload.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/resources/(?P<resource_id>[0-9]+)',
                      views.ResourceDetail.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/resources/images/(?P<image_id>[0-9]+)',
                      views.ResourceImageDetail.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/resources', views.ResourcesList.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/items/(?P<item_id>[0-9]+)/images',
                      views.ItemImageUpload.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/items/(?P<item_id>[0-9]+)',
                      views.ItemDetail.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/items/images/(?P<image_id>[0-9]+)',
                      views.ItemImageDetail.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/items', views.ItemsList.as_view()),
                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/item_types', views.ItemTypesList.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/plans/(?P<plan_id>[0-9]+)', views.PlanDetail.as_view()),
                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/plans', views.PlanInfoList.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/agenda_rooms', views.AgendaRooms.as_view()),
                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/agenda_resources', views.AgendaResources.as_view()),
                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/agenda_items', views.AgendaItems.as_view()),

                  url(
                      r'^coworkings/(?P<coworking_id>[0-9]+)/schedulings/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})',
                      views.QuerySchedulingsByDay.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/schedulings/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})',
                      views.QuerySchedulingsByMonth.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/schedulings/(?P<agenda_id>[0-9]+)',
                      views.QuerySpecificScheduling.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/schedulings', views.QuerySchedulings.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/room_schedulings/(?P<room_id>[0-9]+)',
                      views.QueryRoomSchedulings.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/resource_schedulings/(?P<resource_id>[0-9]+)',
                      views.QueryResourceSchedulings.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/user_schedulings/(?P<user_id>[0-9]+)',
                      views.QueryAllUserSchedulings.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/users/(?P<user_id>[0-9]+)/images',
                      views.PersonalUserImageUpload.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/users/(?P<user_id>[0-9]+)', views.UserDetail.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/users', views.UserList.as_view()),

                  url(r'^coworkings/teste/(?P<user_id>[0-9]+)', views.BillDetail.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)/images', views.CoworkingLogoUpload.as_view()),

                  url(r'^coworkings/(?P<coworking_id>[0-9]+)', views.CoworkingDetail.as_view()),
                  url(r'^coworkings', views.CoworkingList.as_view()),
                  url(r'^users/sign_in', views.UserSignIn.as_view()),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
