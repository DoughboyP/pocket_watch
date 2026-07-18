"""
Tests for the Pocket Watch multidimensional management system.
"""

import pytest

from pocket_watch.factions import FACTIONS, Faction, get_faction
from pocket_watch.paradox_engine import ParadoxEngine, ParadoxType
from pocket_watch.dimensions import (
    AccessTier,
    Dimension,
    DimensionRegistry,
    DimensionStatus,
    RegistryError,
)
from pocket_watch.keeper import Keeper
from pocket_watch.story import origin_story

EXPECTED_FACTION_COUNT = 8


# ---------------------------------------------------------------------------
# Faction tests
# ---------------------------------------------------------------------------

class TestFactions:
    def test_eight_factions_defined(self):
        assert len(FACTIONS) == EXPECTED_FACTION_COUNT

    def test_all_factions_have_pseudonym(self):
        for faction in FACTIONS:
            assert isinstance(faction.pseudonym, str)
            assert len(faction.pseudonym) > 0

    def test_all_factions_have_allegiance(self):
        valid = {"order", "chaos", "neutral"}
        for faction in FACTIONS:
            assert faction.allegiance in valid, (
                f"{faction.pseudonym} has invalid allegiance: {faction.allegiance}"
            )

    def test_get_faction_by_pseudonym(self):
        faction = get_faction("The Clockmakers")
        assert faction.pseudonym == "The Clockmakers"

    def test_get_faction_case_insensitive(self):
        faction = get_faction("the void walkers")
        assert faction.pseudonym == "The Void Walkers"

    def test_get_faction_unknown_raises(self):
        with pytest.raises(KeyError):
            get_faction("Non-existent Faction")

    def test_faction_str_contains_pseudonym(self):
        faction = FACTIONS[0]
        assert faction.pseudonym in str(faction)

    def test_faction_known_dimensions_is_list(self):
        for faction in FACTIONS:
            assert isinstance(faction.known_dimensions, list)

    def test_no_real_world_criminal_references(self):
        """Faction content should not contain known real-world criminal org names."""
        sensitive_terms = [
            "mafia", "cartel", "triad", "yakuza", "cosa nostra",
            "camorra", "ms-13", "crips", "bloods",
        ]
        for faction in FACTIONS:
            text = (
                faction.pseudonym
                + faction.description
                + faction.domain
                + faction.motto
            ).lower()
            for term in sensitive_terms:
                assert term not in text, (
                    f"Faction '{faction.pseudonym}' contains restricted term: {term}"
                )


# ---------------------------------------------------------------------------
# Paradox Engine tests
# ---------------------------------------------------------------------------

class TestParadoxEngine:
    def test_all_paradox_types_have_resolutions(self):
        engine = ParadoxEngine()
        for ptype in ParadoxType:
            resolution = engine.get_resolution(ptype)
            assert resolution is not None

    def test_resolution_has_strategy(self):
        engine = ParadoxEngine()
        for ptype in ParadoxType:
            res = engine.get_resolution(ptype)
            assert len(res.resolution_strategy) > 20

    def test_log_case_increments_count(self):
        engine = ParadoxEngine()
        assert engine.case_count() == 0
        engine.log_case("T-001", "DIM-001", ParadoxType.GRANDFATHER)
        assert engine.case_count() == 1

    def test_log_case_returns_dict_with_resolution(self):
        engine = ParadoxEngine()
        case = engine.log_case("T-002", "DIM-002", ParadoxType.BOOTSTRAP)
        assert "resolution_applied" in case
        assert "paradox_type" in case
        assert case["paradox_type"] == "BOOTSTRAP"

    def test_cases_for_traveller_filters_correctly(self):
        engine = ParadoxEngine()
        engine.log_case("T-AAA", "DIM-001", ParadoxType.GRANDFATHER)
        engine.log_case("T-BBB", "DIM-001", ParadoxType.BUTTERFLY)
        engine.log_case("T-AAA", "DIM-002", ParadoxType.TEMPORAL_TWIN)
        cases = engine.cases_for_traveller("T-AAA")
        assert len(cases) == 2
        assert all(c["traveller_id"] == "T-AAA" for c in cases)

    def test_all_resolutions_returns_list_of_correct_length(self):
        engine = ParadoxEngine()
        resolutions = engine.all_resolutions()
        assert len(resolutions) == len(list(ParadoxType))

    def test_seven_paradox_types_exist(self):
        assert len(list(ParadoxType)) == 7


