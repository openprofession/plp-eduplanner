# coding: utf-8
from __future__ import unicode_literals
from itertools import groupby
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_delete, pre_delete
from django.utils.functional import cached_property

from plp.models import User, Course, Participant
from plp_eduplanner import validators
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class Competence(MPTTModel):
    title = models.CharField(max_length=200, unique=True, verbose_name=_('Название'))
    annotation = models.CharField(max_length=200, blank=True, verbose_name=_('Аннотация'))
    is_public = models.BooleanField(default=True, db_index=True, verbose_name=_('Публичный'))
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_('Родитель'))
    total_leafs = models.PositiveIntegerField(default=0, editable=getattr(settings, 'DEBUG'))

    def save(self, *args, **kwargs):
        super(Competence, self).save(*args, **kwargs)
        if self.level == 2:
            self.parent.recount_leafs(commit=True)

    def recount_leafs(self, commit=True):
        self.total_leafs = self.get_descendant_count()
        if commit:
            self.save()

    @staticmethod
    def get_plan(expected_courses, required_competencies, user):
        plan = []
        for course in expected_courses:
            local_plan = [course, 0]
            for rel in course.competencies.all():
                if rel.comp_id in required_competencies and rel.rate >= required_competencies[rel.comp_id] and not required_competencies[rel.comp_id] == 0:
                    local_plan[1] += 1
                    required_competencies[rel.comp_id] = 0
            plan.append(local_plan)
        courses = filter(lambda x: x[1] > 0, plan)
        for course, weight in courses:
            session = course.next_session
            course.in_progress = False
            course.is_graduate = False
            if session:
                try:
                    Participant.objects.filter(user=user).update(is_graduate=True)
                    participant = Participant.objects.get(session=session, user=user)
                except Participant.DoesNotExist:
                    pass
                else:
                    course.in_progress = True
                    course.is_graduate = participant.is_graduate
        return courses

    @staticmethod
    def get_required_comps(required_comps, source_comps):
        """
        Получить все подходящие курсы под указанные компетенция
        Args:
            required_comps (dict): Доступные компетенции
            source_comps (dict): Требуемые компетенции

        Returns:
            dict

        Examples:
            get_required_comps({comp_id:rate,comp_id2:rate},{comp_id1:rate})
            {comp_id2:rate}
        """
        required = {}
        for c in required_comps:
            if c in source_comps:
                if source_comps[c] < required_comps[c]:
                    required[c] = required_comps[c] - source_comps[c]
            else:
                required[c] = required_comps[c]
        return required

    def __unicode__(self):
        return self.title

    class Meta:
        unique_together = (('id', 'parent'),)
        verbose_name = _('Компетенция')
        verbose_name_plural = _('Компетенции')


class AbstractRateBasedRelation(models.Model):
    comp = models.ForeignKey(Competence, verbose_name=_('Компетенция'))
    rate = models.SmallIntegerField(default=1, validators=validators.RATE_VALIDATORS, verbose_name=_('Значение'))

    class Meta:
        abstract = True


