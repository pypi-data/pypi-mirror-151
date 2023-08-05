"""
Created on Aug 13, 2021

@author: Siro

"""


class BoBlacklistElementsMaps(object):

    bo_blacklist_select_type_css = "select[name='includeItem.type'][id='_includeItem_type']"
    bo_blacklist_select_type_value_country = "country"
    bo_blacklist_select_country_css = "select[name='includeItem.value'][id='_includeItem_value']"
    bo_blacklist_add_button_xpath = "//*[@id='_0']"
    bo_blacklist_first_row_value_xpath = "//*[@id='blacklistIncluded']/tbody/tr[1]/td[1]"
    bo_blacklist_first_row_remove_button_xpath = "//*[@id='blacklistIncluded']/tbody/tr[1]/td[5]/a"
