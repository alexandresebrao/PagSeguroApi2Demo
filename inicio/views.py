from django.shortcuts import render
from pagseguro.api import PagSeguroApiTransparent, PagSeguroItem
from django.http import HttpResponse


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
    api = PagSeguroApiTransparent()
    if request.POST['payment'] == "boleto":
        api.set_payment_method('boleto')
        api.set_sender_hash(request.POST['sender_hash'])
        # Item
        item1 = PagSeguroItem(id='0001', description='Anucio', amount='39.00',
                              quantity=1)
        # Dados do Comprador
        sender = {'name': 'Jose Comprador', 'area_code': 11, 'phone': 56273440,
                  'email': 'comprador@sandbox.pagseguro.com.br', 'cpf': '22111944785'}
        api.set_sender(**sender)

        api.add_item(item1)
        shipping = {'street': "Av. Brigadeiro Faria Lima", 'number': 1384, 'complement': '5o andar', 'district': 'Jardim Paulistano', 'postal_code': '01452002', 'city': 'Sao Paulo', 'state': 'SP', 'country': 'BRA',}
        api.set_shipping(**shipping)
        data = api.checkout()
