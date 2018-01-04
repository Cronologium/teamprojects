from django.conf.urls import url

from web import views

urlpatterns = [
    url(r'^encrypt$', views.encrypt),
    url(r'^decrypt$', views.decrypt),
    url(r'^', views.home),
]