# ---------------------------------------------------------------------------
# Dimension Registry tests
# ---------------------------------------------------------------------------

class TestDimensionRegistry:
    def _make_dim(self, dim_id: str, access: AccessTier = AccessTier.OPEN) -> Dimension:
        return Dimension(
            dimension_id=dim_id,
            name=f"Test Dimension {dim_id}",
            description="A test dimension.",
            access_tier=access,
        )

    def test_add_and_retrieve_dimension(self):
        reg = DimensionRegistry()
        dim = self._make_dim("D-001")
        reg.add_dimension(dim)
        assert reg.get_dimension("D-001").name == "Test Dimension D-001"

    def test_duplicate_dimension_raises(self):
        reg = DimensionRegistry()
        dim = self._make_dim("D-001")
        reg.add_dimension(dim)
        with pytest.raises(RegistryError):
            reg.add_dimension(self._make_dim("D-001"))

    def test_get_unknown_dimension_raises(self):
        reg = DimensionRegistry()
        with pytest.raises(RegistryError):
            reg.get_dimension("D-UNKNOWN")

    def test_register_and_get_traveller(self):
        reg = DimensionRegistry()
        reg.register_traveller("TRV-01", AccessTier.OPEN)
        traveller = reg.get_traveller("TRV-01")
        assert traveller["clearance"] == AccessTier.OPEN

    def test_duplicate_traveller_raises(self):
        reg = DimensionRegistry()
        reg.register_traveller("TRV-01", AccessTier.OPEN)
        with pytest.raises(RegistryError):
            reg.register_traveller("TRV-01", AccessTier.OPEN)

    def test_successful_transit(self):
        reg = DimensionRegistry()
        reg.add_dimension(self._make_dim("ORIGIN"))
        reg.add_dimension(self._make_dim("DEST"))
        reg.register_traveller("TRV-01", AccessTier.OPEN)
        record = reg.request_transit("TRV-01", "ORIGIN", "DEST")
        assert record.traveller_id == "TRV-01"
        assert record.destination_dimension_id == "DEST"

    def test_transit_to_inaccessible_dimension_raises(self):
        reg = DimensionRegistry()
        origin = self._make_dim("ORIGIN")
        dest = Dimension(
            dimension_id="DEST-COL",
            name="Collapsed World",
            description="Gone.",
            status=DimensionStatus.COLLAPSED,
        )
        reg.add_dimension(origin)
        reg.add_dimension(dest)
        reg.register_traveller("TRV-01", AccessTier.OPEN)
        with pytest.raises(RegistryError):
            reg.request_transit("TRV-01", "ORIGIN", "DEST-COL")

    def test_transit_requires_clearance(self):
        reg = DimensionRegistry()
        reg.add_dimension(self._make_dim("ORIGIN"))
        reg.add_dimension(
            self._make_dim("CLASSIFIED-DEST", AccessTier.CLASSIFIED)
        )
        reg.register_traveller("TRV-LOW", AccessTier.OPEN)
        with pytest.raises(RegistryError):
            reg.request_transit("TRV-LOW", "ORIGIN", "CLASSIFIED-DEST")

    def test_transit_controlled_requires_keeper_approval(self):
        reg = DimensionRegistry()
        reg.add_dimension(self._make_dim("ORIGIN"))
        reg.add_dimension(
            self._make_dim("CONTROLLED-DEST", AccessTier.CONTROLLED)
        )
        reg.register_traveller("TRV-HIGH", AccessTier.CLASSIFIED)
        # Should fail without approval flag
        with pytest.raises(RegistryError):
            reg.request_transit(
                "TRV-HIGH", "ORIGIN", "CONTROLLED-DEST", keeper_approved=False
            )
        # Should succeed with approval flag
        record = reg.request_transit(
            "TRV-HIGH", "ORIGIN", "CONTROLLED-DEST", keeper_approved=True
        )
        assert record is not None

    def test_complete_transit_updates_traveller_stats(self):
        reg = DimensionRegistry()
        reg.add_dimension(self._make_dim("O"))
        reg.add_dimension(self._make_dim("D"))
        reg.register_traveller("TRV-X", AccessTier.OPEN)
        record = reg.request_transit("TRV-X", "O", "D")
        reg.complete_transit(record.record_id)
        assert reg.get_traveller("TRV-X")["total_transits"] == 1

    def test_flag_paradox_increments_traveller_paradox_count(self):
        reg = DimensionRegistry()
        reg.add_dimension(self._make_dim("O"))
        reg.add_dimension(self._make_dim("D"))
        reg.register_traveller("TRV-P", AccessTier.OPEN)
        record = reg.request_transit("TRV-P", "O", "D")
        reg.flag_paradox(record.record_id)
        assert reg.get_traveller("TRV-P")["paradox_count"] == 1
        assert len(reg.flagged_records()) == 1

    def test_travel_history_filters_by_traveller(self):
        reg = DimensionRegistry()
        reg.add_dimension(self._make_dim("O"))
        reg.add_dimension(self._make_dim("D"))
        reg.register_traveller("TRV-A", AccessTier.OPEN)
        reg.register_traveller("TRV-B", AccessTier.OPEN)
        reg.request_transit("TRV-A", "O", "D")
        reg.request_transit("TRV-B", "O", "D")
        reg.request_transit("TRV-A", "D", "O")
        assert len(reg.travel_history("TRV-A")) == 2
        assert len(reg.travel_history("TRV-B")) == 1

    def test_list_dimensions_with_status_filter(self):
        reg = DimensionRegistry()
        stable = self._make_dim("S-01")
        collapsed = Dimension(
            dimension_id="C-01",
            name="Gone",
            description="Collapsed.",
            status=DimensionStatus.COLLAPSED,
        )
        reg.add_dimension(stable)
        reg.add_dimension(collapsed)
        stables = reg.list_dimensions(status_filter=DimensionStatus.STABLE)
        assert len(stables) == 1
        assert stables[0].dimension_id == "S-01"


