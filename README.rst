
===============
Getting Started
===============

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


Terminology
-----------

=============  ===============================================
 Term           Definition
=============  ===============================================
 Tile           Polygon shape (square or equilateral triangle)
 Edge           Tile's side, possibly shared between two tiles
 Scene          The collection of all tiles
 Active Tile    Tile cursor
 Active Edge    Edge cursor
 Selection      A highlighted subgroup of tiles
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
| Ctrl     |  Select/deselect the active tile          |                         |
+----------+-------------------------------------------+-------------------------+
| Delete   |  Delete the tile across the active edge   | Delete selection        |
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


==========================
Developers and Power Users
==========================

Required to run the source code directly:

- `Python 2.7`_
- `Python MegaWidgets`_

.. _`Python 2.7`: http://www.python.org/
.. _`Python MegaWidgets`: http://pmw.sourceforge.net/

The recommended way to get Pmw is with with the pip_ python package installer:

  pip install pmw

.. _pip: https://pip.pypa.io/

To build a windows executable, py2exe_ is used, also obtained via pip:

  pip install py2exe

.. _py2exe: http://www.py2exe.org/


--------

The home page for this project is:
http://www.github.com/sfaleron/PolygonTiles
