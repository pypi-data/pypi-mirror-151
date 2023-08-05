"""
Created on July 26, 2021

@author: Siro

"""


class BoRebateElementsMaps(object):

    bo_rebate_link_xpath = '//*[@id="bo-page-rebate-rebate-instances"]/div/div/div/div/div[1]/nav/div/ul/li[5]/a/span/span'
    bo_rebate_instance_link_css = 'a[class="bo-nav__control"][href="rebateInstances!search?status=ACTIVE"]'
    bo_rebate_create_new_instance_link_css = 'a[class="bo-link bo-filter__link"][href="rebateCreateInstance!view"]'
    bo_rebate_create_new_instance_name_field_css = '//*[@id="rebateCreateInstance_entity_name"]'

    bo_rebate_categories_header_text = 'Rebate Categories'
    bo_rebate_games_header_text = 'Rebate Games'
    bo_rebate_categories_header_xpath = '//*[@id="bo-page-rebate-rebate-categories"]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]'
    bo_rebate_games_header_xpath = '//*[@id="bo-page-rebate-rebate-games"]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]'
    bo_rebate_games_game_id_field_xpath = '//*[@id="rebateGames_gameId"]'
    bo_rebate_games_search_button_xpath = '//*[@id="rebateGames_0"]'
    bo_rebate_games_searched_item_game_id_column_xpath = '//*[@id="games"]/tbody/tr/td[3]'
    bo_rebate_games_searched_item_rebate_category_column_select_xpath = '//*[@id="rebateGames_config_categoryId"]'

    bo_rebate_create_new_category_link = 'https://bo-dev.onladv.com/bo/rebateCreateCategory!view?create=true'
    bo_rebate_create_new_category_header_text = 'CREATE REBATE CATEGORY'
    bo_rebate_create_new_category_header_xpath = '//*[@id="bo-page-rebate-rebate-category-create"]/div[1]/div/div/div/div[2]/div[1]/div[1]/div/div/ol/li[3]/a'
    bo_rebate_create_new_rebate_category_css = 'a[href="rebateCreateCategory!view?create=true"][class="bo-link bo-filter__link"]'

    bo_rebate_create_new_rebate_category_name_xpath = '//*[@id="rebateCreateCategory_entity_name"]'
    bo_rebate_create_new_rebate_category_slug_xpath = '//*[@id="rebateCreateCategory_entity_slug"]'
    bo_rebate_create_new_rebate_category_cash_rebate_factor_xpath = '//*[@id="rebateCreateCategory_entity_factor_formatted"]'
    bo_rebate_create_new_rebate_category_button_xpath = '//*[@id="rebateCreateCategory_0"]/span'
    bo_rebate_create_new_rebate_category_successful_css = "div[class='bo-alert bo-alert--success bo-alert--dismissible alert alert-success alert-dismissible fade in']"
    bo_rebate_rebate_categories_link_css = 'a[class="bo-breadcrumbs__item"][href="rebateCategories!search"]'

    bo_rebate_latest_rebate_category_name_item_xpath = '//*[@id="entities"]/tbody/tr[1]/td[2]/a'

    bo_rebate_template_header_text = 'Rebate Templates'
    bo_rebate_template_header_xpath = '//*[@id="bo-page-rebate-rebate-templates"]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]'
    bo_rebate_template_create_new_rebate_template_css = 'a[href="rebateCreateTemplate!view"][class="bo-link bo-filter__link"]'

    bo_rebate_template_create_new_rebate_template_header_text = 'Create New Rebate Template'
    bo_rebate_template_create_new_rebate_template_header_css = 'a[class="bo-breadcrumbs__item"][href="rebateCreateTemplate!view"]'
    bo_rebate_template_name_field_xpath = '//*[@id="rebateCreateTemplate_entity_name"]'
    bo_rebate_template_type_select_xpath = '//*[@id="rebateCreateTemplate_entity_type"]'
    bo_rebate_template_multiplier_field_xpath = '//*[@id="rebateCreateTemplate_entity_multiplier_formatted"]'
    bo_rebate_template_description_textarea_xpath = '//*[@id="rebateCreateTemplate_entity_description"]'
    bo_rebate_template_title_field_xpath = '//*[@id="rebateCreateTemplate_entity_title"]'
    bo_rebate_template_slug_field_xpath = '//*[@id="rebateCreateTemplate_entity_slug"]'
    bo_rebate_template_duration_field_xpath = '//*[@id="rebateCreateTemplate_entity_duration"]'
    bo_rebate_template_note_textarea_xpath = '//*[@id="rebateCreateTemplate_entity_note"]'

    bo_rebate_template_note_max_Number_of_round_field_xpath = '//*[@id="rebateCreateTemplate_entity_maxRounds_formatted"]'
    bo_rebate_template_max_total_rebate_button_xpath = '//*[@id="rebateCreateTemplate"]/fieldset/div[2]/div[2]/div[2]/div/div/div/div/button'
    bo_rebate_template_dialog_key_xpath = '//*[@id="key_0"]'
    bo_rebate_template_dialog_value_xpath = '//*[@id="value_0"]'
    bo_rebate_template_dialog_update_button_xpath = '//*[@id="bo-modal-metadata"]/div/div/div[2]/div/div[2]/button[1]'
    bo_rebate_template_dialog_add_button_xpath = '//*[@id="bo-modal-metadata"]/div/div/div[2]/div/div[2]/button[2]'


    bo_rebate_template_max_bet_contribution_button_xpath = '//*[@id="rebateCreateTemplate"]/fieldset/div[2]/div[2]/div[4]/div[1]/div/div/div/button'
    bo_rebate_template_cap_maximum_bet_checkbox_xpath = '//*[@id="rebateCreateTemplate_entity_maxBetCap"]'
    bo_rebate_template_maximum_rebate_points_per_round_button_xpath = '//*[@id="rebateCreateTemplate"]/fieldset/div[3]/div[2]/div[4]/div/div/div/div/button'

    bo_rebate_template_min_bet_requirement_button_xpath = '//*[@id="rebateCreateTemplate"]/fieldset/div[2]/div[2]/div[3]/div/div/div/div/button'

    bo_rebate_template_instant_rebate_to_rebate_point_balance_checkbox_xpath = '//*[@id="rebateCreateTemplate_entity_instantPay"]'
    bo_rebate_template_pay_after_completion_checkbox_xpath = '//*[@id="rebateCreateTemplate_entity_payCompleted"]'
    bo_rebate_template_create_new_rebate_template_button_xpath = '//*[@id="rebateCreateTemplate_0"]'

    bo_rebate_template_modify_rebate_template_header_text = 'Modify Rebate Template'
    bo_rebate_template_modify_rebate_template_header_xpath = '//*[@id="bo-page-rebate-rebate-template"]/div[1]/div/div/div/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]'
    bo_rebate_template_modify_rebate_template_rule_tab_xpath = '//*[@id="bo-page-rebate-rebate-template"]/div[1]/div/div/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div/ul/li[4]'

    bo_rebate_template_modify_rebate_template_rebate_category_select_xpath = '//*[@id="rebateTemplate_ruleCategory"]'
    bo_rebate_template_modify_rebate_template_game_provider_select_xpath = '//*[@id="rebateTemplate_ruleProvider"]'
    bo_rebate_template_modify_rebate_template_game_textarea_xpath = '//*[@id="rebateTemplate_ruleGame"]'
    bo_rebate_template_modify_rebate_template_game_category_select_xpath = '//*[@id="rebateTemplate_ruleGameCategory"]'

    bo_rebate_template_modify_rebate_template_add_rebate_category_button_css = 'button[type="button"][id="addRebateCategory"][value="Submit"][class="bo-button bo-button--primary bo-button--submit btn btn-primary"]'
    bo_rebate_template_modify_rebate_template_add_game_provider_button_css = 'button[type="button"][id="addRuleProvider"][value="Submit"][class="bo-button bo-button--primary bo-button--submit btn btn-primary"]'
    bo_rebate_template_modify_rebate_template_add_game_button_css = 'button[type="button"][id="addRuleGame"][value="Submit"][class="bo-button bo-button--primary bo-button--submit btn btn-primary"]'
    bo_rebate_template_modify_rebate_template_add_game_category_button_css = 'button[type="button"][id="addGameCategory"][value="Submit"][class="bo-button bo-button--primary bo-button--submit btn btn-primary"]'

    bo_rebate_template_modify_rebate_template_details_tab_css = 'li[class="bo-tabs__item bo-tabs__item--1 bo-nav__item"]'
    bo_rebate_template_modify_rebate_template_activate_button_xpath = '//*[@id="rebateTemplate_2"]'

    bo_rebate_template_modify_rebate_template_activated_css = 'div[class="bo-alert bo-alert--success bo-alert--dismissible alert alert-success alert-dismissible fade in"]'

    bo_rebate_instances_header_text = 'Rebate Instances'
    bo_rebate_instances_header_xpath = '//*[@id="bo-page-rebate-rebate-instances"]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]'
    bo_rebate_instances_create_instance_header_text = 'Create Instance'
    bo_rebate_instances_create_instance_header_xpath = '//*[@id="bo-page-rebate-rebate-instance-create"]/div[1]/div/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/div/div[1]'
    bo_rebate_instances_create_instance_name_field_xpath = '//*[@id="rebateCreateInstance_createRebateRequest_name"]'
    bo_rebate_instances_create_instance_multiplier_field_xpath = '//*[@id="rebateCreateInstance_createRebateRequest_multiplier_formatted"]'
    bo_rebate_instances_create_instance_type_select_xpath = '//*[@id="rebateCreateInstance_createRebateRequest_type"]'
    bo_rebate_instances_create_instance_title_field_xpath = '//*[@id="rebateCreateInstance_createRebateRequest_title"]'
    bo_rebate_instances_create_instance_slug_field_xpath = '//*[@id="rebateCreateInstance_createRebateRequest_slug"]'
    bo_rebate_instances_create_instance_note_textarea_xpath = '//*[@id="rebateCreateInstance_createRebateRequest_note"]'
    bo_rebate_instances_create_instance_end_time_field_xpath = '//*[@id="rebateCreateInstance_createRebateRequest_endTime"]'
    bo_rebate_instances_create_instance_duration_field_xpath = '//*[@id="rebateCreateInstance_createRebateRequest_duration"]'
    bo_rebate_instances_create_instance_user_id_textarea_xpath = '//*[@id="rebateCreateInstance_createRebateRequest_awardUserList"]'
    bo_rebate_instances_create_instance_exclude_user_checkbox_xpath = '//*[@id="rebateCreateInstance_createRebateRequest_excludeUser"]'
    bo_rebate_instances_create_instance_max_number_of_round_field_xpath = '//*[@id="rebateCreateInstance_createRebateRequest_maxRounds_formatted"]'
    bo_rebate_instances_create_instance_max_total_rebate_button_xpath = '//*[@id="rebateCreateInstance"]/fieldset/div[4]/div[2]/div[2]/div/div/div/div/button'
    bo_rebate_instances_create_instance_min_bet_requirement_button_xpath = '//*[@id="rebateCreateInstance"]/fieldset/div[4]/div[2]/div[3]/div/div/div/div/button'
    bo_rebate_instances_create_instance_max_bet_contribution_button_xpath = '//*[@id="rebateCreateInstance"]/fieldset/div[4]/div[2]/div[4]/div[1]/div/div/div/button'
    bo_rebate_instances_create_instance_cap_maximum_bet_checkbox_xpath = '//*[@id="rebateCreateInstance_createRebateRequest_maxBetCap"]'
    bo_rebate_instances_create_instance_maximum_rebate_points_per_round_button_xpath = '//*[@id="rebateCreateInstance"]/fieldset/div[5]/div[2]/div[4]/div/div/div/div/button'

    bo_rebate_instances_dialog_key_xpath = '//*[@id="key_0"]'
    bo_rebate_instances_dialog_value_xpath = '//*[@id="value_0"]'
    bo_rebate_instances_dialog_update_button_xpath = '//*[@id="bo-modal-metadata"]/div/div/div[2]/div/div[2]/button[1]'
    bo_rebate_instances_dialog_add_button_xpath = '//*[@id="bo-modal-metadata"]/div/div/div[2]/div/div[2]/button[2]'

    bo_rebate_instances_create_instance_instant_rebate_to_rebate_point_balance_checkbox_xpath = '//*[@id="rebateCreateInstance_createRebateRequest_instantPay"]'
    bo_rebate_instances_create_instance_pay_after_completion_checkbox_xpath = '//*[@id="rebateCreateInstance_createRebateRequest_payCompleted"]'
    bo_rebate_instances_create_instance_button_xpath = '//*[@id="rebateCreateInstance_0"]'

    bo_rebate_instances_modify_rebate_instance_header_text = 'Modify Instance'
    bo_rebate_instances_modify_rebate_instance_header_xpath = '//*[@id="bo-page-rebate-rebate-instance"]/div[1]/div/div/div/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/div[1]'
    bo_rebate_instances_modify_rebate_instance_rule_tab_xpath = '//*[@id="bo-page-rebate-rebate-instance"]/div[1]/div/div/div/div[2]/div[1]/div[2]/div[3]/div[2]/div[1]/div/div/ul/li[5]/a'

    bo_rebate_instances_modify_rebate_instance_rebate_category_select_xpath = '//*[@id="rebateInstance_ruleCategory"]'
    bo_rebate_instances_modify_rebate_instance_game_provider_select_xpath = '//*[@id="rebateInstance_ruleProvider"]'
    bo_rebate_instances_modify_rebate_instance_game_textarea_xpath = '//*[@id="rebateInstance_ruleGame"]'
    bo_rebate_instances_modify_rebate_instance_game_category_select_xpath = '//*[@id="rebateInstance_ruleGameCategory"]'

    bo_rebate_instances_modify_rebate_instance_add_rebate_category_button_css = 'button[type="button"][id="addRebateCategory"][value="Submit"][class="bo-button bo-button--primary bo-button--submit btn btn-primary"]'
    bo_rebate_instances_modify_rebate_instance_add_game_provider_button_css = 'button[type="button"][id="addRuleProvider"][value="Submit"][class="bo-button bo-button--primary bo-button--submit btn btn-primary"]'
    bo_rebate_instances_modify_rebate_instance_add_game_button_css = 'button[type="button"][id="addRuleGame"][value="Submit"][class="bo-button bo-button--primary bo-button--submit btn btn-primary"]'
    bo_rebate_instances_modify_rebate_instance_add_game_category_button_css = 'button[type="button"][id="addGameCategory"][value="Submit"][class="bo-button bo-button--primary bo-button--submit btn btn-primary"]'

    bo_rebate_instances_modify_rebate_instance_details_tab_css = 'li[class="bo-tabs__item bo-tabs__item--1 bo-nav__item"]'
    bo_rebate_instances_modify_rebate_instance_activate_button_xpath = '//*[@id="rebateInstance_2"]'

    bo_rebate_instances_modify_rebate_instance_added_rule_text_xpath = '//*[@id="bo-page-rebate-rebate-instance"]/div[1]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/p'
    bo_rebate_instances_modify_rebate_instance_added_rule_successfully_text = 'Entity has been activated.'
