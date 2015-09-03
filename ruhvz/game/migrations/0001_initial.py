# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import geoposition.fields
import ruhvz.game.models
import mptt.fields
import django.db.models.deletion
from django.conf import settings
import ruhvz.overwrite_fs


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('points', models.IntegerField(help_text=b'Can be negative, e.g. to penalize players')),
                ('code', models.CharField(help_text=b'leave blank for automatic (re-)generation', max_length=255, blank=True)),
                ('redeem_limit', models.IntegerField(help_text=b'Maximum number of players that can redeem award via code entry (set to 0 for awards to be added by moderators only)')),
                ('redeem_type', models.CharField(max_length=1, choices=[(b'H', b'Humans only'), (b'Z', b'Zombies only'), (b'A', b'All players')])),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('registration_date', models.DateTimeField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('rules', models.FileField(storage=ruhvz.overwrite_fs.OverwriteFileSystemStorage(), upload_to=ruhvz.game.models.gen_rules_filename)),
                ('color', models.CharField(default=b'#FFFFFF', max_length=64)),
                ('flavor_h', models.TextField(default=b'', max_length=6000)),
                ('flavor_z', models.TextField(default=b'', max_length=6000)),
            ],
            options={
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='HighValueDorm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dorm', models.CharField(max_length=4, choices=[(b'ALL', b'Allan Webb'), (b'COU', b'Courtenay-Latimer'), (b'DES', b'Desmond Tutu'), (b'DRO', b'Drostdy'), (b'FOU', b'Founders'), (b'HOB', b'Hobson'), (b'JAN', b'Jan Smuts'), (b'KIM', b'Kimberley'), (b'LIL', b'Lilian Ngoyi'), (b'MIR', b'Miriam Makeba'), (b'NEL', b'Nelson Mandela'), (b'OPP', b'Oppidan'), (b'STM', b'St Mary')])),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('points', models.IntegerField(default=3)),
                ('game', models.ForeignKey(to='game.Game')),
            ],
        ),
        migrations.CreateModel(
            name='HighValueTarget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('kill_points', models.IntegerField(default=5, help_text=b'# of points zombies receive for killing this HVT')),
                ('award_points', models.IntegerField(default=3, help_text=b'# of points the HVT earns if he/she survives for the entire duration')),
            ],
        ),
        migrations.CreateModel(
            name='Kill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('points', models.IntegerField(default=1)),
                ('notes', models.TextField(blank=True)),
                ('pos', geoposition.fields.GeopositionField(max_length=42, null=True, verbose_name=b'position', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('hvd', models.ForeignKey(related_name='kills', on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'High-value Dorm', blank=True, to='game.HighValueDorm', null=True)),
                ('hvt', models.OneToOneField(related_name='kill', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='game.HighValueTarget', verbose_name=b'High-value target')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('pos', geoposition.fields.GeopositionField(max_length=42, null=True, verbose_name=b'position', blank=True)),
                ('img', models.CharField(max_length=100, choices=[(b'/static/img/mission_markers/bag.png', b'Bag'), (b'/static/img/mission_markers/bottle.png', b'Bottle'), (b'/static/img/mission_markers/food.png', b'Food'), (b'/static/img/mission_markers/hospital.png', b'Hospital'), (b'/static/img/mission_markers/medical.png', b'Medical'), (b'/static/img/mission_markers/petrol.png', b'Petrol'), (b'/static/img/mission_markers/pills.png', b'Pills'), (b'/static/img/mission_markers/plane.png', b'Plane'), (b'/static/img/mission_markers/tools.png', b'Tools'), (b'/static/img/mission_markers/tooth.png', b'Tooth')])),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('def_points', models.IntegerField(help_text=b'Can be negative, e.g. to penalize players')),
                ('def_redeem_limit', models.IntegerField(help_text=b'Maximum number of players that can redeem award via code entry (set to 0 for awards to be added by moderators only)')),
                ('def_redeem_type', models.CharField(max_length=1, choices=[(b'H', b'Humans only'), (b'Z', b'Zombies only'), (b'A', b'All players')])),
                ('game', models.ForeignKey(related_name='+', to='game.Game')),
            ],
        ),
        migrations.CreateModel(
            name='New_Squad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('game', models.ForeignKey(related_name='new_squads', to='game.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=False)),
                ('bite_code', models.CharField(help_text=b'leave blank for automatic (re-)generation', max_length=255, blank=True)),
                ('dorm', models.CharField(max_length=4, choices=[(b'ALL', b'Allan Webb'), (b'COU', b'Courtenay-Latimer'), (b'DES', b'Desmond Tutu'), (b'DRO', b'Drostdy'), (b'FOU', b'Founders'), (b'HOB', b'Hobson'), (b'JAN', b'Jan Smuts'), (b'KIM', b'Kimberley'), (b'LIL', b'Lilian Ngoyi'), (b'MIR', b'Miriam Makeba'), (b'NEL', b'Nelson Mandela'), (b'OPP', b'Oppidan'), (b'STM', b'St Mary')])),
                ('major', models.CharField(help_text=b'autopopulates from LDAP', max_length=255, blank=True)),
                ('human', models.BooleanField(default=True)),
                ('opt_out_hvt', models.BooleanField(default=False)),
                ('gun_requested', models.BooleanField(default=False)),
                ('renting_gun', models.BooleanField(default=False)),
                ('gun_returned', models.BooleanField(default=False)),
                ('last_words', models.CharField(max_length=255, blank=True)),
                ('game', models.ForeignKey(related_name='players', to='game.Game')),
                ('new_squad', models.ForeignKey(related_name='players', blank=True, to='game.New_Squad', null=True)),
            ],
            options={
                'ordering': ['-game__start_date', 'user__username', 'user__last_name', 'user__first_name'],
            },
        ),
        migrations.CreateModel(
            name='Squad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('game', models.ForeignKey(related_name='squads', to='game.Game')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='squad',
            field=models.ForeignKey(related_name='players', blank=True, to='game.Squad', null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='kill',
            name='killer',
            field=models.ForeignKey(related_name='+', to='game.Player'),
        ),
        migrations.AddField(
            model_name='kill',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', blank=True, editable=False, to='game.Kill', null=True),
        ),
        migrations.AddField(
            model_name='kill',
            name='victim',
            field=models.ForeignKey(related_name='+', to='game.Player'),
        ),
        migrations.AddField(
            model_name='highvaluetarget',
            name='player',
            field=models.OneToOneField(related_name='hvt', to='game.Player'),
        ),
        migrations.AddField(
            model_name='award',
            name='game',
            field=models.ForeignKey(related_name='+', to='game.Game'),
        ),
        migrations.AddField(
            model_name='award',
            name='group',
            field=models.ForeignKey(related_name='mission', blank=True, to='game.Mission', null=True),
        ),
        migrations.AddField(
            model_name='award',
            name='players',
            field=models.ManyToManyField(help_text=b'Players that should receive this award.', related_name='awards', null=True, to='game.Player', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='squad',
            unique_together=set([('game', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([('game', 'bite_code'), ('user', 'game')]),
        ),
        migrations.AlterUniqueTogether(
            name='new_squad',
            unique_together=set([('game', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='mission',
            unique_together=set([('game', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='kill',
            unique_together=set([('parent', 'killer', 'victim')]),
        ),
        migrations.AlterUniqueTogether(
            name='highvaluedorm',
            unique_together=set([('game', 'dorm')]),
        ),
        migrations.AlterUniqueTogether(
            name='award',
            unique_together=set([('game', 'code')]),
        ),
    ]