# ---------------------------------------------------------------------------
# Keeper tests
# ---------------------------------------------------------------------------

class TestKeeper:
    def test_keeper_initialises_with_default_dimensions(self):
        keeper = Keeper()
        dims = keeper.list_all_dimensions()
        assert len(dims) > 0

    def test_keeper_has_eight_factions(self):
        keeper = Keeper()
        assert len(keeper.factions) == EXPECTED_FACTION_COUNT

    def test_keeper_register_and_transit(self):
        keeper = Keeper()
        keeper.register_traveller("T-HERO", AccessTier.OPEN)
        record = keeper.transit("T-HERO", "DIM-000", "DIM-002")
        assert record.traveller_id == "T-HERO"

    def test_keeper_approve_controlled_transit(self):
        keeper = Keeper()
        keeper.register_traveller("T-ELITE", AccessTier.CLASSIFIED)
        keeper.approve_transit("T-ELITE", "DIM-006")
        record = keeper.transit(
            "T-ELITE", "DIM-000", "DIM-006", keeper_approved=True
        )
        assert record is not None

    def test_keeper_report_paradox(self):
        keeper = Keeper()
        keeper.register_traveller("T-PAR", AccessTier.OPEN)
        record = keeper.transit("T-PAR", "DIM-000", "DIM-002")
        case = keeper.report_paradox(
            traveller_id="T-PAR",
            dimension_id="DIM-002",
            paradox_type=ParadoxType.GRANDFATHER,
            record_id=record.record_id,
        )
        assert case["paradox_type"] == "GRANDFATHER"
        assert keeper.paradox_engine.case_count() == 1
        assert len(keeper.registry.flagged_records()) == 1

    def test_keeper_status_report_is_string(self):
        keeper = Keeper()
        report = keeper.status_report()
        assert isinstance(report, str)
        assert "KEEPER" in report

    def test_open_dimensions_accessible(self):
        keeper = Keeper()
        open_dims = keeper.list_open_dimensions()
        for dim in open_dims:
            assert dim.is_accessible()
            assert dim.access_tier == AccessTier.OPEN

    def test_elevate_clearance(self):
        keeper = Keeper()
        keeper.register_traveller("T-LOW", AccessTier.OPEN)
        keeper.elevate_clearance("T-LOW", AccessTier.CLASSIFIED)
        traveller = keeper.registry.get_traveller("T-LOW")
        assert traveller["clearance"] == AccessTier.CLASSIFIED


# ---------------------------------------------------------------------------
# Story tests
# ---------------------------------------------------------------------------

class TestStory:
    def test_origin_story_returns_string(self):
        text = origin_story()
        assert isinstance(text, str)

    def test_origin_story_mentions_pocket_watch(self):
        text = origin_story().lower()
        assert "pocket watch" in text

    def test_origin_story_mentions_keeper(self):
        text = origin_story()
        assert "KEEPER" in text

    def test_origin_story_mentions_register(self):
        text = origin_story()
        assert "REGISTER" in text
