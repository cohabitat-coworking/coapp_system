# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserAddress(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=300, verbose_name="Descrição")

    def __unicode__(self):
        return u'%s' % self.description

    class Meta:
        verbose_name_plural = "Endereços de Usuários"


class GenericAddress(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=300, verbose_name="Descrição")

    def __unicode__(self):
        return u'%s' % self.description

    class Meta:
        verbose_name_plural = "Endereços Genéricos"


class Coworking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, verbose_name="Nome")
    address = models.ForeignKey(GenericAddress)
    url = models.URLField()
    logo = models.ImageField(upload_to="images/logos", null=True, blank=True)
    cnpj = models.CharField(max_length=14)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        ordering = ('created_at',)


class Profile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11)
    rg = models.CharField(max_length=13)
    coworking = models.ForeignKey(Coworking, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="images/profiles", null=True, blank=True)
    address = models.ForeignKey(UserAddress, verbose_name="Endereco", null=True)

    def get_cpf(self):
        return self.cpf

    def __unicode__(self):
        return u'%s' % self.user.username

    class Meta:
        verbose_name_plural = "Perfis de Usuários - Pessoa Física"


class ContactType(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=10, verbose_name="Tipo")
    coworking = models.ForeignKey(Coworking, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % self.type

    class Meta:
        verbose_name_plural = "Tipos de contato"


class ContactInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    coworking = models.ForeignKey(Coworking, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Nome")
    info = models.CharField(max_length=300)
    type = models.ForeignKey(ContactType, verbose_name="Tipo")

    def __unicode__(self):
        return u'%s' % (self.type.type + ": " + self.name + " - " + self.info)

    class Meta:
        verbose_name_plural = "Informações de Contato"


class ProfileJuridic(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cnpj = models.CharField(max_length=14)
    juridic_name = models.CharField(max_length=300)
    fantasy_name = models.CharField(max_length=300)
    coworking = models.ForeignKey(Coworking, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="images/profiles", null=True, blank=True)
    address = models.ForeignKey(UserAddress, verbose_name="Endereco", null=True)

    def __unicode__(self):
        return u'%s' % self.user.username

    class Meta:
        verbose_name_plural = "Perfis de Usuários - Pessoa Jurídica"


class JuridicProfileDocument(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(ProfileJuridic, on_delete=models.CASCADE)
    document = models.FileField(upload_to="files/profiles", null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.profile.juridic_name

    class Meta:
        verbose_name_plural = "Documentos - Pessoa Jurídica"


class JuridicPartner(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    juridic_profile = models.ForeignKey(ProfileJuridic)
    personal_profile = models.ForeignKey(Profile)

    def __unicode__(self):
        return u'%s' % self.juridic_profile.juridic_name + " - " + self.personal_profile.user.username

    class Meta:
        verbose_name_plural = "Socios  - Pessoa Juridica"


class Resource(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, verbose_name="Nome")
    description = models.CharField(max_length=300, verbose_name="Descrição")
    price = models.FloatField(verbose_name="Valor")
    coworking = models.ForeignKey(Coworking, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name_plural = "Recursos"


class ImageResource(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="images/resources", null=True, blank=True)
    resource = models.ForeignKey(Resource, verbose_name="Recurso", on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % self.image.path

    class Meta:
        verbose_name_plural = "Imagens de recursos"


class RoomType(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=20, verbose_name="Tipo")
    coworking = models.ForeignKey(Coworking, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % (self.type)

    class Meta:
        verbose_name_plural = "Tipos de sala"


class Room(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, verbose_name="Nome")
    description = models.CharField(max_length=300, verbose_name="Descrição")
    price_hour = models.FloatField(verbose_name="Valor Hora")
    price_month = models.FloatField(verbose_name="Valor mensal")
    type = models.ForeignKey(RoomType, verbose_name="Tipo")
    area = models.FloatField(verbose_name="Area", default=0)
    coworking = models.ForeignKey(Coworking, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        verbose_name_plural = "Salas"


class ImageRoom(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="images/rooms", null=True, blank=True)
    room = models.ForeignKey(Room, verbose_name="Sala", on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % self.image.url

    class Meta:
        verbose_name_plural = "Imagens de Salas"


class ItemType(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=10, verbose_name="Tipo")
    coworking = models.ForeignKey(Coworking, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % (self.type)

    class Meta:
        verbose_name_plural = "Tipos de item"


class ItemUnity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    unity = models.CharField(max_length=10, verbose_name="Unidade")

    def __unicode__(self):
        return u'%s' % (self.unity)

    class Meta:
        verbose_name_plural = "Unidades de Item"


class Item(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, verbose_name="Nome")
    description = models.CharField(max_length=300, verbose_name="Descrição")
    price = models.FloatField(default=None)
    unity = models.ForeignKey(ItemUnity, verbose_name="Unidade", default=None)
    type = models.ForeignKey(ItemType, verbose_name="Tipo")
    coworking = models.ForeignKey(Coworking, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        verbose_name_plural = "Itens"


class ImageItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="images/items", null=True, blank=True)
    item = models.ForeignKey(Item, verbose_name="Item", on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % self.image.path

    class Meta:
        verbose_name_plural = "Imagens de itens"


class Plan(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, verbose_name="Nome")
    description = models.CharField(max_length=300, verbose_name="Descrição")
    price = models.FloatField(verbose_name="Preço")
    resources = models.ManyToManyField(Resource, verbose_name="Recursos", through="PlanResource")
    rooms = models.ManyToManyField(Room, verbose_name="Salas", through="PlanRoom")
    items = models.ManyToManyField(Item, verbose_name="Itens", through="PlanItem")
    coworking = models.ForeignKey(Coworking, on_delete=models.CASCADE, default=None)
    square_meter_value = models.FloatField(verbose_name="Valor metro quadrado", default=0)
    plan_type = models.BooleanField(default=True, verbose_name="Plano Dinâmico")

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        verbose_name_plural = "Planos"


class PlanItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Quantidade")

    class Meta:
        verbose_name_plural = "Itens em Planos"

    def __unicode__(self):
        return u'%s' % (self.plan.name + " - " + self.item.name)


class PlanResource(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    quantity_hours = models.IntegerField(verbose_name="Quantidade de horas")

    def __unicode__(self):
        return u'%s' % (self.plan.name + " - " + self.resource.name)

    class Meta:
        verbose_name_plural = "Recursos em Planos"


class PlanRoom(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    quantity_hours = models.IntegerField(verbose_name="Quantidade de horas")

    def __unicode__(self):
        return u'%s' % (self.plan.name + " - " + self.room.name)

    class Meta:
        verbose_name_plural = "Salas em Planos"


class UserHasPlan(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coworking = models.ForeignKey(Coworking, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % (self.plan.name + " - " + self.user.username)

    class Meta:
        verbose_name_plural = "Planos e Usuários"


class Agenda(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField(verbose_name="Data do agendamento")
    rooms = models.ManyToManyField(Room, verbose_name="Salas", through="AgendaRoom")
    items = models.ManyToManyField(Item, verbose_name="Items", through="AgendaItem")
    resources = models.ManyToManyField(Resource, verbose_name="Recursos", through="AgendaResource")
    user_plan = models.ForeignKey(UserHasPlan, on_delete=models.CASCADE, unique_for_date="date")
    coworking = models.ForeignKey(Coworking, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % self.id + " - " + self.user_plan.user.username.__str__() + " - " + self.date.__str__()

    class Meta:
        verbose_name_plural = "Agendas"


class AgendaRoom(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time_slot = models.TimeField(verbose_name="Horário Inicial")
    end_time_slot = models.TimeField(verbose_name="Horário Final")

    def __unicode__(self):
        return u'%s' % self.room.name + " - " + self.agenda.user_plan.user.username + " - " + self.agenda.date.__str__() + " - " + self.start_time_slot.__str__()

    class Meta:
        ordering = ('agenda', 'start_time_slot',)
        verbose_name_plural = "Salas em Agenda"


class AgendaItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    start_time_slot = models.TimeField(verbose_name="Horário Inicial")
    end_time_slot = models.TimeField(verbose_name="Horário Final")
    quantity = models.IntegerField(verbose_name="Quantidade")

    def __unicode__(self):
        return u'%s' % self.item.name

    class Meta:
        verbose_name_plural = "Items em Agenda"


class AgendaResource(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    start_time_slot = models.TimeField(verbose_name="Horário Inicial")

    def __unicode__(self):
        return u'%s' % self.resource.name

    class Meta:
        verbose_name_plural = "Recursos em Agenda"


class Contract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    coworking = models.ForeignKey(Coworking, on_delete=models.CASCADE, default=None)

    def __unicode__(self):
        return u'%s' % self.user

    class Meta:
        verbose_name_plural = "Contratos"


class AgendaContracts(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    contracts = models.ForeignKey(Contract, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % self.agenda.date

    class Meta:
        verbose_name_plural = "Agendas em contrato"


class BillStatus(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s' % self.status

    class Meta:
        verbose_name_plural = "Status de fatura"


class Bill(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    status = models.ForeignKey(BillStatus)
    month = models.IntegerField()

    def __unicode__(self):
        return u'%s' % self.contract + " - " + self.month.__str__()

    class Meta:
        verbose_name_plural = "Faturas"
