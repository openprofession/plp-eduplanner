# coding: utf-8
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q

from plp.models import User, Course
from plp_eduplanner import validators
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext_lazy as _


class CompManager(models.Manager):
    def select_parents(self, competencies):
        tree_list = {}
        query = Q()
        for node in competencies:
            if node.tree_id not in tree_list:
                tree_list[node.tree_id] = []

            parent = node.parent.pk if node.parent is not None else None,

            if parent not in tree_list[node.tree_id]:
                tree_list[node.tree_id].append(parent)

                query |= Q(lft__lt=node.lft, rght__gt=node.rght, tree_id=node.tree_id)

        return self.get_queryset().filter(query)


class Competence(MPTTModel):
    title = models.CharField(max_length=200, unique=True, verbose_name=_('Название'))
    annotation = models.CharField(max_length=200, blank=True, verbose_name=_('Аннотация'))
    is_public = models.BooleanField(default=True, db_index=True, verbose_name=_('Публичный'))
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_('Родитель'))
    # objects = CompManager()

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

    def get_absolute_url(self):
        return reverse('plp_eduplanner:profession', args=(self.pk,))

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-title']
        verbose_name = _('Профессия')
        verbose_name_plural = _('Профессии')


class UserComp(AbstractRateBasedRelation):
    user = models.ForeignKey(User, verbose_name=_('Пользователь'))

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
    course = models.ForeignKey(Course, verbose_name=_('Курс'))

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        verbose_name = _('Компетенция курса')
        verbose_name_plural = _('Компетенции курсов')
