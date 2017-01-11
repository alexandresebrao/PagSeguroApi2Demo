from django.shortcuts import render
from pagseguro.api import PagSeguroApiTransparent, PagSeguroItem


# Create your views here.
def index(request):
    context = {'user': request.user}
    data = PagSeguroApiTransparent().get_session_id()
    context['session_id'] = data['session_id']
    template = 'index.html'
    return render(request, template, context)

def checkout(request):
    api = PagseguroApiTransparent()
    sender = {'name': 'Jose Comprador', 'area_code': 11, 'phone': 56273440, 'email': 'comprador@uol.com.br', 'cpf': '22111944785',}
    api.set_sender(**sender)
    shipping = {'street': "Av. Brigadeiro Faria Lima", 'number': 1384, 'complement': '5o andar', 'district': 'Jardim Paulistano', 'postal_code': '01452002', 'city': 'Sao Paulo', 'state': 'SP', 'country': 'BRA',}
    api.set_shipping(**shipping)
    item1 = PagSeguroItem(id='0001', description='Notebook Prata', amount='24300.00', quantity=1)
    api.set_payment_method('boleto')
    api.set_sender_hash(request.POST['sender_hash'])
    api.checkout()
    context = {'user': request.user}
    data = PagSeguroApiTransparent().get_session_id()
    context['session_id'] = data['session_id']
    template = 'index.html'
    return render(request, template, context)
