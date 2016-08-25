# coding: utf-8
from __future__ import unicode_literals
from django.views import generic
from plp_eduplanner import models


class Profession(generic.DetailView):
    template_name = 'plp_eduplanner/profession.html'
    queryset = models.Profession.objects.filter(is_public=True)

    def get_context_data(self, **kwargs):
        cd = super(Profession, self).get_context_data(**kwargs)
        cd['objectives'] = self.object.objectives.all()[:10]

        return cd
