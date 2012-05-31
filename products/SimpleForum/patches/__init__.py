## -*- coding: utf-8 -*-
## Copyright (C)2006 Ingeniweb

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
Import patches
"""
__version__ = "$Revision: 1.4 $"
# $Source: /cvsroot/ingeniweb/SimpleForum/patches/__init__.py,v $
# $Id: __init__.py,v 1.4 2006/05/17 08:04:44 clebeaupin Exp $
__docformat__ = 'restructuredtext'


# Backport _getTempFolder from Plone 2.1 for Plone 2.0
import FactoryToolPatch
