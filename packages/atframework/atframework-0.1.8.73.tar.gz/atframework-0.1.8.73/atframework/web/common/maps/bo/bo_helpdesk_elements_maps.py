"""
Created on July 26, 2021

@author: Siro

"""


class BoHelpdeskElementsMaps(object):
    """
    PLAYER SEARCH
    """
    bo_helpdesk_link_css = "a[class='bo-nav__control'][href='playerSearch!view']"
    bo_search_text_field_css = "input[id='playerSearch_freeText'][class='bo-field__control form-control bo-field__control--textfield']"
    bo_search_text_field_xpath = "//*[@id='playerSearch_freeText']"
    bo_search_button_css = "button[id='playerSearch_0'][class='bo-button bo-button--primary bo-button--submit btn btn-primary']"
    bo_user_xpath = ".//*[@id='players']/tbody/tr/td[3]/a"
    bo_account_status_selector_css = "select[id='player_user_userStatus'][class='bo-field__control form-control bo-field__control--select']"
    bo_account_status_selector_active_value = "active"
    bo_update_button_css = "button[id='player_0'][class='bo-button bo-button--primary bo-button--submit btn btn-primary'][type='submit']"
    bo_update_1st_button_xpath = ".//*[@id='player_0'][1]"

    '''
    PLAYER INFORMATION
    '''
    bo_player_information_link_suffix = "/bo/player!view?userId="
    bo_player_information_header_text = "Player Profile"
    bo_player_information_header_xpath = '//*[@id="bo-page-player-view"]/div/div/div/div/div[2]/div[1]/div[2]/div[5]/div[1]/div[1]/div[1]'
    bo_player_information_balance_tab_xpath = '//*[@id="bo-page-player-view"]/div[1]/div/div/div/div[2]/div[1]/div[2]/div[6]/div[2]/div/div/form/fieldset/div/ul/li[1]/a'
    bo_player_information_balance_tab_cash_balance_xpath = '//*[@id="_account_cashBalance_formatted"]'
    bo_player_information_balance_tab_promo_balance_xpath = '//*[@id="_account_promoBalance_formatted"]'
    bo_player_information_balance_tab_total_balance_xpath = '//*[@id="_player_account_totalBalance_label"]/a'

    bo_player_information_vouchers_xpath = '//*[@id="bo-page-player-view"]/div[1]/div/div/div/div[2]/div[1]/div[2]/div[6]/div[1]/div[2]/div/div/div[1]/a'
