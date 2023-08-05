"""
Created on July 26, 2021

@author: Siro

"""


class BoHeaderElementsMaps(object):

    bo_site_not_select_text_css = "button[class='btn dropdown-toggle btn-default'][title='Select site']"
    bo_site_select_button_css = "button[class='btn dropdown-toggle btn-default'][data-toggle='dropdown']"
    bo_site_select_luckycasino_xpath = "//*[@id='bo-page-player-list']/div[1]/header/div/div/div[2]/div[4]/div/div/ul/li[4]"
    bo_site_select_css = "select[class='bo-site-selector__input bo-select bs-select-hidden']"
    bo_site_select_on_helpdesk_xpath = "//*[@id='bo-page-player-list']/div[1]/header/div/div/div[2]/div[4]/select"
    bo_site_select_on_report_statistic_xpath = "//*[@id='bo-page-reports-statistics']/div[1]/header/div/div/div[2]/div[4]/div/button"
    bo_site_select_on_report_business_overview_xpath = "//*[@id='bo-page-reports-overview']/div[1]/header/div/div/div[2]/div[4]/div/button"

    bo_helpdesk_link_css = "a[class='bo-nav__control'][href='playerSearch!view']"
    bo_search_text_field_css = "input[id='playerSearch_freeText'][class='bo-field__control form-control bo-field__control--textfield']"
    bo_search_text_field_xpath = "//*[@id='playerSearch_freeText']"
    bo_home_link_css = "a[class='bo-nav__control'][href='/bo/playerSearch!view']"