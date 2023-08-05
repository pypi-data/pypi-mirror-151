"""
Created on Mar 03, 2021

@author: Siro

"""
from atframework.web.common.model.at_closing import AtClosing
from atframework.web.common.model.at_opening import AtOpening
from atframework.web.common.model.at_waiting import AtWaiting
from atframework.web.common.model.at_show import AtShow
from atframework.web.common.model.at_click import AtClick
from atframework.web.common.model.at_type import AtType
from atframework.web.common.model.at_select import AtSelect
from atframework.web.common.model.at_get import AtGet
from atframework.web.common.model.at_expand import AtExpand
from atframework.web.common.model.at_scroll import AtScroll
from atframework.web.common.model.at_clear import AtClear



class ModelHelper(AtClosing, AtOpening, AtWaiting, AtClear,
                  AtType, AtShow, AtClick, AtSelect,
                  AtGet, AtExpand, AtScroll):
    """
    Integrate all model to this class, Use this class to drive test steps
    """
