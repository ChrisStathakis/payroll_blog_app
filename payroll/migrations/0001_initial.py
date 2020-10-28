# Generated by Django 2.2 on 2020-10-28 19:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=64)),
                ('notes', models.TextField(blank=True, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=50)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=64, unique=True)),
                ('phone', models.CharField(blank=True, max_length=10)),
                ('phone1', models.CharField(blank=True, max_length=10)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=50)),
                ('value_per_hour', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('extra_per_hour', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('monthly_salary', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('occupation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='payroll.Occupation', verbose_name='Απασχόληση')),
            ],
        ),
        migrations.CreateModel(
            name='PersonSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateTimeField(verbose_name='From')),
                ('date_end', models.DateTimeField(verbose_name='Until')),
                ('hours', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('category', models.CharField(choices=[('a', 'Normal Time'), ('b', 'Extra time')], default='a', max_length=1)),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=20, max_length=20)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='payroll.Person')),
            ],
            options={
                'ordering': ['-date_start'],
            },
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('date_expired', models.DateField(default=django.utils.timezone.now)),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('taxes', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('paid_value', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('final_value', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('is_paid', models.BooleanField(default=True)),
                ('printed', models.BooleanField(default=False)),
                ('title', models.CharField(blank=True, max_length=150)),
                ('category', models.CharField(choices=[('1', 'Salary'), ('2', 'Extra')], default='1', max_length=1)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='person_invoices', to='payroll.Person')),
            ],
            options={
                'ordering': ['is_paid', '-date_expired'],
            },
        ),
    ]
