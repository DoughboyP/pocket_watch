"""
Dimension Registry — the management layer for multidimensional travel.

The Registry tracks every known dimension, every active traveller, and
every transit record.  Access to a dimension requires a valid travel
request approved by the Keeper.  No dimension is reachable without a
registered pocket watch.

No personal identifiers, criminal information, or real-world locations
are stored in this registry.  Traveller IDs are opaque tokens only.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Dict, List, Optional


class DimensionStatus(Enum):
    """Operational status of a dimension."""

    STABLE = auto()
    UNSTABLE = auto()
    QUARANTINED = auto()
    COLLAPSED = auto()
    RESTRICTED = auto()


class AccessTier(Enum):
    """
    Required clearance tier to enter a dimension.

    OPEN        — any registered traveller may enter.
    VETTED      — traveller must have a clean paradox record.
    CONTROLLED  — Keeper approval required for each visit.
    CLASSIFIED  — Keeper personal escort only; no solo transit.
    """

    OPEN = 1
    VETTED = 2
    CONTROLLED = 3
    CLASSIFIED = 4


@dataclass
class Dimension:
    """Represents a single dimension in the multiverse."""

    dimension_id: str
    name: str
    description: str
    controlling_faction: Optional[str] = None  # faction pseudonym
    status: DimensionStatus = DimensionStatus.STABLE
    access_tier: AccessTier = AccessTier.OPEN
    fixed_point: bool = False  # True if a Predestination Fixed Point is present
    notes: str = ""

    def is_accessible(self) -> bool:
        """Return True if the dimension can currently receive travellers."""
        return self.status not in (
            DimensionStatus.COLLAPSED,
            DimensionStatus.QUARANTINED,
        )

    def __str__(self) -> str:
        status_flag = " [FIXED POINT]" if self.fixed_point else ""
        return (
            f"Dimension : {self.name} ({self.dimension_id}){status_flag}\n"
            f"  Status    : {self.status.name}\n"
            f"  Access    : {self.access_tier.name}\n"
            f"  Faction   : {self.controlling_faction or 'unclaimed'}\n"
            f"  Notes     : {self.notes or self.description}"
        )


@dataclass
class TravelRecord:
    """An immutable log entry for a single transit event."""

    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    traveller_id: str = ""
    origin_dimension_id: str = ""
    destination_dimension_id: str = ""
    departure_time: datetime = field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )
    arrival_time: Optional[datetime] = None
    approved_by_keeper: bool = False
    paradox_flagged: bool = False
    notes: str = ""

    def complete_transit(self, notes: str = "") -> None:
        """Mark the transit as completed."""
        self.arrival_time = datetime.now(tz=timezone.utc)
        if notes:
            self.notes = notes

    def __str__(self) -> str:
        arrival = (
            self.arrival_time.isoformat() if self.arrival_time else "in transit"
        )
        return (
            f"TravelRecord {self.record_id[:8]}\n"
            f"  Traveller   : {self.traveller_id}\n"
            f"  Route       : {self.origin_dimension_id} → "
            f"{self.destination_dimension_id}\n"
            f"  Departed    : {self.departure_time.isoformat()}\n"
            f"  Arrived     : {arrival}\n"
            f"  Approved    : {'yes' if self.approved_by_keeper else 'no'}\n"
            f"  Paradox     : {'YES — flagged' if self.paradox_flagged else 'none'}"
        )


class RegistryError(Exception):
    """Raised when a travel request violates registry rules."""


class DimensionRegistry:
    """
    Manages the catalogue of dimensions and the transit log.

    This is the administrative core of the pocket-watch system.
    The Keeper holds the master instance.
    """

    def __init__(self) -> None:
        self._dimensions: Dict[str, Dimension] = {}
        self._travel_log: List[TravelRecord] = []
        self._registered_travellers: Dict[str, dict] = {}

    # ------------------------------------------------------------------
    # Dimension management
    # ------------------------------------------------------------------

    def add_dimension(self, dimension: Dimension) -> None:
        """Register a dimension.  Raises if the ID is already in use."""
        if dimension.dimension_id in self._dimensions:
            raise RegistryError(
                f"Dimension ID '{dimension.dimension_id}' is already registered."
            )
        self._dimensions[dimension.dimension_id] = dimension

    def get_dimension(self, dimension_id: str) -> Dimension:
        """Retrieve a dimension by its ID."""
        try:
            return self._dimensions[dimension_id]
        except KeyError:
            raise RegistryError(
                f"Unknown dimension: '{dimension_id}'."
            ) from None

    def list_dimensions(
        self,
        status_filter: Optional[DimensionStatus] = None,
        faction_filter: Optional[str] = None,
    ) -> List[Dimension]:
        """Return dimensions, optionally filtered by status or faction."""
        results = list(self._dimensions.values())
        if status_filter is not None:
            results = [d for d in results if d.status == status_filter]
        if faction_filter is not None:
            needle = faction_filter.lower()
            results = [
                d
                for d in results
                if d.controlling_faction
                and d.controlling_faction.lower() == needle
            ]
        return results

    def update_status(
        self, dimension_id: str, new_status: DimensionStatus
    ) -> None:
        """Update the operational status of a dimension."""
        dim = self.get_dimension(dimension_id)
        dim.status = new_status

    # ------------------------------------------------------------------
    # Traveller management
    # ------------------------------------------------------------------

    def register_traveller(self, traveller_id: str, clearance: AccessTier) -> None:
        """
        Register a traveller with a given clearance tier.

        traveller_id must be an opaque token — no personal information.
        """
        if traveller_id in self._registered_travellers:
            raise RegistryError(
                f"Traveller '{traveller_id}' is already registered."
            )
        self._registered_travellers[traveller_id] = {
            "clearance": clearance,
            "active_transit": None,
            "total_transits": 0,
            "paradox_count": 0,
        }

    def get_traveller(self, traveller_id: str) -> dict:
        """Return registry data for a traveller."""
        try:
            return self._registered_travellers[traveller_id]
        except KeyError:
            raise RegistryError(
                f"Traveller '{traveller_id}' is not registered."
            ) from None

    # ------------------------------------------------------------------
    # Transit management
    # ------------------------------------------------------------------

    def request_transit(
        self,
        traveller_id: str,
        origin_id: str,
        destination_id: str,
        keeper_approved: bool = False,
    ) -> TravelRecord:
        """
        Validate and open a transit request.

        Raises
        ------
        RegistryError
            If the traveller lacks clearance, the dimension is inaccessible,
            or the request violates a registry rule.
        """
        traveller = self.get_traveller(traveller_id)
        destination = self.get_dimension(destination_id)
        origin = self.get_dimension(origin_id)

        if not origin.is_accessible():
            raise RegistryError(
                f"Origin dimension '{origin_id}' is not accessible "
                f"(status: {origin.status.name})."
            )

        if not destination.is_accessible():
            raise RegistryError(
                f"Destination dimension '{destination_id}' is not accessible "
                f"(status: {destination.status.name})."
            )

        required_tier = destination.access_tier
        traveller_tier = traveller["clearance"]

        if traveller_tier.value < required_tier.value:
            raise RegistryError(
                f"Traveller '{traveller_id}' has clearance tier "
                f"{traveller_tier.name} but dimension '{destination_id}' "
                f"requires {required_tier.name}."
            )

        if destination.access_tier in (AccessTier.CONTROLLED, AccessTier.CLASSIFIED):
            if not keeper_approved:
                raise RegistryError(
                    f"Dimension '{destination_id}' requires Keeper approval."
                )

        record = TravelRecord(
            traveller_id=traveller_id,
            origin_dimension_id=origin_id,
            destination_dimension_id=destination_id,
            approved_by_keeper=keeper_approved,
        )
        traveller["active_transit"] = record.record_id
        self._travel_log.append(record)
        return record

    def complete_transit(self, record_id: str, notes: str = "") -> TravelRecord:
        """Mark a transit as complete and update traveller stats."""
        record = self._find_record(record_id)
        record.complete_transit(notes)
        traveller = self._registered_travellers.get(record.traveller_id)
        if traveller:
            traveller["active_transit"] = None
            traveller["total_transits"] += 1
        return record

    def flag_paradox(self, record_id: str) -> TravelRecord:
        """Flag a transit record as involving a paradox event."""
        record = self._find_record(record_id)
        record.paradox_flagged = True
        traveller = self._registered_travellers.get(record.traveller_id)
        if traveller:
            traveller["paradox_count"] += 1
        return record

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def travel_history(self, traveller_id: str) -> List[TravelRecord]:
        """Return all travel records for a given traveller."""
        return [r for r in self._travel_log if r.traveller_id == traveller_id]

    def flagged_records(self) -> List[TravelRecord]:
        """Return all travel records that were flagged for a paradox."""
        return [r for r in self._travel_log if r.paradox_flagged]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _find_record(self, record_id: str) -> TravelRecord:
        for record in self._travel_log:
            if record.record_id == record_id:
                return record
        raise RegistryError(f"No travel record found with ID '{record_id}'.")
