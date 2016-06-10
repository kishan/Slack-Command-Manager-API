from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.tableflip, name='tableflip'),
    url(r'^index/', views.index, name='index'),
]