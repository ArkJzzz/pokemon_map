from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name='Название на русском')
    title_en = models.CharField(max_length=200, verbose_name='Название на английском', blank=True)
    title_jp = models.CharField(max_length=200, verbose_name='Название на японском', blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    image = models.ImageField(upload_to='pokemon_images', null=True, blank=True, verbose_name='Изображение')
    previous_evolution = models.ForeignKey(
                'self', 
                verbose_name='Из кого эволюционирует',
                related_name='next_evolutions', 
                null=True, blank=True, 
                on_delete=models.SET_NULL
            )

    def __str__(self):
        return f'{self.title_ru}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(null=True, blank=True, verbose_name='Когда появится')
    disappeared_at = models.DateTimeField(null=True, blank=True, verbose_name='Когда пропадет')
    level = models.IntegerField(null=True, blank=True, verbose_name='Уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(null=True, blank=True, verbose_name='Атака')
    defence = models.IntegerField(null=True, blank=True, verbose_name='Защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='Выносливость')