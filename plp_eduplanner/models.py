# coding: utf-8
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from plp.models import User, Course
from plp_eduplanner import validators
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext_lazy as _


class Competence(MPTTModel):
    title = models.CharField(max_length=200, unique=True, verbose_name=_('Название'))
    annotation = models.CharField(max_length=200, blank=True, verbose_name=_('Аннотация'))
    is_public = models.BooleanField(default=True, db_index=True, verbose_name=_('Публичный'))
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_('Родитель'))

    @staticmethod
    def get_plan(expected_courses, required_competencies):
        plan = []
        for course in expected_courses:
            local_plan = [course, 0]
            for rel in course.competencies.all():
                if rel.comp_id in required_competencies and rel.rate >= required_competencies[rel.comp_id] and not required_competencies[rel.comp_id] == 0:
                    local_plan[1] += 1
                    required_competencies[rel.comp_id] = 0
            plan.append(local_plan)
        return filter(lambda x: x[1] > 0, plan)

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
    cover_alt = models.CharField(max_length=255, default='', blank=True, verbose_name=_(u'alt к обложке'))
    video = models.CharField(max_length=500, blank=True, default='', verbose_name=_(u'Промовидео'), help_text=_(u'код видео'))
    video_cover = models.ImageField(upload_to='video_cover', blank=True, verbose_name=_(u'Картинка для видео'))
    video_cover_alt = models.CharField(max_length=255, blank=True, verbose_name=_(u'alt к картинке для видео'))

    salary_min = models.PositiveIntegerField(default=None, blank=True, null=True)
    salary_max = models.PositiveIntegerField(default=None, blank=True, null=True)
    vacancies_external_link = models.URLField(blank=True)

    require_educational_projects = models.PositiveSmallIntegerField(default=None, blank=True, null=True)

    companies_html = models.TextField(blank=True, verbose_name=_('HTML код блока компаний'))
    objectives_html = models.TextField(blank=True, verbose_name=_('HTML код блока задач'))
    directions_html = models.TextField(blank=True, verbose_name=_('HTML код блока направлений'))

    @staticmethod
    def get_expected_courses(required_comps):
        qs = Course.objects.filter(competencies__comp_id__in=required_comps.keys()).prefetch_related('competencies').distinct()  # TODO: duplicate query

        print qs.query

        return qs

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
