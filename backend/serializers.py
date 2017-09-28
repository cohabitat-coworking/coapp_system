from rest_framework import serializers
from rest_framework.authtoken.models import Token

from models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')


class ExistingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')


class GenericAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericAddress
        fields = ('id', 'description')


class CoworkingSerializer(serializers.ModelSerializer):
    address = GenericAddressSerializer()

    class Meta:
        model = Coworking
        fields = ('id', 'name', 'cnpj', 'address')
        depth = 2


class CoworkingCreationSerializer(serializers.ModelSerializer):
    address = serializers.PrimaryKeyRelatedField(queryset=GenericAddress.objects.all())

    class Meta:
        model = Coworking
        fields = ('id', 'name', 'cnpj', 'address')
        depth = 2


class ProfileSerializer(serializers.ModelSerializer):
    user = ExistingUserSerializer()
    address = serializers.PrimaryKeyRelatedField(queryset=UserAddress.objects.all())

    class Meta:
        model = Profile
        depth = 2
        fields = ('cpf', 'rg', 'profile_image', 'address', 'user')


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ('id', 'description')


class ProfileDocumentSerializer(serializers.ModelSerializer):
    user = ExistingUserSerializer()
    address = UserAddressSerializer()

    class Meta:
        model = Profile
        depth = 2
        fields = ('cpf', 'rg', 'profile_image', 'user', 'address')


class JuridicProfileSerializer(serializers.ModelSerializer):
    user = ExistingUserSerializer()
    address = serializers.PrimaryKeyRelatedField(queryset=UserAddress.objects.all())

    class Meta:
        depth = 2
        model = ProfileJuridic
        fields = ('user', 'cnpj', 'profile_image', 'address')


class JuridicProfileCreationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    address = serializers.PrimaryKeyRelatedField(queryset=UserAddress.objects.all())

    class Meta:
        model = ProfileJuridic
        fields = ('user', 'cnpj', 'address')



class ContactInfoCreationSerializer(serializers.ModelSerializer):
    # type = serializers.PrimaryKeyRelatedField(queryset=ContactType.objects.all())

    # coworking = serializers.PrimaryKeyRelatedField(queryset=Coworking.objects.all())

    class Meta:
        model = ContactInfo
        fields = ('id', 'name', 'email', 'phone')
        depth = 2


class ContactInfoSerializer(serializers.ModelSerializer):
    # type = serializers.CharField(source="type.type")

    class Meta:
        model = ContactInfo
        fields = ('id', 'name', 'email', 'phone')
        depth = 2


class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = ('id', 'type',)


class ImageItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageItem
        fields = ('id', 'image',)


class ItemSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="type.type")
    unity = serializers.CharField(source="unity.unity")
    images = ImageItemSerializer(source="imageitem_set", many=True)

    class Meta:
        model = Item
        fields = ('id', 'name', 'price', 'unity', 'description', 'type', 'images')
        depth = 2


class ItemCreationSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=ItemType.objects.all())
    unity = serializers.PrimaryKeyRelatedField(queryset=ItemUnity.objects.all())

    class Meta:
        model = Item
        fields = ('id', 'name', 'price', 'unity', 'description', 'type')
        depth = 2


class PlanItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = PlanItem
        fields = ('item', 'quantity')
        depth = 2


class PlanItemCreationSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())

    class Meta:
        model = PlanItem
        fields = ('item', 'quantity')
        depth = 2


class ImageResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageResource
        fields = ('id', 'image')


class ResourceSerializer(serializers.ModelSerializer):
    images = ImageItemSerializer(source="imageresource_set", many=True)

    class Meta:
        model = Resource
        fields = ('id', 'name', 'description', 'price', 'images')


class ResourceCreationSerializer(serializers.ModelSerializer):
    # type = serializers.PrimaryKeyRelatedField(queryset=ContactType.objects.all())

    # coworking = serializers.PrimaryKeyRelatedField(queryset=Coworking.objects.all())

    class Meta:
        model = Resource
        fields = ('id', 'name', 'description', 'price')
        depth = 2


class PlanResourceSerializer(serializers.ModelSerializer):
    resource = ResourceSerializer()

    class Meta:
        model = PlanResource
        fields = ('resource', 'quantity_hours')


class PlanResourceCreationSerializer(serializers.ModelSerializer):
    resource = serializers.PrimaryKeyRelatedField(queryset=Resource.objects.all())

    class Meta:
        model = PlanResource
        fields = ('resource', 'quantity_hours')


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ('id', 'type',)


class ImageRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageRoom
        fields = ('id', 'image',)


class RoomSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="type.type")
    images = ImageRoomSerializer(source="imageroom_set", many=True)

    class Meta:
        model = Room
        fields = ('id', 'name', 'description', 'price_hour', 'price_month', 'type', "images")
        depth = 2


class RoomCreationSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=RoomType.objects.all())

    class Meta:
        model = Room
        fields = ('id', 'name', 'description', 'price_hour', 'price_month', 'type',)
        depth = 2


class PlanRoomSerializer(serializers.ModelSerializer):
    room = RoomSerializer()

    class Meta:
        model = PlanRoom
        fields = ('room', 'quantity_hours')
        depth = 2


class PlanRoomCreationSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    class Meta:
        model = PlanRoom
        fields = ('room', 'quantity_hours')
        depth = 2


class PlanSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()

    class Meta:
        model = Plan
        depth = 2
        fields = ('id', 'name', 'description', 'price')


class PlanCreationSerializer(serializers.ModelSerializer):
    resources = PlanResourceCreationSerializer(source='planresource_set', many=True)
    rooms = PlanRoomCreationSerializer(source='planroom_set', many=True)
    items = PlanItemCreationSerializer(source='planitem_set', many=True)

    def update(self, instance, validated_data):
        instance.name = validated_data["name"]
        instance.description = validated_data["description"]
        instance.price = validated_data["price"]
        instance.save()

        previous_rooms = PlanRoom.objects.filter(plan=instance)

        for room in previous_rooms:
            room.delete()

        for room_data in validated_data["planroom_set"]:
            room_instance = room_data["room"]
            plan_room = PlanRoom(plan=instance,
                                 room=room_instance,
                                 quantity_hours=room_data["quantity_hours"])
            plan_room.save()

        previous_resource = PlanResource.objects.filter(plan=instance)

        for resource in previous_resource:
            resource.delete()

        for resource_data in validated_data["planresource_set"]:
            resource_instance = resource_data["resource"]
            plan_resource = PlanResource(plan=instance,
                                         resource=resource_instance,
                                         quantity_hours=resource_data["quantity_hours"])
            plan_resource.save()

        previous_items = PlanItem.objects.filter(plan=instance)

        for item in previous_items:
            item.delete()

        for item_data in validated_data["planitem_set"]:
            item_instance = item_data["item"]
            plan_item = PlanItem(plan=instance,
                                 item=item_instance,
                                 quantity=item_data["quantity"])
            plan_item.save()

        return instance

    class Meta:
        model = Plan
        depth = 2
        fields = ('id', 'name', 'description', 'price', 'resources', 'rooms', 'items')


class PlanDetailSerializer(serializers.ModelSerializer):
    resources = PlanResourceSerializer(source='planresource_set', many=True)
    rooms = PlanRoomSerializer(source='planroom_set', many=True)
    items = PlanItemSerializer(source='planitem_set', many=True)

    class Meta:
        model = Plan
        depth = 2
        fields = ('id', 'name', 'description', 'price', 'resources', 'rooms', 'items')


class AgendaItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = AgendaItem
        fields = ('agenda', 'item', 'quantity', 'start_time_slot','end_time_slot')


class AgendaResourceSerializer(serializers.ModelSerializer):
    resource = serializers.PrimaryKeyRelatedField(queryset=Resource.objects.all())

    class Meta:
        model = AgendaResource
        fields = ('resource', 'start_time_slot','end_time_slot')


class AgendaQueryResourceSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    scheduling_id = serializers.SerializerMethodField()

    def get_scheduling_id(self, obj):
        return obj.agenda.id

    def get_date(self, obj):
        return obj.agenda.date

    class Meta:
        model = AgendaResource
        fields = ('scheduling_id', 'date', 'start_time_slot','end_time_slot')


class AgendaRoomSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    class Meta:
        model = AgendaRoom

        # depth = 1
        fields = ('room', 'start_time_slot','end_time_slot')


class AgendaDateOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda
        fields = ('id', 'date')


class AgendaRoomQuerySerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    scheduling_id = serializers.SerializerMethodField()

    def get_scheduling_id(self, obj):
        return obj.agenda.id

    def get_date(self, obj):
        return obj.agenda.date

    class Meta:
        model = AgendaRoom
        depth = 1
        fields = ('scheduling_id', 'date', 'start_time_slot','end_time_slot')


class QueryAgendaSerializer(serializers.ModelSerializer):
    resources = AgendaResourceSerializer(source='agendaresource_set', many=True)
    rooms = AgendaRoomSerializer(source='agendaroom_set', many=True)
    items = AgendaItemSerializer(source='agendaitem_set', many=True)

    class Meta:
        model = Agenda
        depth = 2
        fields = ('id', 'date', 'rooms', 'resources', 'items')


class UserToken(serializers.ModelSerializer):
    user = ExistingUserSerializer()
    private_token = serializers.CharField(source='key')
    coworking = serializers.SerializerMethodField()

    def get_coworking(self, token):
        profile = Profile.objects.get(user=token.user)
        coworking = Coworking.objects.get(pk=profile.coworking.id)
        return CoworkingSerializer(coworking).data

    class Meta:
        model = Token
        depth = 2
        fields = ('private_token', 'user', 'coworking')


class AgendaContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgendaContracts
        fields = '__all__'


class ContractSerializer(serializers.ModelSerializer):
    agendas = AgendaContractSerializer(source='agendacontracts_set', many=True)

    class Meta:
        model = Contract
        depth = 2
        fields = ('id', 'user', 'start_date', 'end_date', 'agendas')


class PersonalProfileCreationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    address = serializers.PrimaryKeyRelatedField(queryset=UserAddress.objects.all())

    class Meta:
        model = Profile
        fields = ('cpf', 'rg', 'user', 'address')
