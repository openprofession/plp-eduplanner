# coding: utf-8
from __future__ import unicode_literals
from django.db.models import Q
from django.views import generic
from plp_eduplanner import models


class Profession(generic.DetailView):
    template_name = 'plp_eduplanner/profession.html'
    queryset = models.Profession.objects.filter(is_public=True)
    context_object_name = 'profession'

    def get_context_data(self, **kwargs):
        cd = super(Profession, self).get_context_data(**kwargs)
        related = self.object.competencies.all().select_related('comp__parent')[:100]  # Все компетенции последнего уровня для тек. проф
        leaf_nodes_only_prof = [x.comp_id for x in related]
        sub_parents_ids = models.Competence.objects.filter(pk__in=[x.comp.parent_id for x in related])  # ID компетеций 2 уровня
        leaf_nodes = models.Competence.objects.filter(parent_id__in=sub_parents_ids)  # Все-все компетенции для компетенций 2 уровня для этой проф.

        cd['tree'] = models.Competence.objects.get_queryset_ancestors(sub_parents_ids, include_self=True)  # Получение дерева
        cd['leaf_nodes'] = sorted(leaf_nodes, key=lambda x: x.pk not in leaf_nodes_only_prof)  # Сначала выводим попадающие под тек. проф.
        cd['leaf_nodes_only_prof'] = leaf_nodes_only_prof

        # TODO подразумевается какая-либо логика?
        cd['other_professions'] = models.Profession.objects.filter(~Q(pk=self.object.pk), is_public=True)[:2]

        return cd


class Professions(generic.ListView):
    template_name = 'plp_eduplanner/professions.html'
    queryset = models.Profession.objects.filter(is_public=True)
    context_object_name = 'professions'
    paginate_by = 100  # TODO Paginate?
