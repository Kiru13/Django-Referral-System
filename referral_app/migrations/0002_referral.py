# Generated by Django 3.1.6 on 2021-02-19 09:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('referral_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_email', models.EmailField(max_length=100)),
                ('status', models.CharField(default='referred', max_length=20)),
                ('referred_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referred_to', to=settings.AUTH_USER_MODEL)),
                ('referrer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referrer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]