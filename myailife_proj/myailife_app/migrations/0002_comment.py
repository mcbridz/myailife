# Generated by Django 3.1.1 on 2021-02-24 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myailife_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('is_reply', models.BooleanField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comments', to='myailife_app.post')),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='replies', to='myailife_app.comment')),
            ],
        ),
    ]
