# coding: utf-8
from __future__ import unicode_literals
import time
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.views import generic
from plp_eduplanner import models
from django.conf import settings


class Dashboard(generic.TemplateView):
    """
    Главная пользователя
    """
    template_name = 'profile/dashboard.html'

    def get_context_data(self, **kwargs):
        cd = super(Dashboard, self).get_context_data(**kwargs)
        html = []
        if not models.Plan.objects.filter(user=self.request.user).exists():
            html += self._select_profession()
        else:
            html += self._profession()
        cd['html'] = mark_safe(''.join(html))
        return cd

    def _select_profession(self):
        return [render_to_string('profile/dashboard/select_profession.html', dict(professions=models.Profession.objects.filter(is_public=True)[:5]))]

    def _profession(self):
        plan = models.Plan.objects.filter(user=self.request.user).first()
        cd = plan.profession.competencies_tree()
        cd['profession'] = plan.profession
        return [
            render_to_string('profile/dashboard/profession.html', cd),
            render_to_string('profile/dashboard/plan.html', {'courses': plan.courses.all()[:100], 'plan': plan})
        ]


class Professions(generic.ListView):
    """
    Актуально только для dev
    """
    template_name = 'plp_eduplanner/professions.html'
    queryset = models.Profession.objects.filter(is_public=True)
    context_object_name = 'professions'
    paginate_by = 100  # TODO Paginate?


class AbstractProfessionPlan(generic.DetailView):
    queryset = models.Profession.objects.filter(is_public=True)
    context_object_name = 'profession'

    def get(self, *args, **kwargs):
        self.object = self.get_object(self.queryset)
        self.tree = self.object.competencies_tree()
        prof_comps = {x.comp_id: x.rate for x in self.tree['related']}
        user_comps = {x.comp_id: x.rate for x in self.request.user.competencies.all()[:100]}

        self.required = models.Competence.get_required_comps(prof_comps, user_comps)
        self.required_set = set(self.required.keys())

        expected_courses = sorted(models.Profession.get_expected_courses(self.required), key=lambda x: len(self.required_set - set([x.comp_id for x in x.competencies.all()])), reverse=False)

        self.plan = models.Competence.get_plan(expected_courses, self.required.copy())

        return self.response()


class Profession(AbstractProfessionPlan):
    """
    Страница профессии
    """
    template_name = 'plp_eduplanner/profession.html'
    queryset = models.Profession.objects.filter(is_public=True)
    context_object_name = 'profession'

    def get_context_data(self, **kwargs):
        cd = super(Profession, self).get_context_data(**kwargs)
        cd.update(self.tree)

        # TODO подразумевается какая-либо логика?
        cd['other_professions'] = models.Profession.objects.filter(~Q(pk=self.object.pk), is_public=True)[:2]
        cd['plan'] = self.plan
        return cd

    def response(self):
        return self.render_to_response(self.get_context_data())


class ProfessionPlan(AbstractProfessionPlan):
    """
    Получить план для изучения професии
    """

    def _course_response(self, course):
        data = dict()
        data['title'] = str(course)

        session = course.next_session
        data['price'] = session.price if session else None
        data['datetime_starts'] = time.mktime(session.datetime_starts.timetuple()) if session else None
        return data

    def response(self):
        """

        Returns:
            JsonResponse: Данные о курсах и компетенциях требуемых для изучения указанной профессии
            {
                courses: see _course_response()
                competencies: [[competence_id,rate],[competence_id,rate]]
            }

        """
        return JsonResponse(
            {
                'courses': {course.pk: self._course_response(course) for course, ttl in self.plan},
                'competencies': [(x, y) for x, y in self.required.items()]
            }
        )


class LearnProfession(AbstractProfessionPlan):
    def response(self):
        """
        Начать изучение профессии
        :return: Redirect to  plp_eduplanner.Dashboard view
        """
        if self.object.can_learn(self.request.user):
            self.object.learn(self.request.user, [course for course, ttl in self.plan])
        return HttpResponseRedirect(reverse('plp_eduplanner:dashboard'))


class ForgetPlan(generic.View):
    """
    Удалить выбранный план
    """

    def get(self, *args, **kwargs):
        plan = models.Plan.objects.get(user=self.request.user, pk=self.kwargs.get('pk'))
        plan.delete()
        return HttpResponseRedirect(reverse('plp_eduplanner:dashboard'))


class ForgetAll(generic.View):
    """
    Удалить все планы
    """

    def get(self, *args, **kwargs):
        if getattr(settings, 'DEBUG') is True:
            models.Plan.objects.filter(user=self.request.user).all().delete()
        return HttpResponseRedirect(reverse('plp_eduplanner:dashboard'))
