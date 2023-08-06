
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from .api.ability_api import AbilityApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from openapi_client.api.ability_api import AbilityApi
from openapi_client.api.berry_api import BerryApi
from openapi_client.api.berry_firmness_api import BerryFirmnessApi
from openapi_client.api.berry_flavor_api import BerryFlavorApi
from openapi_client.api.characteristic_api import CharacteristicApi
from openapi_client.api.contest_effect_api import ContestEffectApi
from openapi_client.api.contest_type_api import ContestTypeApi
from openapi_client.api.egg_group_api import EggGroupApi
from openapi_client.api.encounter_condition_api import EncounterConditionApi
from openapi_client.api.encounter_condition_value_api import EncounterConditionValueApi
from openapi_client.api.encounter_method_api import EncounterMethodApi
from openapi_client.api.evolution_chain_api import EvolutionChainApi
from openapi_client.api.evolution_trigger_api import EvolutionTriggerApi
from openapi_client.api.gender_api import GenderApi
from openapi_client.api.generation_api import GenerationApi
from openapi_client.api.growth_rate_api import GrowthRateApi
from openapi_client.api.item_api import ItemApi
from openapi_client.api.item_attribute_api import ItemAttributeApi
from openapi_client.api.item_category_api import ItemCategoryApi
from openapi_client.api.item_fling_effect_api import ItemFlingEffectApi
from openapi_client.api.item_pocket_api import ItemPocketApi
from openapi_client.api.language_api import LanguageApi
from openapi_client.api.location_api import LocationApi
from openapi_client.api.location_area_api import LocationAreaApi
from openapi_client.api.machine_api import MachineApi
from openapi_client.api.move_api import MoveApi
from openapi_client.api.move_ailment_api import MoveAilmentApi
from openapi_client.api.move_battle_style_api import MoveBattleStyleApi
from openapi_client.api.move_category_api import MoveCategoryApi
from openapi_client.api.move_damage_class_api import MoveDamageClassApi
from openapi_client.api.move_learn_method_api import MoveLearnMethodApi
from openapi_client.api.move_target_api import MoveTargetApi
from openapi_client.api.nature_api import NatureApi
from openapi_client.api.pal_park_area_api import PalParkAreaApi
from openapi_client.api.pokeathlon_stat_api import PokeathlonStatApi
from openapi_client.api.pokedex_api import PokedexApi
from openapi_client.api.pokemon_api import PokemonApi
from openapi_client.api.pokemon_color_api import PokemonColorApi
from openapi_client.api.pokemon_form_api import PokemonFormApi
from openapi_client.api.pokemon_habitat_api import PokemonHabitatApi
from openapi_client.api.pokemon_shape_api import PokemonShapeApi
from openapi_client.api.pokemon_species_api import PokemonSpeciesApi
from openapi_client.api.region_api import RegionApi
from openapi_client.api.stat_api import StatApi
from openapi_client.api.super_contest_effect_api import SuperContestEffectApi
from openapi_client.api.type_api import TypeApi
from openapi_client.api.version_api import VersionApi
from openapi_client.api.version_group_api import VersionGroupApi
