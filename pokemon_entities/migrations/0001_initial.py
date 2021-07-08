# Generated by Django 3.1.12 on 2021-06-27 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_ru', models.CharField(max_length=200)),
                ('title_en', models.CharField(max_length=200)),
                ('title_jp', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='pokemon_images')),
                ('previous_evolution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pokemon_entities.pokemon')),
            ],
        ),
        migrations.CreateModel(
            name='PokemonEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('appeared_at', models.DateTimeField(null=True)),
                ('disappeared_at', models.DateTimeField(null=True)),
                ('level', models.IntegerField(null=True)),
                ('health', models.IntegerField(null=True)),
                ('strength', models.IntegerField(null=True)),
                ('defence', models.IntegerField(null=True)),
                ('stamina', models.IntegerField(null=True)),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokemon_entities.pokemon')),
            ],
        ),
    ]
