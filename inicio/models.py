# -*-coding:utf-8-*-
from __future__ import unicode_literals
from pagseguro.api import PagSeguroApiTransparent, PagSeguroItem
from django.db import models


class PaymentPagSeguro(models.Model):
    TYPE_PAYMENT = (
        ('1', 'boleto'),
        ('2', 'cartão'),
    )
    TRANSACTION_STATUS = (
        ('0', 'Iniciado'),
        ('1', 'Aguardando pagamento'),
        ('2', 'Em revisão'),
        ('3', 'Aprovado'),
        ('4', 'Disponível'),
        ('5', 'Em disputa'),
        ('6', 'Retornado'),
        ('7', 'Cancelado'),
        ('8', 'Estorno'),
        ('9', 'Contestação'),
        ('10', 'Processando estorno'),
        ('11', 'Pré autorizado')
    )
    sender_name = models.TextField()
    sender_area_code = models.IntegerField()
    sender_phone = models.CharField(max_length=20)
    sender_email = models.TextField()
    sender_cpf = models.CharField(max_length=11)
    sender_birthday = models.DateField(blank=True, null=True)
    shipping_street = models.TextField()
    shipping_number = models.IntegerField(blank=True, null=True)
    shipping_complement = models.TextField(blank=True, null=True)
    shipping_district = models.TextField()
    shipping_postalcode = models.CharField(max_length=8)
    shipping_city = models.TextField()
    shipping_state = models.CharField(max_length=2)
    shipping_country = models.CharField(max_length=3)
    type = models.CharField(choices=TYPE_PAYMENT, max_length=1)
    status = models.CharField(max_length=2, choices=TRANSACTION_STATUS,
                              blank=True, null=True)
    pagseguro_code = models.TextField(blank=True, null=True)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def sender_dictionary(self):
        return {'name': self.sender_name, 'area_code': self.sender_area_code,
                'phone': self.sender_phone, 'email': self.sender_email,
                'cpf': self.sender_cpf}

    def shipping_dictionary(self):
        return {'street': self.shipping_street, 'number': self.shipping_number,
                'complement': self.shipping_complement,
                'district': self.shipping_district,
                'postal_code': self.shipping_postalcode,
                'city': self.shipping_city,
                'state': self.shipping_state, 'country': self.shipping_country}

    def checkout_boleto(self, sender_hash):
        # Instancia a parte da api do Pagseguro
        api = PagSeguroApiTransparent()

        # Adicionamos os Items comprados
        for item in self.itempayment_set.all():
            api.add_item(item.pagseguroitem())
        api.set_sender_hash(sender_hash)
        api.set_sender(**self.sender_dictionary())
        api.set_shipping(**self.shipping_dictionary())
        api.set_payment_method('boleto')
        data = api.checkout()
        self.pagseguro_code = data['transaction']['code']
        self.save()
        boleto = Boleto()
        boleto.url = data['transaction']['paymentLink']
        boleto.payment = self
        boleto.save()

    def checkout_cartao(self, sender_hash, token, birthday_date):
        self.sender_birthday = birthday_date
        self.save()
        api = PagSeguroApiTransparent()
        for item in self.itempayment_set.all():
            api.add_item(item.pagseguroitem())
        api.set_sender_hash(sender_hash)
        api.set_sender(**self.sender_dictionary())
        api.set_shipping(**self.shipping_dictionary())
        api.set_payment_method('creditCard')
        api.set_creditcard_token(token)
        if (self.sender_birthday):
            birthday = "%02d/%02d/%s" % (self.sender_birthday.day,
                                         self.sender_birthday.month,
                                         self.sender_birthday.year)
        else:
            birthday = ""
        data = {'quantity': 1, 'value': "%.2f" % self.amount,
                'name': self.sender_name,
                'birth_date': birthday,
                'cpf': self.sender_cpf, 'area_code': self.sender_area_code,
                'phone': "%s" % self.sender_phone}
        api.set_creditcard_data(**data)
        api.set_creditcard_billing_address(**self.shipping_dictionary())
        api.set_sender_hash(sender_hash)
        data = api.checkout()
        if not data['success']:
            print data
            self.delete()
        self.pagseguro_code = data['transaction']['code']
        self.save()

    def boleto_url(self):
        return Boleto.objects.get(payment=self).url


class ItemPayment(models.Model):
    ident = models.IntegerField()
    description = models.TextField()
    quantity = models.IntegerField()
    amount = models.FloatField()
    payment = models.ForeignKey(PaymentPagSeguro)

    def pagseguroitem(self):
        return PagSeguroItem(id=self.ident, description=self.description,
                             amount=("%.2f" % self.amount),
                             quantity=self.quantity)


class Boleto(models.Model):
    url = models.TextField()
    payment = models.OneToOneField(PaymentPagSeguro)
