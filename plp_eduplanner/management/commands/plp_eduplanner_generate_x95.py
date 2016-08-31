# coding: utf-8
from __future__ import unicode_literals
from random import randint, choice
from django.core.management import BaseCommand
from plp_eduplanner import models

from plp.models import Course, University


class Command(BaseCommand):
    _prof_x = 0

    def handle(self, *args, **options):
        self._gen_cources()
        self._gen_root()
        self._gen_comp(1, 3000, 5000)
        self._gen_comp(2, 5000, 10000)
        self._gen_prof()

    def _gen_cources(self):
        comps = models.Competence.objects.filter(children__isnull=True).all()
        uns = University.objects.all()
        for x in xrange(1000):
            c = Course.objects.create(slug='slug%s' % x, university=choice(uns))
            for x in xrange(randint(2, 30)):
                models.CourseComp.objects.create(course=c, comp=choice(comps), rate=randint(1, 3))

    def _gen_prof(self):
        comps = models.Competence.objects.filter(children__isnull=True).all()
        for x in xrange(100, 200):
            p = models.Profession.objects.create(title='Profession. %d' % x, description='Description')
            for x in xrange(randint(2, 30)):
                models.ProfessionComp.objects.create(profession=p, comp=choice(comps), rate=randint(1, 3))

    def _gen_root(self):
        for x in xrange(50):
            models.Competence.objects.create(title=str(x))

    def _gen_comp(self, lvl, mn=1, mx=100):
        parents = models.Competence.objects.filter(level=lvl - 1)
        for x in xrange(randint(mn, mx)):
            parent = choice(parents)
            title = '%s.%d' % (parent.title, x)
            models.Competence.objects.create(title=title, parent=parent)
