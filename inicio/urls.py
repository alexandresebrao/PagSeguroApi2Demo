from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'checkout/$', views.checkout, name='checkout'),
    url(r'^$', views.index, name='index'),

]
