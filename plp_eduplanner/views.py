# coding: utf-8
from __future__ import unicode_literals

from django.db.models import Q
from django.http import JsonResponse
from django.views import generic
from plp_eduplanner import models


class ProfessionCompetenciesTree(object):
    def get_tree(self, obj):
        related = obj.competencies.all().select_related('comp__parent')[:100]  # Все компетенции последнего уровня для тек. проф
        leaf_nodes_only_prof = [x.comp_id for x in related]
        sub_parents_ids = models.Competence.objects.filter(pk__in=[x.comp.parent_id for x in related])  # ID компетеций 2 уровня
        leaf_nodes = models.Competence.objects.filter(parent_id__in=sub_parents_ids)  # Все-все компетенции для компетенций 2 уровня для этой проф.
        ret = {}
        ret['related'] = related
        ret['tree'] = models.Competence.objects.get_queryset_ancestors(sub_parents_ids, include_self=True)  # Получение дерева
        ret['leaf_nodes'] = sorted(leaf_nodes, key=lambda x: x.pk not in leaf_nodes_only_prof)  # Сначала выводим попадающие под тек. проф.
        ret['leaf_nodes_only_prof'] = leaf_nodes_only_prof

        return ret


class Profession(ProfessionCompetenciesTree, generic.DetailView):
    template_name = 'plp_eduplanner/profession.html'
    queryset = models.Profession.objects.filter(is_public=True)
    context_object_name = 'profession'

    def get_context_data(self, **kwargs):
        cd = super(Profession, self).get_context_data(**kwargs)
        cd.update(self.get_tree(self.object))

        # TODO подразумевается какая-либо логика?
        cd['other_professions'] = models.Profession.objects.filter(~Q(pk=self.object.pk), is_public=True)[:2]

        # print len(connection.queries) # print course???
        return cd


class Professions(generic.ListView):
    template_name = 'plp_eduplanner/professions.html'
    queryset = models.Profession.objects.filter(is_public=True)
    context_object_name = 'professions'
    paginate_by = 100  # TODO Paginate?


class ProfessionPlan(ProfessionCompetenciesTree, generic.DetailView):
    queryset = models.Profession.objects.filter(is_public=True)
    context_object_name = 'profession'

    def get(self, *args, **kwargs):
        obj = self.get_object(self.queryset)
        cd = self.get_tree(obj)
        prof_comps = {x.comp_id: x.rate for x in cd['related']}
        user_comps = {x.comp_id: x.rate for x in self.request.user.competencies.all()[:100]}
        required = models.Competence.get_required_comps(prof_comps, user_comps)
        required_set = set(required.keys())

        expected_courses = sorted(models.Profession.get_expected_courses(required), key=lambda x: len(required_set - set([x.comp_id for x in x.competencies.all()])), reverse=False)

        plan = models.Competence.get_plan(expected_courses, required.copy())
        return JsonResponse(
            {
                'courses': [
                    getattr(course, 'edu_planner_response', {'err': 'Create edu_planner_response property in course class'}) for course, ttl in plan],
                'competencies': [(x, y) for x, y in required.items()]
            }
        )
