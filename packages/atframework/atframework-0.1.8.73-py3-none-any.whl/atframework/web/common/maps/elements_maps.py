"""
Created on Mar 04, 2021

@author: Siro

"""
from atframework.web.common.maps.bo.bo_header_elements_maps import BoHeaderElementsMaps
from atframework.web.common.maps.bo.bo_login_elements_maps import BoLoginElementsMaps
from atframework.web.common.maps.bo.bo_rebate_elements_maps import BoRebateElementsMaps
from atframework.web.common.maps.bo.bo_voucher_elements_maps import BoVoucherElementsMaps
from atframework.web.common.maps.bo.bo_helpdesk_elements_maps import BoHelpdeskElementsMaps
from atframework.web.common.maps.bo.bo_dashboard_elements_maps import BoDashboardElementsMaps
from atframework.web.common.maps.bo.bo_report_elements_maps import BoReportElementsMaps
from atframework.web.common.maps.bo.bo_menu_elements_maps import BoMenuElementsMaps
from atframework.web.common.maps.bo.bo_blacklist_elements_maps import BoBlacklistElementsMaps
from atframework.web.common.maps.bo.bo_alarms_elements_maps import BoAlarmsElementsMaps
from atframework.web.common.maps.bo.bo_billfold_configuration_elements_maps import BoBillfoldConfigurationElementsMaps
from atframework.web.common.maps.bo.bo_payment_elements_maps import BoPaymentElementsMaps
from atframework.web.common.maps.bo.bo_game_transaction_elements_maps import BoGameTransactionElementsMaps
from atframework.web.common.maps.bo.bo_campaign_elements_maps import BoCampaignElementsMaps


class ElementsMaps(BoHeaderElementsMaps, BoLoginElementsMaps, BoRebateElementsMaps, BoVoucherElementsMaps,
                   BoHelpdeskElementsMaps, BoDashboardElementsMaps, BoReportElementsMaps, BoMenuElementsMaps,
                   BoBlacklistElementsMaps, BoAlarmsElementsMaps, BoBillfoldConfigurationElementsMaps, BoPaymentElementsMaps,
                   BoGameTransactionElementsMaps, BoCampaignElementsMaps):
    """
    Integrate all model to this class, Use this class to call elements
    """
