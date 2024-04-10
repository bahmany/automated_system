# -*- coding: utf-8 -*-
from __future__ import division
from amspApp.Infrustructures.MySpiffWorkflow.version import __version__
from amspApp.Infrustructures.MySpiffWorkflow.Workflow import Workflow
from amspApp.Infrustructures.MySpiffWorkflow.Task import Task
from amspApp.Infrustructures.MySpiffWorkflow.exceptions import WorkflowException

import inspect
__all__ = [name for name, obj in list(locals().items())
           if not (name.startswith('_') or inspect.ismodule(obj))]
