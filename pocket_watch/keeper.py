"""
The Keeper — sovereign of the dimensional repository.

The Keeper is the single authority who owns the multiverse registry.
No traveller enters a controlled or classified dimension without the
Keeper's explicit approval.  The Keeper also seeds the registry with
the known dimensions and manages faction relationships.

The Keeper holds no personal information on travellers — only opaque
transit tokens.  No criminal records, real identities, or location
data are stored here.
"""

from __future__ import annotations

from .dimensions import (
    AccessTier,
    Dimension,
    DimensionRegistry,
    DimensionStatus,
    RegistryError,
    TravelRecord,
)
from .factions import FACTIONS, Faction
from .paradox_engine import ParadoxEngine, ParadoxType


# ---------------------------------------------------------------------------
# Default dimensions seeded by the Keeper
# ---------------------------------------------------------------------------

_DEFAULT_DIMENSIONS: list[Dimension] = [
    Dimension(
        dimension_id="DIM-001",
        name="The Wound",
        description=(
            "A dimension frozen at the moment of a great catastrophe.  "
            "Controlled by The Clockmakers as a testing ground for new relics."
        ),
        controlling_faction="The Clockmakers",
        status=DimensionStatus.STABLE,
        access_tier=AccessTier.VETTED,
        fixed_point=True,
        notes="Entry near the catastrophe event is strictly forbidden.",
    ),
    Dimension(
        dimension_id="DIM-002",
        name="The Still Hour",
        description=(
            "Time moves at one tenth of normal speed.  Favoured by scholars "
            "who need centuries of uninterrupted study.  Clockmaker territory."
        ),
        controlling_faction="The Clockmakers",
        status=DimensionStatus.STABLE,
        access_tier=AccessTier.OPEN,
    ),
    Dimension(
        dimension_id="DIM-003",
        name="The Seam",
        description=(
            "The primary transit corridor used by the Void Walkers.  "
            "Technically unclaimed, practically their home."
        ),
        controlling_faction="The Void Walkers",
        status=DimensionStatus.STABLE,
        access_tier=AccessTier.OPEN,
    ),
    Dimension(
        dimension_id="DIM-004",
        name="The Fold",
        description=(
            "A compressed dimension where distances between realities "
            "are minimal — travellers use it as a shortcut hub."
        ),
        controlling_faction="The Void Walkers",
        status=DimensionStatus.STABLE,
        access_tier=AccessTier.VETTED,
    ),
    Dimension(
        dimension_id="DIM-005",
        name="Foundation Zero",
        description=(
            "The Architects' headquarters: a dimension that pre-dates all "
            "others and contains the original lattice blueprints."
        ),
        controlling_faction="The Architects",
        status=DimensionStatus.RESTRICTED,
        access_tier=AccessTier.CLASSIFIED,
        fixed_point=True,
        notes="The Architects permit no unsupervised access.",
    ),
    Dimension(
        dimension_id="DIM-006",
        name="The Fixed Point",
        description=(
            "An Anchor-managed dimension built around a cluster of "
            "Predestination Fixed Points.  Used as a calibration standard "
            "for all pocket-watch relics."
        ),
        controlling_faction="The Anchors",
        status=DimensionStatus.STABLE,
        access_tier=AccessTier.CONTROLLED,
        fixed_point=True,
    ),
    Dimension(
        dimension_id="DIM-007",
        name="The Grey Archive",
        description=(
            "The Echoes' storage dimension.  Filled with preserved memories "
            "and artefacts from hundreds of collapsed realities."
        ),
        controlling_faction="The Echoes",
        status=DimensionStatus.STABLE,
        access_tier=AccessTier.VETTED,
        notes="Removing any archived item triggers an automatic Paradox Engine alert.",
    ),
    Dimension(
        dimension_id="DIM-008",
        name="The Dominion",
        description=(
            "The administrative capital of the Sovereign Fold.  Heavily "
            "patrolled; entry without tribute is met with expulsion."
        ),
        controlling_faction="The Sovereign Fold",
        status=DimensionStatus.STABLE,
        access_tier=AccessTier.CONTROLLED,
    ),
    Dimension(
        dimension_id="DIM-009",
        name="Node Prime",
        description=(
            "The Pale Circuit's central node.  All Circuit communications "
            "route through here."
        ),
        controlling_faction="The Pale Circuit",
        status=DimensionStatus.STABLE,
        access_tier=AccessTier.VETTED,
    ),
    Dimension(
        dimension_id="DIM-010",
        name="The Between",
        description=(
            "The Driftborn's adopted home — a dimension with no native "
            "timeline of its own, where displaced travellers find refuge."
        ),
        controlling_faction="The Driftborn",
        status=DimensionStatus.STABLE,
        access_tier=AccessTier.OPEN,
        notes="Neutral ground.  No faction enforcement is permitted here.",
    ),
    Dimension(
        dimension_id="DIM-011",
        name="Residue",
        description=(
            "A former Sovereign Fold territory that collapsed after a "
            "Butterfly cascade.  Now managed by the Echoes for archival study."
        ),
        controlling_faction="The Echoes",
        status=DimensionStatus.QUARANTINED,
        access_tier=AccessTier.CLASSIFIED,
    ),
    Dimension(
        dimension_id="DIM-000",
        name="The Origin",
        description=(
            "The dimension from which the pocket watch was first recovered.  "
            "Classified by the Keeper as the anchor of the entire registry."
        ),
        controlling_faction=None,
        status=DimensionStatus.STABLE,
        access_tier=AccessTier.OPEN,
        fixed_point=True,
        notes="Default home dimension for unregistered travellers.",
    ),
]


