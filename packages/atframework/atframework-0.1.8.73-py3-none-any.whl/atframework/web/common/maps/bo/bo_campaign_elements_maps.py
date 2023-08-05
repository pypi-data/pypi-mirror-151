"""
Created on Aug 18, 2021

@author: Siro

"""


class BoCampaignElementsMaps(object):

    """
    Create new campaign
    """
    bo_campaign_create_new_campaign_header_xpath = "//*[@id='bo-page-campaigns-create']/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]"
    bo_campaign_create_new_campaign_header_text = "Please input a new campaign details"
    bo_campaign_campaign_type_select_css = "select[name='campaign.campaignType'][id='campaignCreate_campaign_campaignType']"
    bo_campaign_campaign_type_select_xpath = '//*[@id="campaignCreate_campaign_campaignType"]'
    bo_campaign_select_player_deposit_code_value = "deposit_code"
    bo_campaign_select_player_deposit_all_value = "deposit_all"
    bo_campaign_select_n_deposit_value = "n_deposit"
    bo_campaign_select_registration_code_value = "registration_code"
    bo_campaign_select_registration_all_value = "registration_all"
    bo_campaign_select_player_campaign_value = "player_campaign"
    bo_campaign_select_player_campaign_with_code_value = "player_campaign_with_code"
    bo_campaign_select_n_deposit_with_code_value = "n_deposit_with_code"

    bo_campaign_name_field_xpath = '//*[@id="campaignCreate_campaign_name"]'
    bo_campaign_turnover_factor_field_xpath = '//*[@id="campaignCreate_campaign_turnoverFactor"]'
    bo_campaign_end_time_field_xpath = '//*[@id="campaignCreate_campaign_endTime"]'

    bo_campaign_free_spin_tab_xpath = '//*[@id="campaignCreate"]/fieldset/div[3]/div/div/ul/li[1]'
    bo_campaign_cash_tab_xpath = '//*[@id="campaignCreate"]/fieldset/div[3]/div/div/ul/li[2]/a'
    bo_campaign_promo_tab_xpath = '//*[@id="campaignCreate"]/fieldset/div[3]/div/div/ul/li[3]/a'
    bo_campaign_rebate_tab_xpath = "//*[@id='campaignCreate']/fieldset/div[3]/div/div/ul/li[4]/a"
    bo_campaign_free_spin_bonus_in_voucher_checkbox_xpath = "//*[@id='campaignCreate_formData_freeSpinsBonusInVoucher']"
    bo_campaign_cash_bonus_in_voucher_checkbox_xpath = "//*[@id='campaignCreate_formData_cashBonusInVoucher']"
    bo_campaign_promo_bonus_in_voucher_checkbox_xpath = '//*[@id="campaignCreate_formData_promoBonusInVoucher"]'
    bo_campaign_rebate_bonus_in_voucher_checkbox_xpath = '//*[@id="campaignCreate_formData_rebateBonusInVoucher"]'
    bo_campaign_cash_tab_cash_amount_xpath = '//*[@id="campaignCreate_cashDto_amount_formatted"]'
    bo_campaign_promo_tab_promo_amount_xpath = '//*[@id="campaignCreate_promoDto_amount_formatted"]'

    bo_campaign_users_select_xpath = '//*[@id="campaignCreate_userIdsType"]'
    bo_campaign_users_select_user_from_list_text = 'Select user from list'
    bo_campaign_users_user_id_list_textarea_xpath = '//*[@id="campaignCreate_campaign_userIds"]'

    bo_campaign_create_new_campaign_button_xpath = '//*[@id="campaignCreate_0"]'

    bo_campaign_translation_field_xpath = '//*[@id="campaignCreate_billfoldMessage_message"]'
    bo_campaign_new_campaign_created_id_xpath = '//*[@id="bo-page-campaigns-create"]/div[1]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/p/a'
    bo_campaign_create_successful_css = "div[class='bo-alert bo-alert--success bo-alert--dismissible alert alert-success alert-dismissible fade in']"

    """
    campaign information
    """

    bo_campaign_information_header_xpath = '//*[@id="bo-page-campaigns-view"]/div[1]/div/div/div/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]'
    bo_campaign_information_header_text = "Campaign Details"
    bo_campaign_information_link_suffix = "/bo/campaign!view?campaignId="

    bo_campaign_information_status_xpath = '//*[@id="campaign_campaign_campaignStatus"]'
    bo_campaign_information_status_selector_active_value = "cancelled"
    bo_campaign_information_update_button = "button[type='submit'][id='campaign_0'][class='bo-button bo-button--primary bo-button--submit btn btn-primary']"

    bo_campaign_information_benefit_user_id_xpath ='//*[@id="campaignUsage"]/tbody/tr/td[3]/a'
    bo_campaign_information_benefit_reward_type_xpath ='//*[@id="campaignUsage"]/tbody/tr/td[5]'
    bo_campaign_information_benefit_reward_type_direct_text ='Direct'
    bo_campaign_information_benefit_reward_type_voucher_text ='Voucher'
    bo_campaign_information_benefit_bonus_amount_xpath ='//*[@id="campaignUsage"]/tbody/tr/td[6]'
    bo_campaign_information_benefit_balance_type_xpath ='//*[@id="campaignUsage"]/tbody/tr/td[7]'
    bo_campaign_information_benefit_balance_type_promo_text ='Promo'
    bo_campaign_information_benefit_balance_type_Cash_text ='Cash'
    bo_campaign_information_benefit_bonus_status_xpath ='//*[@id="campaignUsage"]/tbody/tr/td[10]'
    bo_campaign_information_benefit_bonus_status_text ='success'
