
Introduction
------------

This is an editor for combining adjoining polygonal shapes into patterns.
Currently two shapes are included: squares and equilateral triangles, with
equal side length. The immediate intended application is planning base
foundations for the MMORPG Rust_, but the software's potential scope is
more general than this.

.. _Rust: https://playrust.com/

This software is operated almost entirely by keyboard. Some mouse actions
are supported. A summary of these functions is provided below.

This software is a work-in-progress. It is considered to be sufficiently
useful and glitch-free to be presented publicly. Some intended features are
not implemented, there are probably gaps in the documentation, and some
aspects are not as aesthetically pleasing as would be preferred. No glitches
or gotchas are present to my knowledge, but there may be some lurking out of
sight.

Regular updates are expected for the spring of 2016. At some point, interest
will wane, but I will attempt to keep this notice current.

Terminology
-----------

=============  ===============================================
 Term           Definition
=============  ===============================================
 Tile           Polygon shape (square or equilateral triangle)
 Edge           Tile's side, possibly shared between two tiles
 Scene          The collection of all tiles
 Active Tile    Tile cursor
 Active Edge    Edge cursor, always an edge of the active tile
=============  ===============================================


Interface
---------

+----------+-------------------------------------------+-------------------------+
| Key      |  Effect                                   | Shifted Effect          |
+==========+===========================================+=========================+
| q        |  Create a square tile                     | Active tile not changed |
+----------+-------------------------------------------+-------------------------+
| t        |  Create a triangular tile                 | Active tile not changed |
+----------+-------------------------------------------+-------------------------+
| Left     |  Rotate the active edge counter-clockwise |                         |
+----------+-------------------------------------------+-------------------------+
| Right    |  Rotate the active edge clockwise         |                         |
+----------+-------------------------------------------+-------------------------+
| | Keypad | | Set active tile to the tile across the  |                         |
| | Insert | | active edge                             |                         |
+----------+-------------------------------------------+-------------------------+
| Space    |  Select/deselect the active tile          |                         |
+----------+-------------------------------------------+-------------------------+
| Delete   |  Delete the tile across the active edge   | Delete selected tiles   |
+----------+-------------------------------------------+-------------------------+
| l        |  Load scene from a file                   |                         |
+----------+-------------------------------------------+-------------------------+
| s        |  Save scene to a file                     |                         |
+----------+-------------------------------------------+-------------------------+
| Escape   |  Exit program                             |                         |
+----------+-------------------------------------------+-------------------------+


+----------+------------------------------------------------+
| | Mouse  | Effect                                         |
| | Button |                                                |
+==========+================================================+
| Left     | Activate tile under the mouse pointer          |
+----------+------------------------------------------------+
| Right    | Select/deselect tile under the mouse pointer   |
+----------+------------------------------------------------+


--------

This software is licenced under the `Apache Public License, version 2.0`_

.. _`Apache Public License, version 2.0`: http://www.apache.org/licenses/LICENSE-2.0

The home page for this project is:
http://www.github.com/sfaleron/PolygonTiles
