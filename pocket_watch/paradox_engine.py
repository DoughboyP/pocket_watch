"""
Paradox Engine — identifies, classifies, and resolves time-travel paradoxes.

Seven canonical paradox types are recognised by the system.  Each has an
associated resolution strategy enforced by The Anchors and encoded into
every Clockmaker-built relic.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class ParadoxType(Enum):
    """Enumeration of known time-travel and dimensional paradox types."""

    GRANDFATHER = auto()
    BOOTSTRAP = auto()
    PREDESTINATION = auto()
    BUTTERFLY = auto()
    TEMPORAL_TWIN = auto()
    INFORMATION = auto()
    ONTOLOGICAL = auto()


@dataclass
class ParadoxResolution:
    """Describes how a specific paradox type is resolved within the system."""

    paradox_type: ParadoxType
    name: str
    description: str
    resolution_strategy: str
    resolution_name: str

    def __str__(self) -> str:
        return (
            f"[{self.name}]\n"
            f"  Type        : {self.paradox_type.name}\n"
            f"  Description : {self.description}\n"
            f"  Resolution  : {self.resolution_name}\n"
            f"  How         : {self.resolution_strategy}"
        )


_RESOLUTIONS: dict[ParadoxType, ParadoxResolution] = {
    ParadoxType.GRANDFATHER: ParadoxResolution(
        paradox_type=ParadoxType.GRANDFATHER,
        name="Grandfather Paradox",
        description=(
            "A traveller takes an action in the past that would prevent their "
            "own existence or the existence of the very cause that sent them "
            "there — creating a logical impossibility."
        ),
        resolution_name="Branching Timeline Protocol",
        resolution_strategy=(
            "The moment a contradictory action is completed, the dimension "
            "forks into a new branch.  The original timeline continues "
            "unaltered; the new branch contains the consequences of the "
            "action.  The traveller now inhabits a parallel dimension rather "
            "than the one they departed from.  The Anchors mark both branch "
            "points with temporal stakes to prevent re-merging."
        ),
    ),
    ParadoxType.BOOTSTRAP: ParadoxResolution(
        paradox_type=ParadoxType.BOOTSTRAP,
        name="Bootstrap Paradox (Causal Loop)",
        description=(
            "An object or piece of information exists in a closed loop with "
            "no discernible origin — it is given to someone in the past by a "
            "future version of themselves, so it was never independently "
            "created."
        ),
        resolution_name="Conservation Loop Seal",
        resolution_strategy=(
            "The Pale Circuit's network assigns every looping object or "
            "datum an Origination Hash.  On each cycle, a tiny quantity of "
            "entropic decay is added to the hash so that the loop is not "
            "truly closed — it is an extremely tight helix rather than a "
            "perfect circle.  After enough cycles the object degrades to "
            "its base state and the loop terminates naturally."
        ),
    ),
    ParadoxType.PREDESTINATION: ParadoxResolution(
        paradox_type=ParadoxType.PREDESTINATION,
        name="Predestination Paradox",
        description=(
            "A traveller goes back in time believing they are changing "
            "events, only to discover that their actions were the very cause "
            "of the events they sought to influence — they were always "
            "supposed to be there."
        ),
        resolution_name="Fixed-Point Acknowledgment",
        resolution_strategy=(
            "The Keeper's Registry flags certain events as Fixed Points — "
            "nodes in the causal fabric so dense that every path through "
            "the multiverse routes through them.  Travellers are warned "
            "before approach.  Attempting to alter a Fixed Point simply "
            "re-routes the traveller through events that produce the "
            "same outcome via a different path.  Resistance is filed as "
            "a resolved predestination case."
        ),
    ),
    ParadoxType.BUTTERFLY: ParadoxResolution(
        paradox_type=ParadoxType.BUTTERFLY,
        name="Butterfly Effect Cascade",
        description=(
            "A small, seemingly inconsequential action in the past amplifies "
            "through the causal chain into massive, unpredictable changes "
            "in the present — potentially unravelling entire dimensions."
        ),
        resolution_name="Dampening Node Deployment",
        resolution_strategy=(
            "The Anchors maintain a grid of Dampening Nodes throughout "
            "high-traffic temporal zones.  Each node absorbs stray causal "
            "ripples and redistributes their energy across low-sensitivity "
            "areas of the timeline.  Travellers who trigger a cascade are "
            "automatically re-routed to a quarantine branch and debriefed "
            "before re-entry to the prime dimension."
        ),
    ),
    ParadoxType.TEMPORAL_TWIN: ParadoxResolution(
        paradox_type=ParadoxType.TEMPORAL_TWIN,
        name="Temporal Twin Paradox",
        description=(
            "A traveller meets a past or future version of themselves.  The "
            "interaction risks an identity collapse — each version attempting "
            "to occupy the same causal role — or the creation of a divergent "
            "duplicate who cannot be integrated back."
        ),
        resolution_name="Identity Divergence Protocol",
        resolution_strategy=(
            "When a registered traveller's biometric signature overlaps with "
            "a previous reading within the same dimension, the pocket watch "
            "automatically phases one instance into a Temporal Offset — a "
            "microsecond displacement that prevents physical and causal "
            "overlap.  Both instances are assigned distinct Registry IDs for "
            "the duration of the encounter.  The Void Walkers provide escort "
            "to ensure safe separation."
        ),
    ),
    ParadoxType.INFORMATION: ParadoxResolution(
        paradox_type=ParadoxType.INFORMATION,
        name="Information Paradox",
        description=(
            "Information that could not have existed at a given point in "
            "time is introduced there, altering the development of "
            "technology, events, or beliefs in ways that corrupt the "
            "natural progression of the timeline."
        ),
        resolution_name="Dimensional Echo Storage",
        resolution_strategy=(
            "The Echoes maintain the Grey Archive — a repository of "
            "information sorted by the dimension and timestamp at which it "
            "legitimately first appeared.  Before a traveller carries any "
            "knowledge forward or backward, it is checked against the "
            "Archive.  Anachronistic knowledge is quarantined in a sealed "
            "echo layer, inaccessible to the timeline's native population, "
            "until the natural discovery date is reached."
        ),
    ),
    ParadoxType.ONTOLOGICAL: ParadoxResolution(
        paradox_type=ParadoxType.ONTOLOGICAL,
        name="Ontological Paradox",
        description=(
            "An object, person, or concept exists without any point of "
            "creation — it passes through time in a loop, so it was never "
            "made, born, or invented by anyone.  Its origin is itself."
        ),
        resolution_name="Origination Anchor",
        resolution_strategy=(
            "The Clockmakers embed an Origination Anchor into every relic "
            "they build.  If that relic is ever detected looping without a "
            "discernible first-creation event, the Keeper's Registry "
            "forcibly materialises a creation record at the earliest point "
            "the object appears, assigning a Clockmaker workshop and "
            "manufacture timestamp.  This breaks the loop by providing a "
            "legitimate origin."
        ),
    ),
}


class ParadoxEngine:
    """
    Detects and resolves dimensional paradoxes.

    The engine is embedded in every pocket watch and consulted whenever
    a travel request is submitted to the Keeper's Registry.
    """

    def __init__(self) -> None:
        self._resolutions: dict[ParadoxType, ParadoxResolution] = dict(_RESOLUTIONS)
        self._case_log: list[dict] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_resolution(self, paradox_type: ParadoxType) -> ParadoxResolution:
        """Return the resolution strategy for a given paradox type."""
        return self._resolutions[paradox_type]

    def all_resolutions(self) -> list[ParadoxResolution]:
        """Return all known paradox resolutions."""
        return list(self._resolutions.values())

    def log_case(
        self,
        traveller_id: str,
        dimension_id: str,
        paradox_type: ParadoxType,
        notes: str = "",
    ) -> dict:
        """
        Record a paradox event and return the resolution record.

        Parameters
        ----------
        traveller_id:
            Registry ID of the traveller involved.
        dimension_id:
            The dimension in which the paradox was detected.
        paradox_type:
            Which type of paradox was triggered.
        notes:
            Optional context captured by the pocket watch.

        Returns
        -------
        dict
            A case record including the applied resolution.
        """
        resolution = self.get_resolution(paradox_type)
        case = {
            "traveller_id": traveller_id,
            "dimension_id": dimension_id,
            "paradox_type": paradox_type.name,
            "resolution_applied": resolution.resolution_name,
            "notes": notes,
        }
        self._case_log.append(case)
        return case

    def case_count(self) -> int:
        """Return the number of paradox cases logged."""
        return len(self._case_log)

    def cases_for_traveller(self, traveller_id: str) -> list[dict]:
        """Return all paradox cases associated with a given traveller ID."""
        return [c for c in self._case_log if c["traveller_id"] == traveller_id]

    def print_all_resolutions(self) -> None:
        """Print a formatted list of every known paradox and its resolution."""
        for res in self.all_resolutions():
            print(res)
            print()
