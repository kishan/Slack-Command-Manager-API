from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.sentiment, name='sentiment'),
    url(r'^channel/$', views.sentiment_channel, name='sentiment_channel'),
    url(r'^index/', views.index, name='index'),
]