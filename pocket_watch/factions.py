"""
Factions that operate across the many dimensions.

All faction names are pseudonyms.  No real-world organisations, criminal
entities, or individuals are referenced or implied.  The factions exist
purely within the fiction of the pocket-watch multiverse.
"""

from dataclasses import dataclass, field


@dataclass
class Faction:
    """Represents one of the eight known multidimensional factions."""

    pseudonym: str
    motto: str
    domain: str
    allegiance: str  # 'order', 'chaos', or 'neutral'
    known_dimensions: list[str] = field(default_factory=list)
    description: str = ""

    def __str__(self) -> str:
        return (
            f"[{self.pseudonym}]\n"
            f"  Motto      : {self.motto}\n"
            f"  Domain     : {self.domain}\n"
            f"  Allegiance : {self.allegiance}\n"
            f"  Dimensions : {', '.join(self.known_dimensions) or 'undisclosed'}\n"
            f"  About      : {self.description}"
        )


# ---------------------------------------------------------------------------
# The eight known factions
# ---------------------------------------------------------------------------

FACTIONS: list[Faction] = [
    Faction(
        pseudonym="The Clockmakers",
        motto="Every second is sovereign.",
        domain="Temporal mechanics and relic crafting",
        allegiance="order",
        known_dimensions=["The Wound", "The Still Hour"],
        description=(
            "The Clockmakers are the oldest known faction.  They forge the "
            "devices — including pocket watches — that make dimensional travel "
            "possible.  They guard the blueprints jealously and levy heavy tolls "
            "on those who seek passage."
        ),
    ),
    Faction(
        pseudonym="The Void Walkers",
        motto="Between the worlds, we are the world.",
        domain="Free-range interdimensional transit",
        allegiance="neutral",
        known_dimensions=["The Seam", "The Fold", "The Rift Corridor"],
        description=(
            "Nomads who exist in the spaces between dimensions.  They neither "
            "claim territory nor recognise borders drawn by other factions.  "
            "Regarded with equal parts awe and suspicion by every other group."
        ),
    ),
    Faction(
        pseudonym="The Architects",
        motto="We laid the roads you walk.",
        domain="Construction and maintenance of dimensional pathways",
        allegiance="order",
        known_dimensions=["The Blueprint Layer", "Foundation Zero"],
        description=(
            "Believed to have authored the original lattice of pathways that "
            "connect dimensions.  The Architects treat the multiverse as "
            "infrastructure — to be maintained, expanded, and above all, "
            "controlled."
        ),
    ),
    Faction(
        pseudonym="The Anchors",
        motto="The line must hold.",
        domain="Timeline stabilisation and paradox containment",
        allegiance="order",
        known_dimensions=["The Fixed Point", "Terminus"],
        description=(
            "Where paradoxes threaten to unravel a dimension, the Anchors "
            "arrive.  They are peacekeepers of causality, driving temporal "
            "stakes into unstable events to prevent cascade collapse."
        ),
    ),
    Faction(
        pseudonym="The Echoes",
        motto="We are what remains.",
        domain="Salvage and memory preservation of collapsed timelines",
        allegiance="neutral",
        known_dimensions=["The Grey Archive", "Residue"],
        description=(
            "When a dimension collapses, the Echoes are already there, "
            "recording the last moments and rescuing stranded travellers.  "
            "They hoard knowledge from dead realities and trade in "
            "dimensional histories."
        ),
    ),
    Faction(
        pseudonym="The Sovereign Fold",
        motto="Territory is truth.",
        domain="Dimensional territory acquisition and governance",
        allegiance="chaos",
        known_dimensions=["The Dominion", "Crown Axis", "Deep Ledge"],
        description=(
            "The Sovereign Fold claim ownership of large swaths of the "
            "multiverse and extract tribute from travellers who pass through "
            "their declared space.  Their borders shift without warning and "
            "their edicts are enforced by agents who answer to no single "
            "timeline's law."
        ),
    ),
    Faction(
        pseudonym="The Pale Circuit",
        motto="Signal over flesh.",
        domain="Dimensional communication and data extraction",
        allegiance="neutral",
        known_dimensions=["Node Prime", "The Wire", "Static"],
        description=(
            "A technology-first collective that has wired many dimensions "
            "together through an invisible network called the Circuit.  They "
            "trade in information — dimensional coordinates, paradox maps, "
            "and traveller profiles — rather than in physical goods."
        ),
    ),
    Faction(
        pseudonym="The Driftborn",
        motto="Born nowhere, belonging everywhere.",
        domain="Advocacy for dimension-displaced persons",
        allegiance="chaos",
        known_dimensions=["The Between", "Scatter"],
        description=(
            "Individuals born in transit — in the space between dimensions — "
            "who have no native reality to return to.  The Driftborn operate "
            "as a loose coalition that fights for the rights of those lost to "
            "dimensional displacement and occasionally destabilises "
            "Sovereign Fold operations out of principle."
        ),
    ),
]


def get_faction(pseudonym: str) -> Faction:
    """Return a faction by its pseudonym (case-insensitive)."""
    needle = pseudonym.strip().lower()
    for faction in FACTIONS:
        if faction.pseudonym.lower() == needle:
            return faction
    raise KeyError(f"No faction found with pseudonym '{pseudonym}'.")
