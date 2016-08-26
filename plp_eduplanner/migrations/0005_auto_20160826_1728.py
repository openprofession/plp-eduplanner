# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plp_eduplanner', '0004_auto_20160825_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professionobjective',
            name='profession',
        ),
        migrations.AddField(
            model_name='profession',
            name='companies_html',
            field=models.TextField(verbose_name='HTML \u043a\u043e\u0434 \u0431\u043b\u043e\u043a\u0430 \u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0439', blank=True),
        ),
        migrations.AddField(
            model_name='profession',
            name='cover',
            field=models.ImageField(upload_to='cover', verbose_name='\u041e\u0431\u043b\u043e\u0436\u043a\u0430', blank=True),
        ),
        migrations.AddField(
            model_name='profession',
            name='cover_alt',
            field=models.CharField(default='', max_length=255, verbose_name='alt \u043a \u043e\u0431\u043b\u043e\u0436\u043a\u0435', blank=True),
        ),
        migrations.AddField(
            model_name='profession',
            name='directions_html',
            field=models.TextField(verbose_name='HTML \u043a\u043e\u0434 \u0431\u043b\u043e\u043a\u0430 \u043d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0439', blank=True),
        ),
        migrations.AddField(
            model_name='profession',
            name='objectives_html',
            field=models.TextField(verbose_name='HTML \u043a\u043e\u0434 \u0431\u043b\u043e\u043a\u0430 \u0437\u0430\u0434\u0430\u0447', blank=True),
        ),
        migrations.AddField(
            model_name='profession',
            name='require_educational_projects',
            field=models.PositiveSmallIntegerField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profession',
            name='salary_max',
            field=models.PositiveIntegerField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profession',
            name='salary_min',
            field=models.PositiveIntegerField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profession',
            name='vacancies_external_link',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='profession',
            name='video',
            field=models.CharField(default='', help_text='\u043a\u043e\u0434 \u0432\u0438\u0434\u0435\u043e', max_length=500, verbose_name='\u041f\u0440\u043e\u043c\u043e\u0432\u0438\u0434\u0435\u043e', blank=True),
        ),
        migrations.AddField(
            model_name='profession',
            name='video_cover',
            field=models.ImageField(upload_to='video_cover', verbose_name='\u041a\u0430\u0440\u0442\u0438\u043d\u043a\u0430 \u0434\u043b\u044f \u0432\u0438\u0434\u0435\u043e', blank=True),
        ),
        migrations.AddField(
            model_name='profession',
            name='video_cover_alt',
            field=models.CharField(max_length=255, verbose_name='alt \u043a \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0435 \u0434\u043b\u044f \u0432\u0438\u0434\u0435\u043e', blank=True),
        ),
        migrations.DeleteModel(
            name='ProfessionObjective',
        ),
    ]
