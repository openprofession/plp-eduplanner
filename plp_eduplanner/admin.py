# coding: utf-8
from __future__ import unicode_literals
from django.contrib import admin
from plp_eduplanner import models
from mptt.admin import MPTTModelAdmin
from django import forms
from django.utils.translation import ugettext_lazy as _
import autocomplete_light


class CompetenceLeafNodes(forms.ModelForm):
    comp = autocomplete_light.ModelChoiceField('CompetenceAutocomplete', label=_('Компетенция'))


class UserCompAdminForm(CompetenceLeafNodes):
    user = autocomplete_light.ModelChoiceField('UserAutocomplete', label=_('Пользователь'))


class ProfessionCompInline(admin.TabularInline):
    model = models.ProfessionComp
    form = CompetenceLeafNodes



@admin.register(models.Profession)
class ProfessionAdmin(admin.ModelAdmin):
    inlines = [ProfessionCompInline]
    list_display = ['title', 'is_public']
    search_fields = ['title', 'description']
    list_filter = ['is_public']


@admin.register(models.Competence)
class CompetenceAdmin(MPTTModelAdmin):
    list_display = ['title', 'annotation', 'is_public']
    list_filter = ['is_public']
    search_fields = ['title', 'annotation']


@admin.register(models.UserComp)
class UserCompAdmin(admin.ModelAdmin):
    list_select_related = ['user', 'comp']
    list_display = ['user', 'comp', 'rate']
    form = UserCompAdminForm


@admin.register(models.CourseComp)
class CourseCompAdmin(admin.ModelAdmin):
    list_select_related = ['course', 'comp']
    list_display = ['course', 'comp', 'rate']
    form = CompetenceLeafNodes