class Profession(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Заголовок'))
    sub_title = models.CharField(max_length=200, blank=True, verbose_name=_('Под заголовок'))
    description = models.TextField(verbose_name=_('Описание'))
    is_public = models.BooleanField(default=True, db_index=True, verbose_name=_('Публичный'))

    cover = models.ImageField(upload_to='cover', blank=True, verbose_name=_(u'Обложка'))
    mini_cover = models.ImageField(upload_to='cover', blank=True, verbose_name=_(u'Обложка маленькая'))
    vertical_cover = models.ImageField(upload_to='cover', blank=True, verbose_name=_(u'Вертикальная обложка'))
    chart = models.ImageField(upload_to='chart', blank=True, verbose_name=_(u'Изображение чарта'))

    cover_alt = models.CharField(max_length=255, default='', blank=True, verbose_name=_(u'alt к обложке'))
    video = models.CharField(max_length=500, blank=True, default='', verbose_name=_(u'Промовидео'), help_text=_(u'код видео'))
    video_cover = models.ImageField(upload_to='video_cover', blank=True, verbose_name=_(u'Картинка для видео'))
    video_cover_alt = models.CharField(max_length=255, blank=True, verbose_name=_(u'alt к картинке для видео'))

    salary_min = models.PositiveIntegerField(default=None, blank=True, null=True, verbose_name=_('Мин. з/п'))
    salary_max = models.PositiveIntegerField(default=None, blank=True, null=True, verbose_name=_('Макс. з/п'))
    salary_average = models.PositiveIntegerField(default=None, blank=True, null=True, verbose_name=_('Средняя з/п'))
    vacancies_external_link = models.URLField(blank=True, verbose_name=_('Ссылка на вакансии'))
    vacancies_external_city_link = models.TextField(blank=True, verbose_name=_('HTML Код ссылки на вакансии в городе'))

    require_educational_projects = models.PositiveSmallIntegerField(default=None, blank=True, null=True)

    companies_html = models.TextField(blank=True, verbose_name=_('HTML код блока компаний'))
    objectives_html = models.TextField(blank=True, verbose_name=_('HTML код блока задач'))
    directions_html = models.TextField(blank=True, verbose_name=_('HTML код блока направлений'))
    academic_banner_html = models.TextField(blank=True, verbose_name=_('HTML код блока академического баннера'), help_text=_('Отображается в футере учебного плана на странице профессии'))

    def competencies_tree(self):
        related = self.competencies.all().select_related('comp__parent')[:100]  # Все компетенции последнего уровня для тек. проф
        leaf_nodes_only_prof = [x.comp_id for x in related]
        sub_parents_ids = Competence.objects.filter(pk__in=[x.comp.parent_id for x in related])  # ID компетеций 2 уровня
        leaf_nodes = Competence.objects.filter(parent_id__in=sub_parents_ids)  # Все-все компетенции для компетенций 2 уровня для этой проф.

        ret = dict()
        ret['related'] = related
        ret['tree'] = Competence.objects.get_queryset_ancestors(sub_parents_ids, include_self=True)  # Получение дерева
        ret['leaf_nodes'] = sorted(leaf_nodes, key=lambda x: x.pk not in leaf_nodes_only_prof)  # Сначала выводим попадающие под тек. проф.
        ret['leaf_nodes_only_prof'] = leaf_nodes_only_prof

        return ret

    def competencies_tree_for_user(self, user):
        cd = self.competencies_tree()

        prof_comps = {x.comp_id: x.rate for x in cd['related']}
        user_comps = {x.comp_id: x.rate for x in user.competencies.all()}
            
        cd['required'] = Competence.get_required_comps(prof_comps, user_comps)
        cd['required_set'] = set(cd['required'].keys())

        cd['percents'] = {}
        cd['profession_progress'] = 0
        
        if prof_comps.keys():
            cd['profession_progress'] = int((1 - float(len(cd['required_set'])) / len(prof_comps.keys())) * 100)
            for parent, irels in groupby(sorted(cd['related'], key=lambda x: x.comp.parent_id), key=lambda x: x.comp.parent_id):
                rels = list(irels)
                a = len(rels)
                b = len([x for x in rels if x.comp_id not in cd['required_set']])
                try:
                    p = int((float(b) / a) * 100)
                except ZeroDivisionError:
                    p = 0
                cd['percents'][parent] = p
        return cd

    @staticmethod
    def get_expected_courses(required_comps):
        qs = Course.objects.filter(competencies__comp_id__in=required_comps.keys()).prefetch_related('competencies').distinct()  # TODO: duplicate query

        return qs

    def can_learn(self, user):
        return not Plan.objects.filter(user=user).exists()

    def learn(self, user, courses):
        plan = Plan.objects.create(user=user, profession=self)
        for course in courses:
            Course2Plan.objects.create(plan=plan, course=course)

            # print Course.objects.bulk_create(relations)

    def get_absolute_url(self):
        return reverse('plp_eduplanner:profession', args=(self.pk,))

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-title']
        verbose_name = _('Профессия')
        verbose_name_plural = _('Профессии')


class UserComp(AbstractRateBasedRelation):
    user = models.ForeignKey(User, verbose_name=_('Пользователь'), related_name='competencies')

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        verbose_name = _('Компетенция пользователя')
        verbose_name_plural = _('Компетенции пользователей')


class ProfessionComp(AbstractRateBasedRelation):
    profession = models.ForeignKey(Profession, related_name='competencies', verbose_name=_('Професия'))

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        verbose_name = _('Компетенция профессии')
        verbose_name_plural = _('Компетенция профессий')


class CourseComp(AbstractRateBasedRelation):
    course = models.ForeignKey(Course, verbose_name=_('Курс'), related_name='competencies')

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        verbose_name = _('Компетенция курса')
        verbose_name_plural = _('Компетенции курсов')


class Plan(models.Model):
    user = models.ForeignKey(User)
    profession = models.ForeignKey(Profession, related_name='plans')
    courses = models.ManyToManyField(Course, through='Course2Plan')

    def courses_with_relations(self):
        return Course2Plan.objects.filter(plan=self).select_related('course')


class Course2Plan(models.Model):
    plan = models.ForeignKey(Plan)
    course = models.ForeignKey(Course)

    def course_competencies_ratio(self):
        table = {}
        for rel in self.course.competencies.all().select_related('comp__parent'):
            if rel.comp.parent_id not in table:
                table[rel.comp.parent_id] = [0, rel.comp.parent]

            table[rel.comp.parent_id][0] += 1
        ret = []
        for total_required, competence in table.values():
            if total_required > 0 and competence.total_leafs > 0:
                ret.append((int(float(total_required) / competence.total_leafs * 100), competence))
            else:
                ret.append((0, competence))
        return ret


def recount_leafs_signal_receiver(sender, instance, **kwargs):
    # -1
    if instance.level == 2:
        instance.recount_leafs()


pre_delete.connect(recount_leafs_signal_receiver, Competence)
