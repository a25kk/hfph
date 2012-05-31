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
$Id: common.py 5400 2006-05-17 08:06:00Z clebeaupin $
"""

# Python imports
import os
import sys
from types import StringType

# Zope imports
from Testing import ZopeTestCase
from AccessControl import Unauthorized
from AccessControl import getSecurityManager

# CMF imports
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.interfaces.base import IBaseUnit

# Products imports
from Products.PloneGlossary.tests import PloneGlossaryTestCase

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
