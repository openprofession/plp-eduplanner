# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('plp_eduplanner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=200, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('annotation', models.CharField(max_length=200, verbose_name='\u0410\u043d\u043d\u043e\u0442\u0430\u0446\u0438\u044f')),
                ('is_public', models.BooleanField(default=True, db_index=True, verbose_name='\u041f\u0443\u0431\u043b\u0438\u0447\u043d\u044b\u0439')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', verbose_name='\u0420\u043e\u0434\u0438\u0442\u0435\u043b\u044c', blank=True, to='plp_eduplanner.Competence', null=True)),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043c\u043f\u0435\u0442\u0435\u043d\u0446\u0438\u044f',
                'verbose_name_plural': '\u041a\u043e\u043c\u043f\u0435\u0442\u0435\u043d\u0446\u0438\u0438',
            },
        ),
        migrations.AlterUniqueTogether(
            name='competition',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='competition',
            name='parent',
        ),
        migrations.AlterModelOptions(
            name='coursecomp',
            options={'verbose_name': '\u041a\u043e\u043c\u043f\u0435\u0442\u0435\u043d\u0446\u0438\u044f \u043a\u0443\u0440\u0441\u0430', 'verbose_name_plural': '\u041a\u043e\u043c\u043f\u0435\u0442\u0435\u043d\u0446\u0438\u0438 \u043a\u0443\u0440\u0441\u043e\u0432'},
        ),
        migrations.AlterModelOptions(
            name='profession',
            options={'ordering': ['-title'], 'verbose_name': '\u041f\u0440\u043e\u0444\u0435\u0441\u0441\u0438\u044f', 'verbose_name_plural': '\u041f\u0440\u043e\u0444\u0435\u0441\u0441\u0438\u0438'},
        ),
        migrations.AlterModelOptions(
            name='professioncomp',
            options={'verbose_name': '\u041a\u043e\u043c\u043f\u0435\u0442\u0435\u043d\u0446\u0438\u044f \u043f\u0440\u043e\u0444\u0435\u0441\u0441\u0438\u0438', 'verbose_name_plural': '\u041a\u043e\u043c\u043f\u0435\u0442\u0435\u043d\u0446\u0438\u044f \u043f\u0440\u043e\u0444\u0435\u0441\u0441\u0438\u0439'},
        ),
        migrations.AlterModelOptions(
            name='usercomp',
            options={'verbose_name': '\u041a\u043e\u043c\u043f\u0435\u0442\u0435\u043d\u0446\u0438\u044f \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f', 'verbose_name_plural': '\u041a\u043e\u043c\u043f\u0435\u0442\u0435\u043d\u0446\u0438\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439'},
        ),
        migrations.AlterField(
            model_name='coursecomp',
            name='comp',
            field=models.ForeignKey(verbose_name='\u041a\u043e\u043c\u043f\u0435\u0442\u0435\u043d\u0446\u0438\u044f', to='plp_eduplanner.Competence'),
        ),
        migrations.AlterField(
            model_name='coursecomp',
            name='course',
            field=models.ForeignKey(verbose_name='\u041a\u0443\u0440\u0441', to='plp.Course'),
        ),
        migrations.AlterField(
            model_name='coursecomp',
            name='rate',
            field=models.SmallIntegerField(default=1, verbose_name='\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435', validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='profession',
            name='description',
            field=models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='profession',
            name='is_public',
            field=models.BooleanField(default=True, db_index=True, verbose_name='\u041f\u0443\u0431\u043b\u0438\u0447\u043d\u044b\u0439'),
        ),
        migrations.AlterField(
            model_name='profession',
            name='title',
            field=models.CharField(max_length=200, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a'),
        ),
        migrations.AlterField(
            model_name='professioncomp',
            name='comp',
            field=models.ForeignKey(verbose_name='\u041a\u043e\u043c\u043f\u0435\u0442\u0435\u043d\u0446\u0438\u044f', to='plp_eduplanner.Competence'),
        ),
        migrations.AlterField(
            model_name='professioncomp',
            name='profession',
            field=models.ForeignKey(verbose_name='\u041f\u0440\u043e\u0444\u0435\u0441\u0438\u044f', to='plp_eduplanner.Profession'),
        ),
        migrations.AlterField(
            model_name='professioncomp',
            name='rate',
            field=models.SmallIntegerField(default=1, verbose_name='\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435', validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='usercomp',
            name='comp',
            field=models.ForeignKey(verbose_name='\u041a\u043e\u043c\u043f\u0435\u0442\u0435\u043d\u0446\u0438\u044f', to='plp_eduplanner.Competence'),
        ),
        migrations.AlterField(
            model_name='usercomp',
            name='rate',
            field=models.SmallIntegerField(default=1, verbose_name='\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435', validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='usercomp',
            name='user',
            field=models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Competition',
        ),
        migrations.AlterUniqueTogether(
            name='competence',
            unique_together=set([('id', 'parent')]),
        ),
    ]
