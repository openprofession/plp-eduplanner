# coding: utf-8
from __future__ import unicode_literals
import time
import datetime
from django.utils.timezone import utc
from itertools import groupby
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.views import generic
from plp_eduplanner import models
from plp_edmodule.views import update_context_with_modules
from plp.models import Participant, EnrollmentReason
from django.conf import settings


class Dashboard(generic.TemplateView):
    """
    Главная пользователя
    """
    template_name = 'profile/dashboard.html'

    def get_context_data(self, **kwargs):
        cd = super(Dashboard, self).get_context_data(**kwargs)
        self.context_data = cd
        html = []
        if not models.Plan.objects.filter(user=self.request.user).exists():
            html += self._select_profession()
        else:
            html += self._profession()
        cd['html'] = mark_safe(''.join(html))
        participants = Participant.objects.filter(user=self.request.user).\
            select_related('session', 'session__course', 'session__course__university')
        cert_data = dict()
        for p in participants:
            cert_data[p.session] = p.certificate_data
        user_course_sessions = [i.session for i in participants]

        user_session_participants = dict([
            (x.session.id, x.id) for x in participants
        ])

        enrollments = dict([(p.session.id, p) for p in participants])

        now = datetime.datetime.utcnow().replace(tzinfo=utc)

        feature, current, finished = [], [], []
        enr_reasons = EnrollmentReason.objects.filter(
            participant__user__id=self.request.user.id,
            session_enrollment_type__mode__in=['verified', 'audit']
        ).values_list('participant__session', flat=True)
        for cs in user_course_sessions:
            cs.participant_id = user_session_participants.get(cs.id, '')
            e = enrollments.get(cs.id)
            cs.enrollment = e
            cs.honor_ended = cs.id not in enr_reasons and cs.course_status()['code'] == 'ended'
            cs.certificate_data = cert_data[cs]
            if cs.enrollment:
                cs.available_enrollment_types = []
                for_use = [(x, x.is_user_enrolled(self.request.user)) for x in e.get_available_enrollment_types(mode='verified', exclude_expired=False)]
                for_enroll = [(x, x.is_user_enrolled(self.request.user)) for x in e.get_available_enrollment_types(mode='verified')]
                for item in for_use:
                    if item in for_enroll:
                        cs.available_enrollment_types.append(item + ('good', item[0].can_return_payment(self.request.user)))
                    else:
                        cs.available_enrollment_types.append(item + ('expired', False))

            if not cs.datetime_starts or now < cs.datetime_starts:
                feature.append(cs)
                continue

            if cs.datetime_ends and now > cs.datetime_ends:
                finished.append(cs)
                continue

            current.append(cs)   
        context_data = dict()
        context_data['courses_finished'] = finished
        context_data['courses_current'] = current
        context_data['courses_feature'] = feature
        update_context_with_modules(context_data, self.request.user)
        self.context_data.update(context_data)
        return self.context_data

    def _select_profession(self):
        return [
            render_to_string('profile/dashboard/select_profession.html', dict(professions=models.Profession.objects.filter(is_public=True)))
        ]

    def _profession(self):
        plan = models.Plan.objects.filter(user=self.request.user).first()
        cd = plan.profession.competencies_tree_for_user(self.request.user)
        cd['profession'] = plan.profession
        self.context_data.update(cd)
        return [
            render_to_string('profile/dashboard/plan.html', {'courses': plan.courses.all(), 'plan': plan, 'profession_progress': cd['profession_progress']}),
            render_to_string('profile/dashboard/profession.html', cd),
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
        self.tree = self.object.competencies_tree_for_user(self.request.user)

        expected_courses = sorted(models.Profession.get_expected_courses(self.tree['required']), key=lambda x: len(self.tree['required_set'] - set([x.comp_id for x in x.competencies.all()])), reverse=False)

        self.plan = models.Competence.get_plan(expected_courses, self.tree['required'].copy(), self.request.user)

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
        try:
            exist = models.Plan.objects.get(user=self.request.user, pk=self.kwargs.get('pk'))
            exist.delete()
        except models.Plan.DoesNotExist:
            pass

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
