"""
Pocket Watch — A multidimensional travel management system.

Entry point to the dimension-hopping world discovered through a single
relic pulled from the coat of a dead soldier on a forgotten battlefield.
"""

from .factions import FACTIONS, Faction
from .paradox_engine import ParadoxEngine, ParadoxType
from .dimensions import DimensionRegistry, Dimension, TravelRecord
from .keeper import Keeper
from .story import origin_story

__all__ = [
    "FACTIONS",
    "Faction",
    "ParadoxEngine",
    "ParadoxType",
    "DimensionRegistry",
    "Dimension",
    "TravelRecord",
    "Keeper",
    "origin_story",
]
