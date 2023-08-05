# flake8: noqa: F405
import re
from io import StringIO

import pytest
from requests import Request
from requests_cache import CachedResponse
from rich.console import Console
from rich.table import Table

from pyinaturalist.constants import API_V0_BASE_URL
from pyinaturalist.formatters import *
from test.sample_data import *

# Lists of JSON records that can be formatted into tables
TABULAR_RESPONSES = [
    j_comments,
    [j_controlled_term_1, j_controlled_term_2],
    [j_identification_1, j_identification_2],
    [j_observation_1, j_observation_2],
    j_obs_species_counts,
    j_life_list,
    [j_listed_taxon_1, j_listed_taxon_2_partial],
    [j_message],
    [j_photo_1, j_photo_2_partial],
    [j_place_1, j_place_2],
    j_places_nearby,
    [j_project_1, j_project_2],
    j_search_results,
    [j_taxon_1, j_taxon_2_partial],
    [j_user_1, j_user_2_partial],
]


def get_variations(response_object):
    """Formatting functions should accept any of these variations"""
    return [{'results': [response_object]}, [response_object], response_object]


# TODO: More thorough tests for table content
@pytest.mark.parametrize('response', TABULAR_RESPONSES)
def test_format_table(response):
    table = format_table(response)
    assert isinstance(table, Table)

    def _get_id(value):
        return str(
            value.get('id') or value.get('record', {}).get('id') or value.get('taxon', {}).get('id')
        )

    # Just make sure at least object IDs show up in the table
    console = Console()
    rendered = '\n'.join([str(line) for line in console.render_lines(table)])

    if isinstance(response, list):
        assert all([_get_id(value) in rendered for value in response])

    # for obj in response:
    #     assert all([value in rendered_table for value in obj.row.values()])


def test_format_table__unknown_type():
    with pytest.raises(ValueError):
        format_table({'foo': 'bar'})


# TODO: Test content written to stdout. For now, just make sure it doesn't explode.
@pytest.mark.parametrize('response', TABULAR_RESPONSES)
def test_pprint(response):
    console = Console(force_terminal=False, width=120)
    with console.capture() as output:
        pprint(response)
    rendered = output.get()


@pytest.mark.parametrize('input', get_variations(j_controlled_term_1))
def test_format_controlled_terms(input):
    assert (
        format_controlled_terms(input)
        == '[12] Plant Phenology: No Evidence of Flowering, Flowering, Fruiting, Flower Budding'
    )


@pytest.mark.parametrize('input', get_variations(j_identification_1))
def test_format_identifications(input):
    expected_str = '[155554373] 🌼 Species: 60132 (supporting) added on Feb 18, 2021 by jkcook'
    assert format_identifications(input) == expected_str


@pytest.mark.parametrize('input', get_variations(j_observation_1))
def test_format_observation(input):
    expected_str = (
        '[16227955] 🪲 Species: Lixus bardanae observed on Sep 05, 2018 '
        'by niconoe at 54 rue des Badauds'
    )
    assert format_observations(input) == expected_str


@pytest.mark.parametrize('input', get_variations(j_project_1))
def test_format_projects(input):
    expected_str = '[8291] PNW Invasive Plant EDDR'
    assert format_projects(input) == expected_str


@pytest.mark.parametrize('input', get_variations(j_place_1))
def test_format_places(input):
    expected_str = '[89191] Conservation Area Riversdale'
    assert format_places(input) == expected_str


def test_format_places__nearby():
    places_str = """
[97394] North America
[97395] Asia
[97393] Oceania
[11770] Mehedinti
[119755] Mahurangi College
[150981] Ceap Breatainn
""".strip()
    assert format_places(j_places_nearby) == places_str


def test_format_search_results():
    expected_str = (
        '[Taxon] [47792] 🐛 Order: Odonata (Dragonflies and Damselflies)\n'
        '[Place] [113562] Odonates of Peninsular India and Sri Lanka\n'
        '[Project] [9978] Ohio Dragonfly Survey  (Ohio Odonata Survey)\n'
        '[User] [113886] odonatanb (Gilles Belliveau)'
    )
    assert format_search_results(j_search_results) == expected_str


@pytest.mark.parametrize('input', get_variations(j_species_count_1))
def test_format_species_counts(input):
    expected_str = '[48484] 🐞 Species: Harmonia axyridis (Asian Lady Beetle): 31'
    assert format_species_counts(input) == expected_str


