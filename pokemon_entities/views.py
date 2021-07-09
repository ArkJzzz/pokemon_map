import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def get_pokemon_img_url(request, pokemon):
    if pokemon.image:
        return request.build_absolute_uri(pokemon.image.url)
    else:
        return DEFAULT_IMAGE_URL


def get_previous_evolution(request, pokemon):
    if pokemon.previous_evolution:
        return {
                'pokemon_id': pokemon.previous_evolution.id,
                'title_ru': pokemon.previous_evolution.title_ru,
                'img_url': get_pokemon_img_url(request, pokemon.previous_evolution)
            }


def get_next_evolution(request, pokemon):
    next_evolutions = pokemon.next_evolutions.all()
    if next_evolutions:
        next_evolution = next_evolutions[0]
        return {
                'pokemon_id': next_evolution.id,
                'title_ru': next_evolution.title_ru,
                'img_url': get_pokemon_img_url(request, next_evolution)
            }


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons_on_page = []

    for pokemon in pokemons:
        pokemon_img_url = get_pokemon_img_url(request, pokemon)
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon_img_url,
            'title_ru': pokemon.title_ru,
        })

        pokemon_entities = pokemon.entities.all()
        for pokemon_entity in pokemon_entities:
            add_pokemon(
                folium_map, 
                pokemon_entity.lat,
                pokemon_entity.lon,
                pokemon_img_url,
            )

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)

    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_img_url = get_pokemon_img_url(request, pokemon)
    pokemon_entities = pokemon.entities.all()
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, 
            pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_img_url,
        )

    requested_pokemon = {
        'pokemon_id': pokemon.id,
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'img_url': pokemon_img_url,
        'description': pokemon.description,
        'next_evolution': get_next_evolution(request, pokemon),
        'previous_evolution': get_previous_evolution(request, pokemon),
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 
        'pokemon': requested_pokemon,
    })






