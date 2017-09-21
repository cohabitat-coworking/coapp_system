from __future__ import unicode_literals

from rest_framework.test import APITestCase, APIClient

from backend.serializers import *


class CreateAgendaTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('test_user_personal', 'usertestpersonal@gmail.com', 'test1234')

        self.address = GenericAddress.objects.create(description="A fake address")
        self.coworking = Coworking.objects.create(name="Test coworking", address=self.address, cnpj="123456789012")
        self.plan = Plan.objects.create(
            name="TestPlan",
            description="TestDescription",
            price=1,
            coworking=self.coworking,
            square_meter_value=1,
            plan_type=True)

        self.room_type = RoomType.objects.create(type="testtype", coworking=self.coworking)
        self.room = Room.objects.create(name="TestRoom",
                                        description="AtestDescription",
                                        price_hour=1,
                                        price_month=1,
                                        type=self.room_type,
                                        area=1,
                                        coworking=self.coworking)

        self.user_plan = UserHasPlan.objects.create(user=self.user, plan=self.plan, coworking=self.coworking)

        self.plan_room = PlanRoom.objects.create(plan=self.plan, room=self.room, quantity_hours=5)

        self.agenda = Agenda.objects.create(
            user_plan=self.user_plan,
            coworking=self.coworking,
            date='2017-09-10')

        self.agenda_room = AgendaRoom.objects.create(agenda=self.agenda,
                                                     room=self.room,
                                                     start_time_slot='12:00:00.000000',
                                                     end_time_slot='13:00:00.000000')

    # def test_create_agenda(self):
    #     self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
    #     self.token = Token.objects.create(user=self.user)
    #
    #     self.client.force_login(user=self.user)
    #
    #     serialized_agenda = QueryAgendaSerializer(self.agenda)
    #
    #     final_record = {"scheduling": serialized_agenda.data,
    #                     "plan": self.plan.id}
    #
    #     response = self.client.post('/api/coworkings/{}/user_schedulings/{}'.format(self.coworking.id, self.user.id),
    #                                 final_record,
    #                                 HTTP_AUTHORIZATION=self.token, format='json')
    #
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
