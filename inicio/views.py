from django.shortcuts import render
from pagseguro.api import PagSeguroApiTransparent


# Create your views here.
def index(request):
    context = {'user': request.user}
    data = PagSeguroApiTransparent().get_session_id()
    context['session_id'] = data['session_id']
    template = 'index.html'
    return render(request, template, context)
