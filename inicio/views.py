from django.shortcuts import render
from pagseguro.api import PagSeguroApiTransparent
from django.http import HttpResponse
from inicio.models import PaymentPagSeguro, ItemPayment

# Create your views here.
def index(request):
    context = {}
    data = PagSeguroApiTransparent().get_session_id()
    if not data['success']:
        return HttpResponse('<h1>Error :()</h1>')
    context['session_id'] = data['session_id']
    template = 'index.html'
    return render(request, template, context)


def checkout(request):
    payment = PaymentPagSeguro()
    payment.sender_name = "Alexandre Sebrao"
    payment.sender_area_code = "47"
    payment.sender_phone = "992752990"
    payment.sender_email = "alexandre.sebrao@sandbox.pagseguro.com.br"
    payment.sender_cpf = "11335624775"
    payment.shipping_street = "Rua Sob Desce desaparece"
    payment.shipping_number = 12
    payment.shipping_complement = ""
    payment.shipping_district = "Rio de Janeiro"
    payment.shipping_postalcode = "22750410"
    payment.shipping_city = "Rio de Janeiro"
    payment.shipping_state = "RJ"
    payment.shipping_country = "BRA"
    payment.type = 1
    payment.status = 'INITIATED'
    payment.save()

    item = ItemPayment()
    item.ident = 1
    item.description = "Anuncio"
    item.amount = 29
    item.quantity = 1
    item.payment = payment
    item.save()

    payment.checkout(request.POST['sender_hash'])
    request.session['url'] = payment.boleto_url()
    request.session['payment'] = "boleto"
    return HttpResponse('<h1>Pronto :()</h1>')


def sucesso(request):
    if (request.session['payment'] == 'boleto'):
        context = {'url': request.session['url']}
        template = "sucesso.html"
        return render(request, template, context)
