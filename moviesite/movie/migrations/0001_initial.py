# Generated by Django 2.2.6 on 2019-11-16 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='演员名字')),
            ],
            options={
                'verbose_name': '演员',
                'verbose_name_plural': '演员',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='导演名字')),
            ],
            options={
                'verbose_name': '导演',
                'verbose_name_plural': '导演',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='体裁名字')),
            ],
            options={
                'verbose_name': '体裁',
                'verbose_name_plural': '体裁',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='语言')),
            ],
            options={
                'verbose_name': '语言',
                'verbose_name_plural': '语言',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IMDB_id', models.CharField(max_length=7, verbose_name='IMDB编号')),
                ('name', models.CharField(max_length=100, verbose_name='电影名字')),
                ('year', models.IntegerField(verbose_name='上映年份')),
                ('duration', models.CharField(max_length=20, verbose_name='时长')),
                ('summary', models.TextField(verbose_name='简介')),
                ('rating', models.FloatField(verbose_name='评分')),
                ('actors', models.ManyToManyField(to='movie.Actor', verbose_name='演员')),
                ('directors', models.ManyToManyField(to='movie.Director', verbose_name='导演')),
                ('genres', models.ManyToManyField(to='movie.Genre', verbose_name='体裁')),
                ('language', models.ManyToManyField(to='movie.Language', verbose_name='语言')),
            ],
            options={
                'verbose_name': '电影',
                'verbose_name_plural': '电影',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Writer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='编剧名字')),
            ],
            options={
                'verbose_name': '编剧',
                'verbose_name_plural': '编剧',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(verbose_name='权重')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.Movie', verbose_name='电影')),
            ],
            options={
                'verbose_name': '推荐电影',
                'verbose_name_plural': '推荐电影',
                'ordering': ['-weight'],
            },
        ),
        migrations.AddField(
            model_name='movie',
            name='writers',
            field=models.ManyToManyField(to='movie.Writer', verbose_name='编剧'),
        ),
    ]
