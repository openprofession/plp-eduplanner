# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plp_eduplanner', '0002_auto_20160825_1731'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessionObjective',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
                ('priority', models.SmallIntegerField(default=0, verbose_name='\u041f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442')),
                ('profession', models.ForeignKey(verbose_name='\u041f\u0440\u043e\u0444\u0435\u0441\u0441\u0438\u044f', to='plp_eduplanner.Profession')),
            ],
            options={
                'ordering': ['-priority'],
                'verbose_name': '\u0420\u0435\u0448\u0430\u043c\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430 \u043f\u0440\u043e\u0444\u0435\u0441\u0441\u0438\u0438',
                'verbose_name_plural': '\u0420\u0435\u0448\u0430\u043c\u044b\u0435 \u0437\u0430\u0434\u0430\u0447\u0438 \u043f\u0440\u043e\u0444\u0435\u0441\u0441\u0438\u0439',
            },
        ),
    ]
