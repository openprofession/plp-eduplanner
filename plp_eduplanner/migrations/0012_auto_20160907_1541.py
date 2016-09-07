# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plp_eduplanner', '0011_profession_academic_banner_html'),
    ]

    operations = [
        migrations.AddField(
            model_name='profession',
            name='chart',
            field=models.ImageField(upload_to='chart', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0447\u0430\u0440\u0442\u0430', blank=True),
        ),
        migrations.AddField(
            model_name='profession',
            name='mini_cover',
            field=models.ImageField(upload_to='cover', verbose_name='\u041e\u0431\u043b\u043e\u0436\u043a\u0430 \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u0430\u044f', blank=True),
        ),
        migrations.AddField(
            model_name='profession',
            name='vacancies_external_city_link',
            field=models.TextField(verbose_name='HTML \u041a\u043e\u0434 \u0441\u0441\u044b\u043b\u043a\u0438 \u043d\u0430 \u0432\u0430\u043a\u0430\u043d\u0441\u0438\u0438 \u0432 \u0433\u043e\u0440\u043e\u0434\u0435', blank=True),
        ),
        migrations.AlterField(
            model_name='profession',
            name='salary_average',
            field=models.PositiveIntegerField(default=None, null=True, verbose_name='\u0421\u0440\u0435\u0434\u043d\u044f\u044f \u0437/\u043f', blank=True),
        ),
        migrations.AlterField(
            model_name='profession',
            name='salary_max',
            field=models.PositiveIntegerField(default=None, null=True, verbose_name='\u041c\u0430\u043a\u0441. \u0437/\u043f', blank=True),
        ),
        migrations.AlterField(
            model_name='profession',
            name='salary_min',
            field=models.PositiveIntegerField(default=None, null=True, verbose_name='\u041c\u0438\u043d. \u0437/\u043f', blank=True),
        ),
        migrations.AlterField(
            model_name='profession',
            name='vacancies_external_link',
            field=models.URLField(verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u0432\u0430\u043a\u0430\u043d\u0441\u0438\u0438', blank=True),
        ),
    ]
