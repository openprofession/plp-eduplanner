# coding: utf-8
from __future__ import unicode_literals
from django.db import models
from plp.models import User, Course
from plp_eduplanner import validators
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext_lazy as _


class Competence(MPTTModel):
    title = models.CharField(max_length=200, unique=True, verbose_name=_('Название'))
    annotation = models.CharField(max_length=200, verbose_name=_('Аннотация'))
    is_public = models.BooleanField(default=True, db_index=True, verbose_name=_('Публичный'))
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_('Родитель'))

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
    description = models.TextField(verbose_name=_('Описание'))
    is_public = models.BooleanField(default=True, db_index=True, verbose_name=_('Публичный'))

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
    profession = models.ForeignKey(Profession, verbose_name=_('Професия'))

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
