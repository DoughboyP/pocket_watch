#!/usr/bin/env python3
"""
main.py — Pocket Watch interactive console.

Usage:
    python main.py

The console lets you explore the dimensional registry, read faction
dossiers, review paradox resolutions, simulate transit requests, and
trigger paradox events — all from the command line.

No personal, criminal, or real-world sensitive information is ever
requested or stored.
"""

from __future__ import annotations

import sys
from pocket_watch.dimensions import AccessTier, Dimension, DimensionStatus
from pocket_watch.keeper import Keeper
from pocket_watch.paradox_engine import ParadoxType
from pocket_watch.story import print_origin_story


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _divider() -> None:
    print("─" * 60)


def _banner() -> None:
    print(
        "\n"
        "╔══════════════════════════════════════════════════════════════╗\n"
        "║         P O C K E T   W A T C H   C O N S O L E            ║\n"
        "║              Multidimensional Management System             ║\n"
        "╚══════════════════════════════════════════════════════════════╝\n"
    )


def _prompt(options: list[tuple[str, str]]) -> str:
    """Display a numbered menu and return the user's choice key."""
    for key, label in options:
        print(f"  [{key}] {label}")
    print()
    return input("  Select: ").strip().lower()


# ---------------------------------------------------------------------------
# Sub-menus
# ---------------------------------------------------------------------------

def menu_story() -> None:
    print_origin_story()
    input("  Press Enter to continue...")


def menu_factions(keeper: Keeper) -> None:
    _divider()
    print("  THE EIGHT KNOWN FACTIONS\n")
    keeper.print_factions()
    input("  Press Enter to continue...")


def menu_dimensions(keeper: Keeper) -> None:
    _divider()
    print("  REGISTERED DIMENSIONS\n")
    keeper.print_dimensions()
    input("  Press Enter to continue...")


def menu_paradoxes(keeper: Keeper) -> None:
    _divider()
    print("  KNOWN PARADOX TYPES AND RESOLUTIONS\n")
    keeper.paradox_engine.print_all_resolutions()
    input("  Press Enter to continue...")


def menu_register_traveller(keeper: Keeper) -> None:
    _divider()
    print("  REGISTER A TRAVELLER\n")
    print("  Enter an opaque traveller token (no personal information).")
    token = input("  Token: ").strip()
    if not token:
        print("  [!] Token cannot be empty.")
        return
    try:
        keeper.register_traveller(token, AccessTier.OPEN)
        print(f"  [✓] Traveller '{token}' registered with OPEN clearance.")
    except Exception as exc:
        print(f"  [!] {exc}")
    input("  Press Enter to continue...")


def menu_transit(keeper: Keeper) -> None:
    _divider()
    print("  REQUEST TRANSIT\n")
    traveller_id = input("  Traveller token : ").strip()
    origin_id = input("  Origin dim ID   : ").strip()
    dest_id = input("  Destination ID  : ").strip()

    # Check if approval is needed
    try:
        dest = keeper.registry.get_dimension(dest_id)
    except Exception as exc:
        print(f"  [!] {exc}")
        input("  Press Enter to continue...")
        return

    keeper_approved = False
    if dest.access_tier.value >= AccessTier.CONTROLLED.value:
        print(
            f"\n  Dimension '{dest.name}' requires Keeper approval "
            f"(tier: {dest.access_tier.name})."
        )
        ans = input("  Request Keeper approval now? [y/n]: ").strip().lower()
        if ans == "y":
            try:
                keeper.approve_transit(traveller_id, dest_id)
                keeper_approved = True
                print("  [✓] Keeper approval granted.")
            except Exception as exc:
                print(f"  [!] Approval failed: {exc}")
                input("  Press Enter to continue...")
                return

    try:
        record = keeper.transit(
            traveller_id=traveller_id,
            origin_id=origin_id,
            destination_id=dest_id,
            keeper_approved=keeper_approved,
        )
        print(f"\n  [✓] Transit opened.\n\n{record}")
        complete = input("\n  Complete transit now? [y/n]: ").strip().lower()
        if complete == "y":
            keeper.complete_transit(record.record_id)
            print("  [✓] Transit completed.")
    except Exception as exc:
        print(f"  [!] Transit failed: {exc}")

    input("  Press Enter to continue...")


def menu_report_paradox(keeper: Keeper) -> None:
    _divider()
    print("  REPORT A PARADOX EVENT\n")
    traveller_id = input("  Traveller token : ").strip()
    dimension_id = input("  Dimension ID    : ").strip()
    print()
    for i, ptype in enumerate(ParadoxType, start=1):
        print(f"    [{i}] {ptype.name}")
    choice = input("\n  Select paradox type: ").strip()
    types = list(ParadoxType)
    try:
        paradox_type = types[int(choice) - 1]
    except (ValueError, IndexError):
        print("  [!] Invalid selection.")
        input("  Press Enter to continue...")
        return

    notes = input("  Notes (optional): ").strip()
    case = keeper.report_paradox(
        traveller_id=traveller_id,
        dimension_id=dimension_id,
        paradox_type=paradox_type,
        notes=notes,
    )
    resolution = keeper.paradox_engine.get_resolution(paradox_type)
    print(f"\n  [✓] Paradox logged.\n")
    print(f"  Type       : {case['paradox_type']}")
    print(f"  Resolution : {case['resolution_applied']}")
    print(f"  Strategy   : {resolution.resolution_strategy[:120]}...")
    input("\n  Press Enter to continue...")


def menu_status(keeper: Keeper) -> None:
    print()
    print(keeper.status_report())
    print()
    input("  Press Enter to continue...")


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def main() -> None:
    _banner()
    keeper = Keeper()

    options = [
        ("s", "Origin story — how the watch was found"),
        ("f", "Faction dossiers — the eight known factions"),
        ("d", "Dimension catalogue — all registered worlds"),
        ("p", "Paradox codex — types and resolutions"),
        ("r", "Register a traveller"),
        ("t", "Request transit between dimensions"),
        ("x", "Report a paradox event"),
        ("k", "Keeper status report"),
        ("q", "Quit"),
    ]

    while True:
        _banner()
        choice = _prompt(options)

        if choice == "s":
            menu_story()
        elif choice == "f":
            menu_factions(keeper)
        elif choice == "d":
            menu_dimensions(keeper)
        elif choice == "p":
            menu_paradoxes(keeper)
        elif choice == "r":
            menu_register_traveller(keeper)
        elif choice == "t":
            menu_transit(keeper)
        elif choice == "x":
            menu_report_paradox(keeper)
        elif choice == "k":
            menu_status(keeper)
        elif choice == "q":
            print("\n  The watch ticks on.  Until next time.\n")
            sys.exit(0)
        else:
            print("  [!] Unknown option.  Please select from the menu.\n")


if __name__ == "__main__":
    main()
