from django.shortcuts import render
from pagseguro.api import PagSeguroApiTransparent
from django.http import HttpResponse
from inicio.models import PaymentPagSeguro, ItemPayment
import datetime


# Create your views here.
def index(request):
    context = {}
    data = PagSeguroApiTransparent().get_session_id()
    if not data['success']:
        return HttpResponse('<h1>Error :()</h1>')
    context['session_id'] = data['session_id']
    context['anos'] = range(datetime.datetime.now().year,
                            int(datetime.datetime.now().year)+20)
    months = []
    for i in range(1, 12):
        months.append("%02d" % i)
    context['months'] = months
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
    payment.amount = 29
    if request.POST['payment'] == 'boleto':
        payment.type = 1
    else:
        payment.type = 2
    payment.status = 0
    payment.save()

    item = ItemPayment()
    item.ident = 1
    item.description = "Anuncio"
    item.amount = 29
    item.quantity = 1
    item.payment = payment
    item.save()

    if request.POST['payment'] == 'boleto':
        payment.checkout_boleto(request.POST['sender_hash'])
        request.session['url'] = payment.boleto_url()
    else:
        payment.checkout_cartao(request.POST['sender_hash'],
                                request.POST['token'],
                                datetime.date(1985, 02, 24))

    request.session['payment'] = request.POST['payment']
    return HttpResponse('<h1>Pronto :()</h1>')


def sucesso(request):
    if (request.session['payment'] == 'boleto'):
        context = {'url': request.session['url']}
        template = "sucesso_boleto.html"
    else:
        context = {'ok'}
        template = "sucesso_cartao.html"
    return render(request, template, context)


def historico(request):
    payments = PaymentPagSeguro.objects.all().order_by('-created_at')
    template = "transacoes.html"
    context = {'pagamentos': payments}
    return render(request, template, context)
