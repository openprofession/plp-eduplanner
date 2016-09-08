# coding: utf-8
from __future__ import unicode_literals
from django.core.management import BaseCommand
from plp_eduplanner import models


class Command(BaseCommand):
    help = 'Перерасчет всех комп. 3 уровня'

    def handle(self, *args, **options):
        for node in models.Competence.objects.filter(level=1):
            node.recount_leafs()

        print 'Finished.'
