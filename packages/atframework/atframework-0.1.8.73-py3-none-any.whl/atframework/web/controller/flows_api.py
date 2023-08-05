'''
Created on Mar 03, 2021

@author: Siro

'''

from atframework.web.common.maps.resource_maps import ResourceMaps
from atframework.web.common.maps.elements_maps import ElementsMaps
from atframework.web.helper.model_helper import ModelHelper
from atframework.tools.log.config import logger
from atframework.web.utils.utils import Utils


class FlowsAPI(ModelHelper):
    '''
    Integrate all flows to this class, Use this class to drive test steps
    '''
    em = ElementsMaps()
    rm = ResourceMaps()

    test_email = rm.TEST_EMAIL

    def open_the_browser(self):
        logger.info('[AtLog] ----- start to init browser driver')
        return self.setup_browser(self.rm.BROWSER_NAME)

    def bring_browser_to_front(self):
        logger.info('[AtLog] ----- bring the browser to front')
        self.bring_to_front()

    def close_the_browser(self):
        self.teardown_browser()

    def get_screenshot_file(self, file_name):
        self.take_screenshot_file(file_name)

    '''
    ----------BO--lV_1 api ---------
    '''

    def bo_login(self, username=rm.USERNAME_BO, password=rm.PASSWORD_BO, site=rm.RUNNING_SITE,
                 bo_site_id=rm.BO_SITE_ID):
        """
        login form bo.

        :param username: Bo login name
        :param password: Bo login password
        :param site: login site address
        :return: none
        """
        logger.info('[AtLog] ----- Access BO')
        self.access_web_url_till_one_time(self.rm.BO_ADDRESS)
        logger.info('[AtLog] ----- Reload BO to find elements')
        self.access_web_url_till_one_time(self.rm.BO_ADDRESS)
        logger.info('[AtLog] ----- Input admin')
        self.type_text_in_field_via_css(self.em.bo_username_field_css,
                                username)
        logger.info('[AtLog] ----- Input password')
        self.type_text_in_field_via_css(self.em.bo_password_field_css,
                                   password)
        logger.info('[AtLog] ----- Click the login button on BO')
        self.click_element_via_css(self.em.bo_login_button_css)
        logger.info('[AtLog] ----- check whether the site is selected on bo')
        if self.is_find_link_via_css(
                self.em.bo_site_not_select_text_css) is True:
            logger.info('[AtLog] ----- select site on BO')
            if site == 'dev':
                self.waits(3)
                logger.info('[AtLog] ----- click select site button')
                self.click_element_via_css(self.em.bo_site_select_button_css)
                self.waits(1)
                logger.info('[AtLog] ----- select BO site by bo_site_id on Dev')
                # self.click_element_via_xpath(self.em.bo_site_select_luckycasino_xpath)
                self.click_element_via_partial_text("(" + str(bo_site_id) + ")")
                self.waits(2)
            else:
                self.waits(3)
                logger.info('[AtLog] ----- select BO site by bo_site_id')
                self.click_element_via_css(self.em.bo_site_select_button_css)
                self.waits(1)
                self.click_element_via_partial_text("(" + str(bo_site_id) + ")")
                self.waits(2)
        else:
            logger.info('[AtLog] ----- the site is selected on BO')
            pass

    def bo_is_login(self):
        """
        is logged in on bo.

        :param: none
        :return: whether logged in
        """
        logger.info('[AtLog] ----- Check whether logged in on BO')
        return self.is_find_link_via_css(self.em.bo_home_link_css)

    '''
    ----------BO--lV_2 api ---------
    '''

    def bo_search_player(self, player_text, flag=0):
        """
        @precondition: the player is logged in on bo.
        This is search player from bo.

        :param player_text:
        :param flag: 0: input the search text and click enter in keyboard,
        1:input the search text, then click search button
        :return: whether search player successfully

        """
        logger.info('[AtLog] ----- Click the helpdesk link')
        self.click_link_via_css(self.em.bo_helpdesk_link_css)
        self.waits(4)
        if flag == 0:
            logger.info(
                '[AtLog] ----- input search text and press Enter button on keyboard'
            )
            self.type_text_via_xpath_and_enter(
                self.em.bo_search_text_field_xpath, player_text)
            self.waits(4)
        elif flag == 1:
            logger.info('[AtLog] ----- input search text')
            self.type_text_in_field_via_css(self.em.bo_search_text_field_css,
                                          player_text)
            logger.info('[AtLog] ----- click search button')
            self.click_link_via_css(self.em.bo_search_button_css)
        return self.is_find_link_via_text(player_text)

    def bo_access_rebate_templates(self):
        """
        @precondition: the player is logged in on bo.

        :return: whether access rebate templates successfully

        """
        if self.is_find_element_via_css(self.em.bo_menu_rebate_categories_css) is False:
            logger.info('[AtLog] ----- expand the Rebate menu')
            self.expand_menu_via_css_from_list(self.em.bo_menu_rebate_expand_icon_css, index=3)
        logger.info('[AtLog] ----- Open the Rebate templates page')
        self.click_element_via_css(self.em.bo_menu_rebate_templates_css)
        logger.info('[AtLog] ----- Check whether in the Rebate templates')
        return self.is_page_shown_via_xpath_expected_text(self.em.bo_rebate_template_header_xpath, self.em.bo_rebate_template_header_text)

    def bo_access_create_rebate_template(self):
        """
        @precondition: the player is logged in on bo.

        :return: whether access create rebate templates successfully

        """
        logger.info('[AtLog] ----- Check whether in the Rebate templates')
        if self.is_page_shown_via_xpath_expected_text(self.em.bo_rebate_template_header_xpath, self.em.bo_rebate_template_header_text) is False:
            logger.info('[AtLog] ----- Start to access Rebate templates')
            self.bo_access_rebate_templates()
        else:
            logger.info('[AtLog] ----- It is in Rebate templates')
            pass
        logger.info('[AtLog] ----- Click create new rebate templates')
        self.click_element_via_css(self.em.bo_rebate_template_create_new_rebate_template_css)
        logger.info('[AtLog] ----- Check whether in create new rebate category')
        return self.is_page_shown_via_css_expected_text(self.em.bo_rebate_template_create_new_rebate_template_header_css,
                                                  self.em.bo_rebate_template_create_new_rebate_template_header_text)

    def bo_create_rebate_template(self, name=rm.REBATE_TEMPLATE_NAME, type=rm.REBATE_TEMPLATE_TYPE,
                                  multiplier=rm.REBATE_TEMPLATE_MULTIPLIER, description=rm.REBATE_TEMPLATE_DESCRIPTION,
                                  title=rm.REBATE_TEMPLATE_TITLE, slug=rm.REBATE_TEMPLATE_SLUG,
                                  duration=rm.REBATE_TEMPLATE_DURATION, note=rm.REBATE_TEMPLATE_NOTE,
                                  max_number_of_round=rm.REBATE_TEMPLATE_MAX_NUMBER_OF_ROUND,
                                  max_total_rebate=rm.REBATE_TEMPLATE_MAX_TOTAL_REBATE,
                                  min_bet_requirement=rm.REBATE_TEMPLATE_MIN_BET_REQUIREMENT,
                                  max_bet_contribution=rm.REBATE_TEMPLATE_MAX_BET_CONTRIBUTION,
                                  cap_max_bet=rm.REBATE_TEMPLATE_CAP_MAX_BET,
                                  max_rebate_points_per_round=rm.REBATE_TEMPLATE_MAX_REBATE_POINTS_PER_ROUND,
                                  rebate_payout_settings=rm.REBATE_TEMPLATE_PAYOUT_SETTINGS,
                                  rule_rebate_category=rm.REBATE_TEMPLATE_RULE_REBATE_CATEGORY,
                                  rule_game_provider=rm.REBATE_TEMPLATE_RULE_GAME_PROVIDER,
                                  rule_game=rm.REBATE_TEMPLATE_RULE_GAME,
                                  rule_game_category=rm.REBATE_TEMPLATE_RULE_GAME_CATEGORY):
        """
        @precondition: the player is logged in on bo.

        :param: name=rm.REBATE_TEMPLATE_NAME,
        :param: type=rm.REBATE_TEMPLATE_TYPE,
        :param: multiplier=rm.REBATE_CATEGORY_SLUG,
        :param: description=rm.REBATE_TEMPLATE_DESCRIPTION,
        :param: title=rm.REBATE_TEMPLATE_TITLE,
        :param: slug=rm.REBATE_TEMPLATE_SLUG,
        :param: duration=rm.REBATE_TEMPLATE_DURATION,
        :param: note=rm.REBATE_TEMPLATE_NOTE,
        :param: max_number_of_round=rm.REBATE_TEMPLATE_MAX_NUMBER_OF_ROUND,
        :param: max_total_rebate=rm.REBATE_TEMPLATE_MAX_TOTAL_REBATE,
        :param: min_bet_requirement=rm.REBATE_TEMPLATE_MIN_BET_REQUIREMENT,
        :param: max_bet_contribution=rm.REBATE_TEMPLATE_MAX_BET_CONTRIBUTION,
        :param: cap_max_bet=rm.REBATE_TEMPLATE_CAP_MAX_BET,
        :param: max_rebate_points_per_round=rm.REBATE_TEMPLATE_MAX_REBATE_POINTS_PER_ROUND,
        :param: rebate_payout_settings=rm.REBATE_TEMPLATE_PAYOUT_SETTINGS,
        :param: rule_rebate_category=rm.REBATE_TEMPLATE_RULE_REBATE_CATEGORY,
        :param: rule_game_provider=rm.REBATE_TEMPLATE_RULE_GAME_PROVIDER,
        :param: rule_game=rm.REBATE_TEMPLATE_RULE_GAME,
        :param: rule_game_category=rm.REBATE_TEMPLATE_RULE_GAME_CATEGORY
        :return: whether create rebate template successfully

        """
        logger.info('[AtLog] ----- Whether in CREATE NEW REBATE TEMPLATE page')
        if self.is_page_shown_via_css_expected_text(self.em.bo_rebate_template_create_new_rebate_template_header_css,
                                               self.em.bo_rebate_template_create_new_rebate_template_header_text) is True:
            logger.info('[AtLog] ----- Accessed CREATE NEW REBATE TEMPLATEpage')
            pass
        else:
            logger.info('[AtLog] ----- Start to access CREATE NEW REBATE TEMPLATE page')
            self.bo_access_create_rebate_template()

        logger.info('[AtLog] ----- Input name of rebate template')
        self.type_text_in_field_via_xpath(self.em.bo_rebate_template_name_field_xpath, name)
        logger.info('[AtLog] ----- Select type of rebate template')
        self.select_dropdown_menu_element_via_locator_text(self.em.bo_rebate_template_type_select_xpath, type)
        logger.info('[AtLog] ----- Input Multiplier of rebate template')
        self.type_text_in_field_via_xpath(self.em.bo_rebate_template_multiplier_field_xpath, multiplier)
        if description is not None:
            logger.info('[AtLog] ----- Input Description of rebate template')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_template_description_textarea_xpath, description)
        if title is not None:
            logger.info('[AtLog] ----- Input Title of rebate template')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_template_title_field_xpath, title)
        if slug is not None:
            logger.info('[AtLog] ----- Input Slug of rebate template')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_template_slug_field_xpath, slug)
        logger.info('[AtLog] ----- Input Duration of rebate template')
        self.type_text_in_field_via_xpath(self.em.bo_rebate_template_duration_field_xpath, duration)
        if note is not None:
            logger.info('[AtLog] ----- Input Note of rebate template')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_template_note_textarea_xpath, note)
        logger.info('[AtLog] ----- Input Max Number of round(s)/spin(s) of rebate template')
        self.type_text_in_field_via_xpath(self.em.bo_rebate_template_note_max_Number_of_round_field_xpath, max_number_of_round)
        logger.info('[AtLog] ----- Click button of Max Total Rebate of rebate template')
        self.click_element_via_xpath(self.em.bo_rebate_template_max_total_rebate_button_xpath)
        logger.info('[AtLog] ----- Input Max total bet')
        self.type_text_in_field_via_xpath(self.em.bo_rebate_template_dialog_key_xpath,
                                           'default')
        self.type_text_in_field_via_xpath(self.em.bo_rebate_template_dialog_value_xpath,
                                           max_total_rebate)
        self.click_element_via_xpath(self.em.bo_rebate_template_dialog_update_button_xpath)
        if min_bet_requirement is not None:
            logger.info('[AtLog] ----- Click Min Bet Requirement button of rebate template')
            self.click_element_via_xpath(self.em.bo_rebate_template_min_bet_requirement_button_xpath)
            logger.info('[AtLog] ----- Input Min Bet Requirement')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_template_dialog_key_xpath,
                                               'default')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_template_dialog_value_xpath,
                                               min_bet_requirement)
            self.click_element_via_xpath(self.em.bo_rebate_template_dialog_update_button_xpath)
        if max_bet_contribution is not None:
            logger.info('[AtLog] ----- Click Max Bet Contribution button of rebate template')
            self.click_element_via_xpath(self.em.bo_rebate_template_max_bet_contribution_button_xpath)
            logger.info('[AtLog] ----- Input Max Bet Contribution')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_template_dialog_key_xpath,
                                               'default')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_template_dialog_value_xpath,
                                               max_bet_contribution)
            self.click_element_via_xpath(self.em.bo_rebate_template_dialog_update_button_xpath)
            if cap_max_bet is True:
                logger.info('[AtLog] ----- tick Cap Maximum Bet  of rebate template')
                self.click_element_via_xpath(self.em.bo_rebate_template_cap_maximum_bet_checkbox_xpath)

        if max_rebate_points_per_round is not None:
            logger.info('[AtLog] ----- Input Maximum Rebate Points per Round of rebate template')
            self.click_element_via_xpath(self.em.bo_rebate_template_maximum_rebate_points_per_round_button_xpath)
            logger.info('[AtLog] ----- Input Max Bet Contribution')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_template_dialog_key_xpath,
                                               'default')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_template_dialog_value_xpath,
                                               max_rebate_points_per_round)
            self.click_element_via_xpath(self.em.bo_rebate_template_dialog_update_button_xpath)

        if rebate_payout_settings == 'instant':
            logger.info('[AtLog] ----- tick checkbox of Instant Rebate to Rebate Point balance of rebate template')
            self.click_element_via_xpath(self.em.bo_rebate_template_instant_rebate_to_rebate_point_balance_checkbox_xpath)
        elif rebate_payout_settings == 'completion':
            logger.info('[AtLog] ----- tick checkbox of Pay After Completion rebate template')
            self.click_element_via_xpath(
                self.em.bo_rebate_template_pay_after_completion_checkbox_xpath)
        else:
            logger.error('[AtLog] ----- Setting type just has Instant Rebate to Rebate Point balance and Pay After Completion ')
            return False
        logger.info('[AtLog] ----- Click Create new rebate template button')
        self.click_element_via_xpath(
            self.em.bo_rebate_template_create_new_rebate_template_button_xpath)

        logger.info('[AtLog] ----- Check whether in the Modify rebate template page')
        if self.is_page_shown_via_xpath_expected_text(self.em.bo_rebate_template_modify_rebate_template_header_xpath,
                                                self.em.bo_rebate_template_modify_rebate_template_header_text) is True:
            if rule_rebate_category is not None or rule_game_provider is not None or rule_game is not None or rule_game_category is not None:
                logger.info('[AtLog] ----- Click Rule tab in the Modify rebate template page')
                self.click_element_via_xpath(self.em.bo_rebate_template_modify_rebate_template_rule_tab_xpath)
                if rule_rebate_category is not None:
                    logger.info('[AtLog] ----- Add Rule of rebate category in the Modify rebate template page')
                    self.select_dropdown_menu_element_via_locator_text(self.em.bo_rebate_template_modify_rebate_template_rebate_category_select_xpath, rule_rebate_category)
                    self.click_element_via_css(self.em.bo_rebate_template_modify_rebate_template_add_rebate_category_button_css)
                if rule_game_provider is not None:
                    logger.info('[AtLog] ----- Add Rule of game provider in the Modify rebate template page')
                    self.select_dropdown_menu_element_via_locator_text(
                        self.em.bo_rebate_template_modify_rebate_template_game_provider_select_xpath,
                        rule_game_provider)
                    self.click_element_via_css(
                        self.em.bo_rebate_template_modify_rebate_template_add_game_provider_button_css)
                if rule_game is not None:
                    logger.info('[AtLog] ----- Add Rule of game in the Modify rebate template page')
                    self.type_text_in_field_via_xpath(self.em.bo_rebate_template_modify_rebate_template_game_textarea_xpath, rule_game)
                    self.click_element_via_css(
                        self.em.bo_rebate_template_modify_rebate_template_add_game_button_css)
                if rule_game_category is not None:
                    logger.info('[AtLog] ----- Add Rule of game category in the Modify rebate template page')
                    self.select_dropdown_menu_element_via_locator_text(
                        self.em.bo_rebate_template_modify_rebate_template_game_category_select_xpath,
                        rule_game_category)
                    self.click_element_via_css(
                        self.em.bo_rebate_template_modify_rebate_template_add_game_category_button_css)
            logger.info('[AtLog] ----- Try to Activate the rebate template')
            logger.info('[AtLog] ----- Click Details tab in the Modify rebate template page')
            self.click_element_via_css(self.em.bo_rebate_template_modify_rebate_template_details_tab_css)
            logger.info('[AtLog] ----- Activate the rebate template')
            self.click_element_via_xpath(self.em.bo_rebate_template_modify_rebate_template_activate_button_xpath)
        else:
            logger.error('[AtLog] ----- It does not redirect to Modify rebate template page')
            return False
        logger.info('[AtLog] ----- Check the rebate template is Active')
        result = self.is_find_element_via_css(self.em.bo_rebate_template_modify_rebate_template_activated_css)
        if result is True:
            logger.info('[AtLog] ----- The rebate template is Active')
            return True
        else:
            logger.error('[AtLog] ----- The rebate template is NOT Active')
            return False

    def bo_access_rebate_instances(self):
        """
        @precondition: the player is logged in on bo.

        :return: whether access rebate instances successfully

        """
        if self.is_find_element_via_css(self.em.bo_menu_rebate_instances_css) is False:
            logger.info('[AtLog] ----- expand the Rebate menu')
            self.expand_menu_via_css_from_list(self.em.bo_menu_rebate_expand_icon_css, index=3)
        logger.info('[AtLog] ----- Click the Rebate instances')
        self.click_element_via_css(self.em.bo_menu_rebate_instances_css)
        logger.info('[AtLog] ----- Check whether in the Rebate instances')
        return self.is_page_shown_via_xpath_expected_text(self.em.bo_rebate_instances_header_xpath, self.em.bo_rebate_instances_header_text)

    def bo_access_create_rebate_instance(self):
        """
        @precondition: the player is logged in on bo.

        :return: whether access create rebate instance successfully

        """
        logger.info('[AtLog] ----- Check whether in the Rebate Instances')
        if self.is_page_shown_via_xpath_expected_text(self.em.bo_rebate_instances_header_xpath,
                                                self.em.bo_rebate_instances_header_text) is False:
            logger.info('[AtLog] ----- Start to access rebate instances')
            self.bo_access_rebate_instances()
        else:
            logger.info('[AtLog] ----- It is in Rebate instances')
            pass
        logger.info('[AtLog] ----- Click create new rebate instance')
        self.click_element_via_css(self.em.bo_rebate_create_new_instance_link_css)
        logger.info('[AtLog] ----- Check whether in create new rebate instance')
        return self.is_page_shown_via_xpath_expected_text(self.em.bo_rebate_instances_create_instance_header_xpath,
                                                    self.em.bo_rebate_instances_create_instance_header_text)

    def bo_create_rebate_instance(self, name=rm.REBATE_INSTANCE_NAME, type=rm.REBATE_INSTANCE_TYPE,
                                  multiplier=rm.REBATE_INSTANCE_MULTIPLIER, title=rm.REBATE_INSTANCE_TITLE,
                                  slug=rm.REBATE_INSTANCE_SLUG, note=rm.REBATE_INSTANCE_NOTE,
                                  end_time=rm.REBATE_INSTANCE_END_TIME, duration=rm.REBATE_INSTANCE_DURATION,
                                  user_id=rm.REBATE_INSTANCE_USER_ID, is_exclude_user=rm.REBATE_INSTANCE_IS_EXCLUDE_USER,
                                  max_number_of_round=rm.REBATE_INSTANCE_MAX_NUMBER_OF_ROUND,
                                  max_total_rebate=rm.REBATE_INSTANCE_MAX_TOTAL_REBATE,
                                  min_bet_requirement=rm.REBATE_INSTANCE_MIN_BET_REQUIREMENT,
                                  max_bet_contribution=rm.REBATE_INSTANCE_MAX_BET_CONTRIBUTION,
                                  cap_max_bet=rm.REBATE_INSTANCE_CAP_MAX_BET,
                                  max_rebate_points_per_round=rm.REBATE_INSTANCE_MAX_REBATE_POINTS_PER_ROUND,
                                  rebate_payout_settings=rm.REBATE_INSTANCE_PAYOUT_SETTINGS,
                                  rule_rebate_category=rm.REBATE_INSTANCE_RULE_REBATE_CATEGORY,
                                  rule_game_provider=rm.REBATE_INSTANCE_RULE_GAME_PROVIDER,
                                  rule_game=rm.REBATE_INSTANCE_RULE_GAME,
                                  rule_game_category=rm.REBATE_INSTANCE_RULE_GAME_CATEGORY):
        """
        @precondition: the player is logged in on bo.

        :param: name=rm.REBATE_INSTANCE_NAME,
        :param: type=rm.REBATE_INSTANCE_TYPE,
        :param: multiplier=rm.REBATE_INSTANCE_MULTIPLIER,
        :param: title=rm.REBATE_INSTANCE_TITLE,
        :param: slug=rm.REBATE_INSTANCE_SLUG,
        :param: duration=rm.REBATE_INSTANCE_DURATION,
        :param: note=rm.REBATE_INSTANCE_NOTE,
        :param: user_id=rm.REBATE_INSTANCE_USER_ID,
        :param: end_time=rm.REBATE_INSTANCE_END_TIME,
        :param: max_number_of_round=rm.REBATE_INSTANCE_MAX_NUMBER_OF_ROUND,
        :param: max_total_rebate=rm.REBATE_INSTANCE_MAX_TOTAL_REBATE,
        :param: min_bet_requirement=rm.REBATE_INSTANCE_MIN_BET_REQUIREMENT,
        :param: max_bet_contribution=rm.REBATE_INSTANCE_MAX_BET_CONTRIBUTION,
        :param: cap_max_bet=rm.REBATE_INSTANCE_CAP_MAX_BET,
        :param: max_rebate_points_per_round=rm.REBATE_INSTANCE_MAX_REBATE_POINTS_PER_ROUND,
        :param: rebate_payout_settings=rm.REBATE_INSTANCE_PAYOUT_SETTINGS,
        :param: rule_rebate_category=rm.REBATE_INSTANCE_RULE_REBATE_CATEGORY,
        :param: rule_game_provider=rm.REBATE_INSTANCE_RULE_GAME_PROVIDER,
        :param: rule_game=rm.REBATE_INSTANCE_RULE_GAME,
        :param: rule_game_category=rm.REBATE_INSTANCE_RULE_GAME_CATEGORY
        :return: whether create rebate template successfully

        """
        logger.info('[AtLog] ----- Whether in CREATE INSTANCE page')
        if self.is_page_shown_via_xpath_expected_text(self.em.bo_rebate_instances_create_instance_header_xpath,
                                                self.em.bo_rebate_instances_create_instance_header_text) is True:
            logger.info('[AtLog] ----- Accessed CREATE INSTANCE page')
            pass
        else:
            logger.info('[AtLog] ----- Start to access CREATE INSTANCE page')
            self.bo_access_create_rebate_instance()

        logger.info('[AtLog] ----- Input name of rebate instance')
        self.type_text_in_field_via_xpath(self.em.bo_rebate_instances_create_instance_name_field_xpath, name)
        logger.info('[AtLog] ----- Select type of rebate instance')
        self.select_dropdown_menu_element_via_locator_text(self.em.bo_rebate_instances_create_instance_type_select_xpath, type)
        logger.info('[AtLog] ----- Input Multiplier of rebate instance')
        self.type_text_in_field_via_xpath(self.em.bo_rebate_instances_create_instance_multiplier_field_xpath, multiplier)

        if title is not None:
            logger.info('[AtLog] ----- Input Title of rebate instance')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_instances_create_instance_title_field_xpath, title)
        if slug is not None:
            logger.info('[AtLog] ----- Input Slug of rebate instance')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_instances_create_instance_slug_field_xpath, slug)
        if note is not None:
            logger.info('[AtLog] ----- Input Note of rebate instance')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_instances_create_instance_note_textarea_xpath, note)

        logger.info('[AtLog] ----- Input Duration of rebate instance')
        self.type_text_in_field_via_xpath(self.em.bo_rebate_instances_create_instance_duration_field_xpath, duration)
        logger.info('[AtLog] ----- Input End Time of rebate instance')
        self.type_text_in_field_via_xpath(self.em.bo_rebate_instances_create_instance_end_time_field_xpath, end_time)

        if user_id is not None:
            logger.info('[AtLog] ----- Input user id')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_instances_create_instance_user_id_textarea_xpath,                                               user_id)
            if is_exclude_user is True:
                logger.info('[AtLog] ----- Exclude the user id')
                self.click_element_via_xpath(self.em.bo_rebate_instances_create_instance_exclude_user_checkbox_xpath)

        logger.info('[AtLog] ----- Input Max Number of round(s)/spin(s) of rebate instance')
        self.type_text_in_field_via_xpath(self.em.bo_rebate_instances_create_instance_max_number_of_round_field_xpath, max_number_of_round)
        logger.info('[AtLog] ----- Click button of Max Total Rebate of rebate instance')
        self.click_element_via_xpath(self.em.bo_rebate_instances_create_instance_max_total_rebate_button_xpath)
        logger.info('[AtLog] ----- Input Max total bet')
        self.type_text_in_field_via_xpath(self.em.bo_rebate_instances_dialog_key_xpath,
                                           'default')
        self.type_text_in_field_via_xpath(self.em.bo_rebate_instances_dialog_value_xpath,
                                           max_total_rebate)
        self.click_element_via_xpath(self.em.bo_rebate_instances_dialog_update_button_xpath)

        if min_bet_requirement is not None:
            logger.info('[AtLog] ----- Click Min Bet Requirement button of rebate instance')
            self.click_element_via_xpath(self.em.bo_rebate_instances_create_instance_min_bet_requirement_button_xpath)
            logger.info('[AtLog] ----- Input Min Bet Requirement')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_instances_dialog_key_xpath,
                                               'default')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_instances_dialog_value_xpath,
                                               min_bet_requirement)
            self.click_element_via_xpath(self.em.bo_rebate_instances_dialog_update_button_xpath)

        if max_bet_contribution is not None:
            logger.info('[AtLog] ----- Click Max Bet Contribution button of rebate instance')
            self.click_element_via_xpath(self.em.bo_rebate_instances_create_instance_max_bet_contribution_button_xpath)
            logger.info('[AtLog] ----- Input Max Bet Contribution')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_instances_dialog_key_xpath,
                                               'default')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_instances_dialog_value_xpath,
                                               max_bet_contribution)
            self.click_element_via_xpath(self.em.bo_rebate_instances_dialog_update_button_xpath)
            if cap_max_bet is True:
                logger.info('[AtLog] ----- tick Cap Maximum Bet of rebate instance')
                self.click_element_via_xpath(self.em.bo_rebate_instances_create_instance_cap_maximum_bet_checkbox_xpath)

        if max_rebate_points_per_round is not None:
            logger.info('[AtLog] ----- Input Maximum Rebate Points per Round of rebate instance')
            self.click_element_via_xpath(self.em.bo_rebate_instances_create_instance_maximum_rebate_points_per_round_button_xpath)
            logger.info('[AtLog] ----- Input Max Bet Contribution')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_instances_dialog_key_xpath,
                                               'default')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_instances_dialog_value_xpath,
                                               max_rebate_points_per_round)
            self.click_element_via_xpath(self.em.bo_rebate_instances_dialog_update_button_xpath)

        if rebate_payout_settings == 'instant':
            logger.info('[AtLog] ----- tick checkbox of Instant Rebate to Rebate Point balance of rebate instance')
            self.click_element_via_xpath(self.em.bo_rebate_instances_create_instance_instant_rebate_to_rebate_point_balance_checkbox_xpath)
        elif rebate_payout_settings == 'completion':
            logger.info('[AtLog] ----- tick checkbox of Pay After Completion rebate instance')
            self.click_element_via_xpath(
                self.em.bo_rebate_instances_create_instance_pay_after_completion_checkbox_xpath)
        else:
            logger.error('[AtLog] ----- Setting type just has Instant Rebate to Rebate Point balance and Pay After Completion ')
            return False
        logger.info('[AtLog] ----- Click Create new rebate instance button')
        self.click_element_via_xpath(
            self.em.bo_rebate_instances_create_instance_button_xpath)

        logger.info('[AtLog] ----- Check whether in the Modify rebate instance page')
        if self.is_page_shown_via_xpath_expected_text(self.em.bo_rebate_instances_modify_rebate_instance_header_xpath,
                                                self.em.bo_rebate_instances_modify_rebate_instance_header_text) is True:
            if rule_rebate_category is not None or rule_game_provider is not None or rule_game is not None or rule_game_category is not None:
                logger.info('[AtLog] ----- Click Rule tab in the Modify rebate instance page')
                self.click_element_via_xpath(self.em.bo_rebate_instances_modify_rebate_instance_rule_tab_xpath)
                if rule_rebate_category is not None:
                    logger.info('[AtLog] ----- Add Rule of rebate category in the Modify rebate instance page')
                    self.select_dropdown_menu_element_via_locator_text(self.em.bo_rebate_instances_modify_rebate_instance_rebate_category_select_xpath, rule_rebate_category)
                    self.click_element_via_css(self.em.bo_rebate_instances_modify_rebate_instance_add_rebate_category_button_css)
                if rule_game_provider is not None:
                    logger.info('[AtLog] ----- Add Rule of game provider in the Modify rebate instance page')
                    self.select_dropdown_menu_element_via_locator_text(
                        self.em.bo_rebate_instances_modify_rebate_instance_game_provider_select_xpath,
                        rule_game_provider)
                    self.click_element_via_css(
                        self.em.bo_rebate_instances_modify_rebate_instance_add_game_provider_button_css)
                if rule_game is not None:
                    logger.info('[AtLog] ----- Add Rule of game in the Modify rebate instance page')
                    self.type_text_in_field_via_xpath(self.em.bo_rebate_instances_modify_rebate_instance_game_textarea_xpath, rule_game)
                    self.click_element_via_css(
                        self.em.bo_rebate_instances_modify_rebate_instance_add_game_button_css)
                if rule_game_category is not None:
                    logger.info('[AtLog] ----- Add Rule of game category in the Modify rebate instance page')
                    self.select_dropdown_menu_element_via_locator_text(
                        self.em.bo_rebate_instances_modify_rebate_instance_game_category_select_xpath,
                        rule_game_category)
                    self.click_element_via_css(
                        self.em.bo_rebate_instances_modify_rebate_instance_add_game_category_button_css)
            logger.info('[AtLog] ----- Try to Activate the rebate instance')
            logger.info('[AtLog] ----- Click Details tab in the Modify rebate instance page')
            self.click_element_via_css(self.em.bo_rebate_instances_modify_rebate_instance_details_tab_css)
            logger.info('[AtLog] ----- Activate the rebate instance')
            self.click_element_via_xpath(self.em.bo_rebate_instances_modify_rebate_instance_activate_button_xpath)
        else:
            logger.error('[AtLog] ----- It does not redirect to Modify rebate instance page')
            return False
        logger.info('[AtLog] ----- Check the rebate instance is Active')
        result = self.is_page_shown_via_xpath_expected_text(self.em.bo_rebate_instances_modify_rebate_instance_added_rule_text_xpath, self.em.bo_rebate_instances_modify_rebate_instance_added_rule_successfully_text)
        if result is True:
            logger.info('[AtLog] ----- The rebate instance is Active')
            return True
        else:
            logger.error('[AtLog] ----- The rebate instance is NOT Active')
            return False

    def bo_access_rebate_categories(self):
        """
        @precondition: the player is logged in on bo.

        :return: whether access rebate categories successfully

        """
        if self.is_find_element_via_css(self.em.bo_menu_rebate_categories_css) is False:
            logger.info('[AtLog] ----- expand the Rebate menu')
            self.expand_menu_via_css_from_list(self.em.bo_menu_rebate_expand_icon_css, index=3)
        logger.info('[AtLog] ----- Click the Rebate Category')
        self.click_link_via_css(self.em.bo_menu_rebate_categories_css)
        logger.info('[AtLog] ----- Check whether in the Rebate Category')
        return self.is_page_shown_via_xpath_expected_text(self.em.bo_rebate_categories_header_xpath, self.em.bo_rebate_categories_header_text)

    def bo_access_rebate_games(self):
        """
        @precondition: the player is logged in on bo.

        :return: whether access rebate games successfully

        """
        if self.is_find_element_via_css(self.em.bo_menu_rebate_categories_css) is False:
            logger.info('[AtLog] ----- expand the Rebate menu')
            self.expand_menu_via_css_from_list(self.em.bo_menu_rebate_expand_icon_css, index=3)
        logger.info('[AtLog] ----- Click the Rebate game')
        self.click_link_via_css(self.em.bo_menu_rebate_games_css)
        logger.info('[AtLog] ----- Check whether in the Rebate Category')
        return self.is_page_shown_via_xpath_text(self.em.bo_rebate_games_header_xpath,
                                              self.em.bo_rebate_games_header_text)

    def bo_search_rebate_game(self, game_id=rm.REBATE_GAME_ID):
        """
        @precondition: the player is logged in on bo.

        :param: game_id
        :return: whether searched rebate game successfully

        """
        logger.info('[AtLog] ----- Check whether in the Rebate Category')
        if self.is_page_shown_via_xpath_text(self.em.bo_rebate_games_header_xpath,
                                         self.em.bo_rebate_games_header_text) is False:
            self.bo_access_rebate_games()
        logger.info('[AtLog] ----- Input game id')
        self.clear_text_from_field_via_xpath(self.em.bo_rebate_games_game_id_field_xpath)
        self.type_text_in_field_via_xpath(self.em.bo_rebate_games_game_id_field_xpath, game_id)
        logger.info('[AtLog] ----- Click search button')
        self.click_link_via_xpath(self.em.bo_rebate_games_search_button_xpath)
        self.waits(2)
        logger.info('[AtLog] ----- Check whether the Rebate game show')
        return self.is_page_shown_via_xpath_expected_text(self.em.bo_rebate_games_searched_item_game_id_column_xpath, game_id)

    def bo_get_rebate_category_name_from_first_row(self):
        """
        @precondition: the player is logged in on bo. There is rebate category has been created.

        :return: rebate category name from first row.

        """
        logger.info('[AtLog] ----- Check whether in the Rebate Categories')
        if self.is_page_shown_via_xpath_expected_text(self.em.bo_rebate_categories_header_xpath,
                                          self.em.bo_rebate_categories_header_text) is False:
            logger.info('[AtLog] ----- Start to access Rebate Categories')
            self.bo_access_rebate_categories()
        else:
            logger.info('[AtLog] ----- It is in Rebate Categories')
            pass
        logger.info('[AtLog] ----- get the name from rebate category first row')
        return self.get_text_via_xpath(self.em.bo_rebate_latest_rebate_category_name_item_xpath)

    def bo_select_rebate_category(self, rebate_category_name, game_id=rm.REBATE_GAME_ID):
        """
        @precondition: the player is logged in on bo.

        :param: game_id
        :return: whether add rebate game to category successfully

        """
        logger.info('[AtLog] ----- Check whether the Rebate game show')
        if self.is_page_shown_via_xpath_expected_text(self.em.bo_rebate_games_searched_item_game_id_column_xpath, game_id) is False:
            self.bo_search_rebate_game(game_id)
        logger.info('[AtLog] ----- Select Rebate Category for the rebate game')
        self.select_dropdown_menu_element_via_locator_text(self.em.bo_rebate_games_searched_item_rebate_category_column_select_xpath, rebate_category_name)
        logger.info('[AtLog] ----- Search the rebate game and check whether in the game category')
        self.bo_search_rebate_game(game_id)
        logger.info('[AtLog] ----- Check whether the Rebate game is added the game category')
        option_text = self.get_current_selected_option_text(
            self.em.bo_rebate_games_searched_item_rebate_category_column_select_xpath)
        logger.info('[AtLog] ----- Current game category is [' + str(option_text) + '] -----')
        if option_text == rebate_category_name:
            return True
        else:
            return False

    def bo_access_create_rebate_category(self):
        """
        @precondition: the player is logged in on bo.

        :return: whether access create rebate category successfully

        """
        logger.info('[AtLog] ----- Check whether in the Rebate Categories')
        if self.is_page_shown_via_xpath_expected_text(self.em.bo_rebate_categories_header_xpath, self.em.bo_rebate_categories_header_text) is False:
            logger.info('[AtLog] ----- Start to access Rebate Categories')
            self.bo_access_rebate_categories()
        else:
            logger.info('[AtLog] ----- It is in Rebate Categories')
            pass
        logger.info('[AtLog] ----- Click create new rebate category')
        self.click_element_via_css(self.em.bo_rebate_create_new_rebate_category_css)
        logger.info('[AtLog] ----- Check whether in create new rebate category')
        return self.is_page_shown_via_xpath_expected_text(self.em.bo_rebate_create_new_category_header_xpath, self.em.bo_rebate_create_new_category_header_text)

    def bo_create_rebate_category(self, rebate_category_name=rm.REBATE_CATEGORY_NAME, cash_rebate_factor=rm.REBATE_CATEGORY_CASH_REBATE_FACTOR, slug=rm.REBATE_CATEGORY_SLUG):
        """
        @precondition: the player is logged in on bo.

        :return: whether create rebate category successfully

        """
        if self.is_page_shown_via_xpath_expected_text(self.em.bo_rebate_create_new_category_header_xpath,
                                               self.em.bo_rebate_create_new_category_header_text) is True:
            logger.info('[AtLog] ----- Accessed create new category page')
            pass
        else:
            logger.info('[AtLog] ----- Start to access rebate new category page')
            self.bo_access_create_rebate_category()
        logger.info('[AtLog] ----- Input name of rebate category')
        self.type_text_in_field_via_xpath(self.em.bo_rebate_create_new_rebate_category_name_xpath, rebate_category_name)
        if slug != '':
            logger.info('[AtLog] ----- Input slug of rebate category')
            self.type_text_in_field_via_xpath(self.em.bo_rebate_create_new_rebate_category_slug_xpath, slug)
        logger.info('[AtLog] ----- Input Cash Rebate Factor of rebate category')
        self.type_text_in_field_via_xpath(self.em.bo_rebate_create_new_rebate_category_cash_rebate_factor_xpath, cash_rebate_factor)
        logger.info('[AtLog] ----- Click create button in rebate category')
        self.click_element_via_xpath(self.em.bo_rebate_create_new_rebate_category_button_xpath)
        logger.info('[AtLog] ----- Check create rebate category whether successfully')
        result1 = self.is_find_element_via_css(self.em.bo_rebate_create_new_rebate_category_successful_css)
        if result1 is True:
            logger.info('[AtLog] ----- Click REBATE CATEGORIES link')
            self.click_element_via_css(self.em.bo_rebate_rebate_categories_link_css)
            logger.info('[AtLog] ----- Check the new category whether shows on rebate categories page')
            result2 = self.is_page_shown_via_xpath_expected_text(self.em.bo_rebate_latest_rebate_category_name_item_xpath, rebate_category_name)
            return result2
        else:
            return False

    def bo_access_helpdesk(self):
        """
        @precondition: the player is logged in on bo.

        :return: whether access helpdesk successfully

        """
        logger.info('[AtLog] ----- Click the Helpdesk link')
        self.click_link_via_css(self.em.bo_helpdesk_link_css)
        logger.info('[AtLog] ----- Check whether on HelpDesk page')
        result = self.is_find_link_via_css(self.em.bo_search_button_css)
        return result

    def bo_access_dashboard(self):
        """
        @precondition: the player is logged in on bo.

        :return: whether access dashboard successfully

        """
        logger.info('[AtLog] ----- Click the Dashboard link')
        self.click_link_via_css(self.em.bo_dashboard_link_css)
        logger.info('[AtLog] ----- Check whether on Dashboard page')
        bo_dashboard_view_all_link = self.em.bo_dashboard_view_all_link_prefix_css + str(
            self.rm.BO_SITE_ID) + self.em.bo_dashboard_view_all_link_suffix_css
        result = self.is_find_link_via_css(bo_dashboard_view_all_link)
        return result

    def bo_access_business_overview(self):
        """
        @precondition: the player is logged in on bo.

        :return: whether access business overview successfully

        """
        logger.info('[AtLog] ----- expand report menu')
        self.expand_menu_via_css(self.em.bo_menu_reports_css)
        logger.info('[AtLog] ----- Click the business overview link')
        self.click_element_via_css(self.em.bo_business_overview_link_css)
        logger.info('[AtLog] ----- Check whether on business overview page')
        result = self.is_find_link_via_xpath(self.em.bo_site_select_on_report_business_overview_xpath)
        return result

    def bo_access_alarms(self):
        """
        access alarms page

        @precondition: the player is logged in on bo.

        :return: whether access Alarms successfully

        """
        logger.info('[AtLog] ----- Click Alarms link')
        self.click_link_via_css(self.em.bo_menu_alarms_css)
        logger.info('[AtLog] ----- Check whether on Alarms')
        return self.is_page_shown_via_xpath_text(self.em.bo_alarms_search_alarms_button_xpath,
                                   self.em.bo_alarms_search_alarms_button_text)

    def bo_access_blacklist_overview(self):
        """
        access blacklist overview

        @precondition: the player is logged in on bo.

        :return: whether access Blacklist successfully

        """
        logger.info('[AtLog] ----- Click Blacklist link')
        self.click_link_via_css(self.em.bo_menu_blacklist_css)
        logger.info('[AtLog] ----- Check whether on Blacklist')
        return self.is_find_link_via_css(self.em.bo_blacklist_select_type_css)

    def bo_blacklist_add_black_country(self, country_abbreviation=rm.COUNTRY_ABB):
        """
        add black country

        @precondition: the player is logged in on bo.

        :param: Country abbreviation, e.g. AUT, DEU, USA
        :return: whether added black country successfully

        """
        logger.info('[AtLog] ----- Check the Country whether is added')
        if self.is_text_in_elements(str(country_abbreviation)) is True:
            logger.info('[AtLog] ----- the Country was added to blacklist')
            return True
        else:
            logger.info('[AtLog] ----- Select the type of country on Blacklist')
            self.select_dropdown_menu_element_via_locator_value(self.em.bo_blacklist_select_type_css,
                                        self.em.bo_blacklist_select_type_value_country)
            logger.info('[AtLog] ----- Select Country in blacklist')
            self.select_dropdown_menu_element_via_locator_value(self.em.bo_blacklist_select_country_css, str(country_abbreviation))
            logger.info('[AtLog] ----- Click Add button')
            self.click_element_via_xpath(self.em.bo_blacklist_add_button_xpath)
            self.waits(2)
            logger.info('[AtLog] ----- Check whether Add successfully')
            latest_item_text = self.get_text_via_xpath(self.em.bo_blacklist_first_row_value_xpath)
            return self.is_added_item(latest_item_text, str(country_abbreviation))

    def bo_blacklist_remove_latest_included_item(self):
        """
        remove latest included item

        @precondition: the player is logged in on bo.

        :return: whether removed latest item successfully

        """
        logger.info('[AtLog] ----- Check the whether has item in blacklist')
        if self.is_find_link_via_xpath(self.em.bo_blacklist_first_row_remove_button_xpath) is True:
            logger.info('[AtLog] ----- get the latest included item from blacklist')
            latest_item_text = self.get_text_via_xpath(self.em.bo_blacklist_first_row_value_xpath)
            logger.info('[AtLog] ----- remove the latest included item from blacklist')
            self.click_element_via_xpath(self.em.bo_blacklist_first_row_remove_button_xpath)
            self.waits(2)
            logger.info('[AtLog] ----- Check whether removed the latest included item from blacklist')
            if self.is_removed_latest_item(self.em.bo_blacklist_first_row_value_xpath,
                                                    str(latest_item_text)) is True:
                logger.info('[AtLog] ----- removed the latest included item from blacklist')
                return True
            else:
                logger.info('[AtLog] ----- removed failed')
                return False
        else:
            logger.info('[AtLog] ----- There is nothing in the blacklist')
            return True

    def bo_access_billfold_configuration(self):
        """
        @precondition: the player is logged in on bo.

        :return: whether access billfold configuration successfully

        """
        logger.info('[AtLog] ----- expand configuration menu')
        self.expand_menu_via_css(self.em.bo_menu_configuration_css)
        logger.info('[AtLog] ----- Click the billfold configuration link')
        self.click_element_via_css(self.em.bo_billfold_configuration_link_css)
        logger.info('[AtLog] ----- Check whether on billfold configuration page')
        result = self.is_page_shown_via_xpath_text(self.em.bo_billfold_configuration_header_xpath,
                                                     self.em.bo_billfold_configuration_header_text)
        return result

    def bo_access_payment_search(self):
        """
        @precondition: the player is logged in on bo.

        :return: whether access payment search successfully

        """
        logger.info('[AtLog] ----- expand payments menu')
        self.expand_menu_via_css(self.em.bo_menu_payment_css)
        logger.info('[AtLog] ----- Click the Payment Search link')
        self.click_link_via_css(self.em.bo_payment_search_link_css)
        logger.info('[AtLog] ----- Check whether on Payment Search page')
        result = self.is_page_shown_via_xpath_text(self.em.bo_payment_search_header_xpath,
                                             self.em.bo_payment_search_header_text)
        return result

    def bo_search_payment(self, reference="", payment_id="", user_id="", flag=0):
        """
        @precondition: the player is logged in on bo.
        This is search payment from bo.

        :param reference:
        :param payment_id:
        :param user_id:
        :param flag: 0: input the search text and click enter in keyboard,
        1:input the search text, then click search button
        :return: whether search player successfully

        """
        if flag == 0:
            logger.info(
                '[AtLog] ----- input search text and press Enter button on keyboard'
            )
            logger.info('[AtLog] ----- input search text of Reference')
            self.type_text_in_field_via_xpath(self.em.bo_payment_reference_field_xpath, reference)
            logger.info('[AtLog] ----- input search text of Payment Id')
            self.type_text_in_field_via_xpath(self.em.bo_payment_payment_id_field_xpath, payment_id)
            logger.info('[AtLog] ----- input search text of User Id and search')
            self.type_text_via_xpath_and_enter(self.em.bo_payment_user_id_field_xpath, user_id)
            self.waits(3)
        elif flag == 1:
            logger.info('[AtLog] ----- input search text of Reference')
            self.type_text_in_field_via_css(self.em.bo_payment_user_id_field_css,
                                          user_id)
            logger.info('[AtLog] ----- input search text of Payment Id')
            self.type_text_in_field_via_css(self.em.bo_payment_user_id_field_css,
                                          user_id)
            logger.info('[AtLog] ----- input search text of User Id')
            self.type_text_in_field_via_css(self.em.bo_payment_user_id_field_css,
                                          user_id)
            logger.info('[AtLog] ----- click search button')
            self.click_link_via_xpath(self.em.bo_payment_search_button_xpath)
            self.waits(3)
        if reference is not "":
            logger.info('[AtLog] ----- check searched result by reference')
            return self.is_page_shown_via_xpath_text(self.em.bo_payment_table_first_row_reference_item, reference)
        elif payment_id is not "":
            logger.info('[AtLog] ----- check searched result by payment_id')
            return self.is_page_shown_via_xpath_text(self.em.bo_payment_table_first_row_payment_id_item, payment_id)
        elif user_id is not "":
            logger.info('[AtLog] ----- check searched result by user_id')
            return self.is_page_shown_via_xpath_text(self.em.bo_payment_table_first_row_user_id_item, user_id)
        return False

    def bo_access_game_transaction(self):
        """
        @precondition: the player is logged in on bo.

        :return: whether access game transaction successfully

        """
        logger.info('[AtLog] ----- expand Game Transactions menu')
        self.expand_menu_via_css(self.em.bo_menu_game_transaction_css)
        logger.info('[AtLog] ----- Click the Game Transactions Search link')
        self.click_link_via_css(self.em.bo_game_transaction_link_css)
        logger.info('[AtLog] ----- Check whether on Payment Search page')
        result = self.is_page_shown_via_xpath_text(self.em.bo_game_transaction_search_header_xpath,
                                               self.em.bo_game_transaction_header_text)
        return result

    def bo_search_game_transaction(self, round_id=rm.GAME_ROUND_ID, start_time=rm.GAME_TRANSACTION_START,
                                   to_time=rm.GAME_TRANSACTION_TO):
        """
        @precondition: the player is logged in on bo.
        This is search payment from bo.

        :param round_id: game round id
        :param start_time: the time of game transactions start
        :param to_time: the time of game transactions to
        :return: whether search game transaction successfully

        """
        logger.info(
            '[AtLog] ----- input search text and press Enter button on keyboard'
        )
        logger.info('[AtLog] ----- input search text of Date From')
        self.clear_text_from_field_via_xpath(self.em.bo_game_transaction_from_xpath)
        self.type_text_in_field_via_xpath(self.em.bo_game_transaction_from_xpath, start_time)
        logger.info('[AtLog] ----- input search text of Date To')
        self.clear_text_from_field_via_xpath(self.em.bo_game_transaction_to_xpath)
        self.type_text_in_field_via_xpath(self.em.bo_game_transaction_to_xpath, to_time)
        logger.info('[AtLog] ----- input search text of Round Id and search')
        self.type_text_via_xpath_and_enter(self.em.bo_game_transaction_round_id_field_xpath, round_id)
        self.waits(3)
        logger.info('[AtLog] ----- check searched result')
        return self.is_page_shown_via_xpath_text(self.em.bo_game_transaction_table_first_row_round_id_item_live, round_id)

    def bo_create_campaign(self, campaign_type=rm.CAMPAIGN_PLAYER_CAMPAIGN, free_spin=None, promo=None, cash=None,
                           translation=False, promo_code_details='', free_spin_provider=''):
        """
        @precondition: the player is logged in on bo.

        :param campaign_type: deposit_code, deposit_all, n_deposit, registration_code, registration_all, player_campaign, player_campaign_with_code, n_deposit_with_code
        :param free_spin: Free spin amount, it is a list, [reword type, free spin amount], reward type includes 'direct' or 'voucher' e.g. ['voucher', '5']
        :param promo: it is a list, [reword type, promo amount], reward type includes 'direct' or 'voucher'. e.g. ['voucher', '5'], reword type is vouerh, promo amount is 5.
        :param cash: cash amount, it is a list, [reword type, cash amount], reward type includes 'direct' or 'voucher' e.g. ['voucher', '5']
        :param translation: True or False
        :param promo_code_details: promo_code, the details is promo_code_666
        :param free_spin_provider: netent, playngo, etc..

        :return: Campaign id, if compaign id is not 0, the campaign is create successfully.

        """
        comapaign_id = '0'

        if promo is None:
            promo = ['none', '0']
        if cash is None:
            cash = ['none', '0']
        if free_spin is None:
            free_spin = ['none', '0']

        logger.info('[AtLog] ----- Expand Campaigns menu')
        self.expand_menu_via_css_from_list(self.em.bo_menu_campaigns_expand_icon_css, index=1)
        logger.info('[AtLog] ----- Open create new campaign page')
        self.click_link_via_css(self.em.bo_menu_campaigns_create_new_campaign_css)
        self.waits(2)

        if promo[1] is not '0':
            logger.info('[AtLog] ----- Click Promo tab')
            self.click_element_via_xpath(self.em.bo_campaign_promo_tab_xpath)
            logger.info('[AtLog] ----- Check reward type of campaign')
            promo_amount = promo[1]
            reward_type = promo[0]
            if reward_type is 'voucher':
                logger.info('[AtLog] ----- this is voucher campaign')
                self.click_element_via_xpath(self.em.bo_campaign_promo_bonus_in_voucher_checkbox_xpath)
            elif reward_type is 'direct':
                logger.info('[AtLog] ----- this is direct campaign')
                pass
            else:
                logger.error('[AtLog] ----- No this reward_type')
                assert False
            logger.info('[AtLog] ----- Input promo Amount')
            self.type_text_in_field_via_xpath(self.em.bo_campaign_promo_tab_promo_amount_xpath, promo_amount)

        if cash[1] is not '0':
            logger.info('[AtLog] ----- Click cash tab')
            self.click_element_via_xpath(self.em.bo_campaign_cash_tab_xpath)
            logger.info('[AtLog] ----- Check reward type of campaign')
            cash_amount = cash[1]
            reward_type = cash[0]
            if reward_type is 'voucher':
                logger.info('[AtLog] ----- this is voucher campaign')
                self.tick_checkbox_in_campaign_via_xpath(self.em.bo_campaign_cash_bonus_in_voucher_checkbox_xpath)
            elif reward_type is 'direct':
                logger.info('[AtLog] ----- this is direct campaign')
                pass
            else:
                logger.error('[AtLog] ----- No this reward_type')
                assert False
            logger.info('[AtLog] ----- Input cash Amount')
            self.type_text_in_field_via_xpath(self.em.bo_campaign_cash_tab_cash_amount_xpath, cash_amount)

        if translation is True:
            logger.info('[AtLog] ----- Input translation')
            translation_text = self.rm.CAMPAIGN_TRANSLATION + self.rm.CAMPAIGN_NAME
            self.type_text_in_field_via_xpath(self.em.bo_campaign_translation_field_xpath, translation_text)

        if campaign_type == self.em.bo_campaign_select_player_campaign_value:
            logger.info('[AtLog] ----- select campaign type')
            self.select_dropdown_menu_element_via_locator_value(self.em.bo_campaign_campaign_type_select_xpath,
                                                           self.em.bo_campaign_select_player_campaign_value)
            logger.info('[AtLog] ----- Input campaign name')
            self.type_text_in_field_via_xpath(self.em.bo_campaign_name_field_xpath, self.rm.CAMPAIGN_NAME)
            logger.info('[AtLog] ----- Input Turnover Factor')
            self.type_text_in_field_via_xpath(self.em.bo_campaign_turnover_factor_field_xpath,
                                                 self.rm.TURNOVER_FACTOR_TIMES)
            logger.info('[AtLog] ----- Input campaign end time')
            self.type_text_in_field_via_xpath(self.em.bo_campaign_end_time_field_xpath, self.rm.CAMPAIGN_END_TIME)
            logger.info('[AtLog] ----- Select user from list')
            self.select_dropdown_menu_element_via_locator_text(self.em.bo_campaign_users_select_xpath,
                                                          self.em.bo_campaign_users_select_user_from_list_text)
            logger.info('[AtLog] ----- input user id on the field')
            self.type_text_in_field_via_xpath(self.em.bo_campaign_users_user_id_list_textarea_xpath, self.rm.USERID)
        else:
            logger.error('[AtLog] ----- There is no this campaign type')
            assert False

        logger.info('[AtLog] ----- scroll to the button of "create new campaign"')
        self.scroll_browser_to_target_via_xpath(self.em.bo_campaign_create_new_campaign_button_xpath)
        logger.info('[AtLog] ----- Click the button of "create new campaign"')
        self.click_element_via_xpath(self.em.bo_campaign_create_new_campaign_button_xpath)
        logger.info('[AtLog] ----- whether "create new campaign" successful ')
        self.waits(3)
        if self.is_find_element_via_css(self.em.bo_campaign_create_successful_css):
            logger.info('[AtLog] ----- get campaign id')
            comapaign_id = self.get_text_via_xpath(self.em.bo_campaign_new_campaign_created_id_xpath)
            logger.info('[AtLog] ----- create campaign successful')
        else:
            logger.error('[AtLog] ----- create campaign failed')
            assert False
        return comapaign_id

    def bo_access_player_information_from_link(self, user_id=rm.USERID):
        """
        @precondition: the player is logged in bo.

        :return: whether access Player Information successfully

        """
        logger.info('[AtLog] ----- Go to player information page')
        site_address = str(self.rm.BO_ADDRESS_ROOT) + str(self.em.bo_player_information_link_suffix) + str(user_id)
        self.access_web_url(site_address)
        if self.is_page_shown_via_xpath_expected_text(self.em.bo_player_information_header_xpath,
                                           self.em.bo_player_information_header_text) is True:
            logger.info('[AtLog] ----- Accessed player information page')
            return True
        else:
            logger.error('[AtLog] ----- Access player information page failed')
            return False

    def bo_access_campaign_information_from_link(self, campaign_id):
        """
        @precondition: the player is logged in BO.

        :return: whether access campaign Information successfully

        """
        logger.info('[AtLog] ----- Go to campaign information page')
        site_address = str(self.rm.BO_ADDRESS_ROOT) + str(self.em.bo_campaign_information_link_suffix) + str(
            campaign_id)
        self.access_web_url(site_address)
        if self.is_page_shown_via_xpath_expected_text(self.em.bo_campaign_information_header_xpath,
                                             self.em.bo_campaign_information_header_text) is True:
            logger.info('[AtLog] ----- Accessed campaign information page')
            return True
        else:
            logger.error('[AtLog] ----- Access campaign information page failed')
            return False

    def bo_cancel_campaign(self, campaign_id):
        """
        @precondition: the player is logged in bo.

        :return: whether cancel campaign successfully by campaign id.

        """
        if self.is_page_shown_via_xpath_expected_text(self.em.bo_campaign_information_header_xpath,
                                             self.em.bo_campaign_information_header_text) is True:
            logger.info('[AtLog] ----- It is in campaign information page')
            pass
        else:
            logger.info('[AtLog] ----- Start to access campaign information page')
            self.bo_access_campaign_information_from_link(campaign_id)
        logger.info('[AtLog] ----- select the drop down menu and cancel the campaign')
        self.select_dropdown_menu_element_via_locator_value(self.em.bo_campaign_information_status_xpath,
                                                       self.em.bo_campaign_information_status_selector_active_value)
        logger.info('[AtLog] ----- update the campaign status')
        self.click_element_in_list_by_index_via_css(self.em.bo_campaign_information_update_button, index=0)
        self.waits(2)

    def bo_claim_latest_voucher_for_player(self, user_id=rm.USERID):
        """
        @precondition: the player is logged in bo.

        :return: whether claim the voucher successfully.

        """
        if self.is_page_shown_via_xpath_expected_text(self.em.bo_player_information_header_xpath,
                                           self.em.bo_player_information_header_text) is True:
            logger.info('[AtLog] ----- Accessed player information page')
        else:
            logger.info('[AtLog] ----- Start to access player information page')
            self.bo_access_player_information_from_link(user_id)
        logger.info('[AtLog] ----- Click the link of vouchers on player information page')
        self.click_element_via_xpath(self.em.bo_player_information_vouchers_xpath)
        logger.info('[AtLog] ----- Click latest voucher id on player vouchers page')
        self.click_element_via_xpath(self.em.bo_voucher_item_voucher_id_xpath)
        logger.info('[AtLog] ----- Click Claim button on Voucher page')
        self.click_element_via_xpath(self.em.bo_voucher_claim_voucher_button_xpath)
        self.waits(2)
        if self.is_find_element_via_css(self.em.bo_voucher_claim_successful_css):
            logger.info('[AtLog] ----- Voucher claim started.')
            return True
        else:
            logger.error('[AtLog] ----- Voucher claim failed')
            return False

    '''
    ----------BO--lV_3 api ---------
    '''

    def bo_get_promo_balance_from_player_information(self):
        """
        @precondition: bo_access_player_information_from_link(),
        the player is logged in on bo. and access the Player Information.

        :return: the amount of promo balance

        """
        logger.info('[AtLog] ----- Get promo balance from player information page')
        self.click_element_via_xpath(self.em.bo_player_information_balance_tab_xpath)
        return self.get_value_via_xpath(self.em.bo_player_information_balance_tab_promo_balance_xpath)

    def bo_get_cash_balance_from_player_information(self):
        """
        @precondition: the player is logged in on bo. and access the Player Information.

        :return: the amount of cash balance

        """
        self.click_element_via_xpath(self.em.bo_player_information_balance_tab_xpath)
        return self.get_value_via_xpath(self.em.bo_player_information_balance_tab_cash_balance_xpath)
