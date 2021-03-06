# Generated by Django 2.1.2 on 2018-10-31 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('content', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('published_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '공지사항',
                'verbose_name_plural': '공지사항 목록',
                'ordering': ['-created_date'],
            },
        ),
    ]