class Keeper:
    """
    The Keeper — sovereign of the multidimensional repository.

    The Keeper initialises and owns the registry, approves restricted
    transit requests, handles paradox escalations, and maintains
    relationships with all eight factions.

    The Keeper stores no personal information on travellers.
    """

    KEEPER_ID = "KEEPER-PRIME"

    def __init__(self) -> None:
        self.registry = DimensionRegistry()
        self.paradox_engine = ParadoxEngine()
        self.factions: list[Faction] = list(FACTIONS)
        self._pending_approvals: list[dict] = []

        # Seed the registry with default dimensions
        for dim in _DEFAULT_DIMENSIONS:
            self.registry.add_dimension(dim)

    # ------------------------------------------------------------------
    # Dimension management
    # ------------------------------------------------------------------

    def add_dimension(self, dimension: Dimension) -> None:
        """Add a new dimension to the registry."""
        self.registry.add_dimension(dimension)

    def list_all_dimensions(self) -> list[Dimension]:
        """Return every dimension in the registry."""
        return self.registry.list_dimensions()

    def list_open_dimensions(self) -> list[Dimension]:
        """Return dimensions that any registered traveller may enter."""
        return [
            d
            for d in self.registry.list_dimensions()
            if d.access_tier == AccessTier.OPEN and d.is_accessible()
        ]

    # ------------------------------------------------------------------
    # Traveller management
    # ------------------------------------------------------------------

    def register_traveller(
        self, traveller_id: str, clearance: AccessTier = AccessTier.OPEN
    ) -> None:
        """Register a new traveller with the given clearance tier."""
        self.registry.register_traveller(traveller_id, clearance)

    def elevate_clearance(
        self, traveller_id: str, new_clearance: AccessTier
    ) -> None:
        """Raise a traveller's clearance tier."""
        traveller = self.registry.get_traveller(traveller_id)
        traveller["clearance"] = new_clearance

    # ------------------------------------------------------------------
    # Transit approval
    # ------------------------------------------------------------------

    def approve_transit(
        self,
        traveller_id: str,
        destination_id: str,
    ) -> str:
        """
        Keeper personally approves a transit to a controlled/classified
        dimension.  Returns the approval token (used in request_transit).
        """
        destination = self.registry.get_dimension(destination_id)
        if not destination.is_accessible():
            raise RegistryError(
                f"Cannot approve transit to '{destination_id}': "
                f"dimension is {destination.status.name}."
            )
        token = f"APPROVED:{traveller_id}:{destination_id}"
        self._pending_approvals.append(
            {
                "token": token,
                "traveller_id": traveller_id,
                "destination_id": destination_id,
            }
        )
        return token

    def transit(
        self,
        traveller_id: str,
        origin_id: str,
        destination_id: str,
        keeper_approved: bool = False,
    ) -> TravelRecord:
        """
        Open a transit request through the registry.

        For CONTROLLED or CLASSIFIED dimensions, caller must first obtain
        approval via ``approve_transit`` and pass ``keeper_approved=True``.
        """
        return self.registry.request_transit(
            traveller_id=traveller_id,
            origin_id=origin_id,
            destination_id=destination_id,
            keeper_approved=keeper_approved,
        )

    def complete_transit(self, record_id: str, notes: str = "") -> TravelRecord:
        """Mark a transit as complete."""
        return self.registry.complete_transit(record_id, notes)

    # ------------------------------------------------------------------
    # Paradox handling
    # ------------------------------------------------------------------

    def report_paradox(
        self,
        traveller_id: str,
        dimension_id: str,
        paradox_type: ParadoxType,
        record_id: str | None = None,
        notes: str = "",
    ) -> dict:
        """
        Log a paradox event and apply the appropriate resolution.

        If a travel record ID is supplied the record is also flagged.
        """
        case = self.paradox_engine.log_case(
            traveller_id=traveller_id,
            dimension_id=dimension_id,
            paradox_type=paradox_type,
            notes=notes,
        )
        if record_id:
            self.registry.flag_paradox(record_id)
        return case

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def status_report(self) -> str:
        """Return a human-readable summary of the registry's current state."""
        dims = self.list_all_dimensions()
        stable = sum(1 for d in dims if d.status == DimensionStatus.STABLE)
        restricted = sum(1 for d in dims if d.status == DimensionStatus.RESTRICTED)
        quarantined = sum(
            1 for d in dims if d.status == DimensionStatus.QUARANTINED
        )
        collapsed = sum(1 for d in dims if d.status == DimensionStatus.COLLAPSED)
        total_records = len(self.registry._travel_log)
        flagged = len(self.registry.flagged_records())
        paradox_cases = self.paradox_engine.case_count()

        lines = [
            "=" * 60,
            "  KEEPER'S REPOSITORY — STATUS REPORT",
            "=" * 60,
            f"  Total dimensions : {len(dims)}",
            f"    Stable         : {stable}",
            f"    Restricted     : {restricted}",
            f"    Quarantined    : {quarantined}",
            f"    Collapsed      : {collapsed}",
            f"  Known factions   : {len(self.factions)}",
            f"  Transit records  : {total_records}",
            f"    Paradox flags  : {flagged}",
            f"  Paradox cases    : {paradox_cases}",
            "=" * 60,
        ]
        return "\n".join(lines)

    def print_factions(self) -> None:
        """Print all faction dossiers."""
        for faction in self.factions:
            print(faction)
            print()

    def print_dimensions(self) -> None:
        """Print all registered dimensions."""
        for dim in self.list_all_dimensions():
            print(dim)
            print()