@pytest.mark.parametrize('input', get_variations(j_taxon_1))
def test_format_taxa__with_common_name(input):
    expected_str = '[70118] 🪲 Species: Nicrophorus vespilloides (Lesser Vespillo Burying Beetle)'
    assert format_taxa(input) == expected_str


@pytest.mark.parametrize('input', get_variations(j_taxon_3_no_common_name))
def test_format_taxon__without_common_name(input):
    assert format_taxa(input) == '[124162] 🪰 Species: Temnostoma vespiforme'


@pytest.mark.parametrize('input', get_variations(j_user_2_partial))
def test_format_users(input):
    expected_str = '[886482] niconoe (Nicolas Noé)'
    assert format_users(input) == expected_str


PRINTED_OBSERVATION = """
Observation(
    id=16227955,
    created_at='2018-09-05 00:00:00+01:00',
    captive=False,
    community_taxon_id=493595,
    description='',
    identifications_count=2,
    identifications_most_agree=True,
    identifications_most_disagree=False,
    identifications_some_agree=True,
    license_code='CC0',
    location=(50.646894, 4.360086),
    mappable=True,
    num_identification_agreements=2,
    num_identification_disagreements=0,
    obscured=False,
    observed_on='2018-09-05 14:06:00+01:00',
    outlinks=[{'source': 'GBIF', 'url': 'http://www.gbif.org/occurrence/1914197587'}],
    owners_identification_from_vision=True,
    place_guess='54 rue des Badauds',
    place_ids=[7008, 8657, 14999, 59614, 67952, 80627, 81490, 96372, 96794, 97391, 97582, 108692],
    positional_accuracy=23,
    preferences={'prefers_community_taxon': None},
    public_positional_accuracy=23,
    quality_grade='research',
    reviewed_by=[180811, 886482, 1226913],
    site_id=1,
    species_guess='Lixus bardanae',
    updated_at='2018-09-22 19:19:27+02:00',
    uri='https://www.inaturalist.org/observations/16227955',
    uuid='6448d03a-7f9a-4099-86aa-ca09a7740b00',
    comments=[
        'borisb on Sep 05, 2018: I now see: Bonus species on observation! You ma...',
        'borisb on Sep 05, 2018: suspect L. bardanae - but sits on Solanum (non-...'
    ],
    identifications=[
        '[34896306] 🪲 Genus: Lixus (improving) added on Sep 05, 2018 by niconoe',
        '[34926789] 🪲 Species: Lixus bardanae (improving) added on Sep 05, 2018 by borisb',
        '[36039221] 🪲 Species: Lixus bardanae (supporting) added on Sep 22, 2018 by jpreudhomme'
    ],
    photos=[
        '[24355315] https://static.inaturalist.org/photos/24355315/original.jpeg?1536150664 (CC-BY, 1445x1057)',
        '[24355313] https://static.inaturalist.org/photos/24355313/original.jpeg?1536150659 (CC-BY, 2048x1364)'
    ],
    taxon='[493595] 🪲 Species: Lixus bardanae',
    user='[886482] niconoe (Nicolas Noé)'
)
"""


def test_pretty_print():
    """Test rich.pretty with modifications, via get_model_fields()"""
    console = Console(force_terminal=False, width=120, file=StringIO())
    observation = Observation.from_json(j_observation_1)

    console.print(observation)
    rendered = console.file.getvalue()

    # Don't check for differences in indendtation
    rendered = re.sub(' +', ' ', rendered.strip())
    expected = re.sub(' +', ' ', PRINTED_OBSERVATION.strip())

    # Emoji may not correctly render in CI
    rendered = rendered.replace(r'\U0001fab2', '🪲')
    assert rendered == expected


def test_format_request():
    request = Request(
        method='GET',
        url=API_V0_BASE_URL,
        headers={'Accept': 'application/json', 'Authorization': 'password123'},
        json={'client_secret': 'password123'},
    ).prepare()
    request_str = format_request(request)
    assert API_V0_BASE_URL in request_str
    assert 'Accept: application/json' in request_str
    assert 'password123' not in request_str


def test_format_response():
    response = CachedResponse(status_code=200, expires=datetime(2021, 1, 1), headers={'Age': '0'})
    response_str = format_response(response)

    assert 'cached; expires in ' in response_str
    assert 'Age: 0' in response_str
    response.expires = None
    assert 'never expires' in format_response(response)
