from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'checkout/$', views.checkout, name='checkout'),
    url(r'sucesso/$', views.sucesso, name='sucesso'),
    url(r'historico/$', views.historico, name='historico'),
    url(r'^$', views.index, name='index'),
]
