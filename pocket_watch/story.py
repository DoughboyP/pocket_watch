"""
Origin story — the moment the pocket watch was found.

This module provides the narrative prologue that contextualises the
pocket-watch system.  No real persons, criminal organisations, or
sensitive information are identified.  All events are entirely fictional.
"""

_PROLOGUE = """\
╔══════════════════════════════════════════════════════════════════════╗
║              T H E   P O C K E T   W A T C H                       ║
╚══════════════════════════════════════════════════════════════════════╝

  The war was winding down in the forests to the east when he came
  across the body.

  The dead man wore the grey-green wool of a soldier who had fought for
  a regime already crumbling into the mud of history.  The soldier had
  fallen in a clearing, far from any road, far from any witnesses.  No
  orders.  No argument.  Just an ending, quiet and alone, among the
  pines.

  He knelt, not out of respect for the uniform — he had no respect for
  it — but out of the universal human impulse to acknowledge a finished
  life.  That was when he saw it.

  Half-buried beneath the man's open coat, glinting in a crack of grey
  morning light: a pocket watch.

  It was unlike anything he had seen before.  The casing was brass,
  worn to a dull gold, but the engravings on the lid were not decorative.
  They were technical.  Geometric.  Diagrams of something he could not
  name.  He opened it.

  The face showed no hours, no minutes.  Instead it held a compass-like
  arrangement of symbols and a spinning central disc that moved of its
  own accord.  A faint hum ran through the metal and into his palm —
  not heat, not electricity, but something older.  A resonance, as
  though the watch were in constant conversation with something just
  beyond the edge of the visible world.

  Written on the inside of the lid, in a language that shifted and
  re-formed as he stared at it until it finally resolved into words he
  could read:

      "PASSAGE GRANTED TO THE HOLDER.
       ENTRY REQUIRES REGISTRATION.
       ALL TRANSITS LOGGED.
       PARADOXES WILL BE RESOLVED.
       — THE KEEPER"

  He pocketed the watch.

  That night, the hum became a voice.  Not a sound — more like a
  certainty that pressed itself into the back of his mind:

      The watch had been placed.  On purpose.  For him.
      Because the multiverse had decided he was the kind of man
      who would use it wisely rather than simply use it.

  By morning he understood three things:

    1.  Dimensions beyond his own existed in vast, interlocking number.
    2.  Other people — other factions — already knew this, already moved
        between those dimensions, already held territory and power
        and history he had never been permitted to see.
    3.  He had just been handed the master key.

  The watch began to warm in his pocket, and on its spinning disc a
  single word appeared:

      REGISTER

  He pressed it.

  The Keeper answered.

══════════════════════════════════════════════════════════════════════
"""


def origin_story() -> str:
    """Return the pocket-watch origin narrative as a string."""
    return _PROLOGUE


def print_origin_story() -> None:
    """Print the pocket-watch origin narrative to stdout."""
    print(origin_story())
