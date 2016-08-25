# coding: utf-8
from __future__ import unicode_literals
from django.conf.urls import url
from plp_eduplanner import views

urlpatterns = [
    url('^profession/(?P<pk>\d+)/', views.Profession.as_view(), name='profession')
]
