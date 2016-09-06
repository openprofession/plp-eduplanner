# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plp_eduplanner', '0010_profession_salary_average'),
    ]

    operations = [
        migrations.AddField(
            model_name='profession',
            name='academic_banner_html',
            field=models.TextField(help_text='\u041e\u0442\u043e\u0431\u0440\u0430\u0436\u0430\u0435\u0442\u0441\u044f \u0432 \u0444\u0443\u0442\u0435\u0440\u0435 \u0443\u0447\u0435\u0431\u043d\u043e\u0433\u043e \u043f\u043b\u0430\u043d\u0430 \u043d\u0430 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0435 \u043f\u0440\u043e\u0444\u0435\u0441\u0441\u0438\u0438', verbose_name='HTML \u043a\u043e\u0434 \u0431\u043b\u043e\u043a\u0430 \u0430\u043a\u0430\u0434\u0435\u043c\u0438\u0447\u0435\u0441\u043a\u043e\u0433\u043e \u0431\u0430\u043d\u043d\u0435\u0440\u0430', blank=True),
        ),
    ]
