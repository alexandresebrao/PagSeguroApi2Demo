from pagseguro.signals import notificacao_recebida
from inicio.models import PaymentPagSeguro


def load_signal(sender, transaction, **kwargs):
    reference = transaction['code']
    payment = PaymentPagSeguro.objects.get(pagseguro_code=reference)
    payment.status = transaction['status']
    payment.save()

notificacao_recebida.connect(load_signal)
