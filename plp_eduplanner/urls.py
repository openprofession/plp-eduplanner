# coding: utf-8
from __future__ import unicode_literals
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from plp_eduplanner import views

urlpatterns = [
    url('^professions/$', login_required(views.Professions.as_view()), name='professions'),
    url('^profession/(?P<pk>\d+)/$', login_required(views.Profession.as_view()), name='profession'),
    url('^profession/(?P<pk>\d+)/plan/$', login_required(views.ProfessionPlan.as_view()), name='profession_plan'),
    url('^profession/(?P<pk>\d+)/learn/$', login_required(views.LearnProfession.as_view()), name='learn_profession'),
    url('^plan/(?P<pk>\d+)/forget/$', login_required(views.ForgetPlan.as_view()), name='forget_plan'),
    url('^dashboard/$', views.Dashboard.as_view(), name='dashboard')
]
