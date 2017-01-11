from __future__ import unicode_literals
from pagseguro.api import PagSeguroApiTransparent, PagSeguroItem
from django.db import models


class PaymentPagSeguro(models.Model):
    TYPE_PAYMENT = (
        ('1', 'boleto'),
        ('2', 'cartão'),
    )
    sender_name = models.TextField()
    sender_area_code = models.IntegerField()
    sender_phone = models.CharField(max_length=15)
    sender_email = models.TextField()
    sender_cpf = models.CharField(max_length=11)
    shipping_street = models.TextField()
    shipping_number = models.IntegerField(blank=True, null=True)
    shipping_complement = models.TextField(blank=True, null=True)
    shipping_district = models.TextField()
    shipping_postalcode = models.CharField(max_length=8)
    shipping_city = models.TextField()
    shipping_state = models.CharField(max_length=2)
    shipping_country = models.CharField(max_length=3)
    payment_type = models.CharField(choices=TYPE_PAYMENT, max_length=1)
    pagseguro_code = models.TextField()

    def sender_dictionary(self):
        return {'name': self.sender_name, 'area_code': self.area_code,
                'phone': self.sender_phone, 'email': self.email,
                'cpf': self.cpf}

    def shipping_dictionary(self):
        return {'street': self.shipping_street, 'number': self.shipping_number,
                'complement': self.shipping_complement,
                'district': self.shipping_district,
                'postal_code': self.shipping_postalcode,
                'city': self.shipping_city,
                'state': self.shipping_state, 'country': self.shipping_country}

    def checkout(self, sender_hash):
        # Instancia a parte da api do Pagseguro
        api = PagSeguroApiTransparent()

        # Adicionamos os Items comprados
        for item in self.itempayment_set.all():
            api.add_item(PagSeguroItem(item.dictionary()))

        api.set_sender(**self.sender_dictionary())
        api.set_shipping(**self.shipping_dictionary())
        if (self.payment_type == 1):
            api.set_payment_method('boleto')
        data = api.checkout()
        data['']


class ItemPayment(models.Model):
    item_id = models.IntegerField()
    item_description = models.TextField()
    item_quantity = models.IntegerField()
    item_amount = models.FloatField()
    payment_pagseguro = models.ForeignKey(PaymentPagSeguro)

    def dictionary(self):
        return {'id': self.item_id, 'item_description': self.item_description,
                'amount': self.item_amout, 'quantity': self.quantity}
