# -*- coding: utf-8 -*-
from __future__ import division
# Copyright (C) 2012 Matthew Hampton
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

from amspApp.Infrustructures.MySpiffWorkflow.bpmn.specs.BpmnSpecMixin import BpmnSpecMixin
from amspApp.Infrustructures.MySpiffWorkflow.specs.Simple import Simple

class StartEvent(Simple, BpmnSpecMixin):
    """
    Task Spec for a bpmn:startEvent node.
    """
    def __init__(self, parent, name, **kwargs):
        super(StartEvent, self).__init__(parent, name, **kwargs)