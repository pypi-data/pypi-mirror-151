"""
Created on Mar 04, 2021

@author: Siro

"""

import os
import platform
import sys
from atframework.web.utils.utils import Utils


class ResourceMaps(object):
    utils = Utils()
    setupPropertiesPath = utils.get_setup_properties_path()
    setupInfo = utils.get_setup_info(setupPropertiesPath)
    documentImagePath = utils.get_document_image_path()

    '''
    site setup info
    '''
    RUNNING_SITE = setupInfo['site']

    if utils.site == "":
        running_site = RUNNING_SITE
    else:
        running_site = str(utils.site)

    '''
    set the current browser
    '''
    if utils.browser == "":
        BROWSER_NAME = setupInfo['browser']
    else:
        BROWSER_NAME = str(utils.browser)

    propertiesPath = os.path.abspath(os.path.dirname(os.getcwd(
    ))) + "/properties/" + running_site + "/integration.properties"
    dicProperties = utils.get_all_properties(propertiesPath)

    requestUrlPath = os.path.abspath(os.path.dirname(os.getcwd(
    ))) + "/properties/" + running_site + "/request.properties"
    requestProperties = utils.get_all_properties(requestUrlPath)

    '''
    set the current testing_type
    '''
    if utils.testing_type == "":
        TESTING_TYPE = setupInfo['testing_type']
    else:
        TESTING_TYPE = str(utils.testing_type)

    '''
    bo site id
    '''
    BO_SITE_ID = dicProperties['boSiteId']

    '''
    Add country in blacklist
    '''
    COUNTRY_ABB = dicProperties['blackCountry']

    '''
    Game round id
    '''
    GAME_ROUND_ID = dicProperties['gameRoundId']
    GAME_TRANSACTION_START = dicProperties['gameTransactionFrom']
    GAME_TRANSACTION_TO = dicProperties['gameTransactionTo']

    '''
    site protection info
    '''
    PROTECTION_USERNAME = dicProperties['protectionUsername']
    PROTECTION_PASSWORD = dicProperties['protectionPassword']

    '''
    the following are web site links
    '''

    SITE_ADDRESS = dicProperties['sitePortal']
    SITE_ADDRESS_EN = dicProperties['sitePortalEN']

    '''
    the following are BO links
    '''
    BO_ADDRESS_ROOT = dicProperties['boPortalRoot']
    BO_ADDRESS = dicProperties['boPortal']

    '''
    the following are BO Admin account info
    '''
    USERNAME_BO = dicProperties['usernameBo']
    PASSWORD_BO = dicProperties['passwordBo']

    '''
    the following test account info should be changed before testing
    '''
    TEST_EMAIL = utils.get_test_user_name() + "@test.com"
    TEST_EMAIL_PREFIX = utils.get_test_user_name_prefix()
    TEST_NICKNAME = utils.get_test_user_name()
    TEST_PASSWORD = dicProperties['testPasswrod']

    '''
    profile page
    '''
    STREET_NUMBER = dicProperties['streetNumber']
    HOUSE_NUMBER = dicProperties['houseNumber']
    DISTRICT = dicProperties['district']
    CITY = dicProperties['city']
    ZIP_CODE = dicProperties['zipCode']
    PHONE_NUMBER = utils.get_phone_number()
    BIRTH_DAY = dicProperties['birthday']
    BIRTH_MONTH = dicProperties['birthmonth']
    BIRTH_MONTH_ENGLISH = dicProperties['birthmonthEnglish']
    BIRTH_YEAR = dicProperties['birthyear']
    DOCUMENT_NAME = dicProperties['documentName']
    DOCUMENT_IMAGE_PATH = documentImagePath

    '''
    testing account
    '''
    USERID = dicProperties['userid']
    USER_EMAIL = dicProperties['userEmail']

    '''
    campaign page
    '''
    CAMPAIGN_NAME = utils.get_campaign_name()
    TURNOVER_FACTOR_TIMES = dicProperties['turnoverFactorTimes']
    FREE_SPIN_AMOUNT = dicProperties['freespinAmount']
    PROMO_AMOUNT = dicProperties['promoAmount']
    CASH_AMOUNT = dicProperties['cashAmount']
    CAMPAIGN_END_TIME = utils.get_campaign_end_time()
    MIN_DEPOSIT_AMOUNT = dicProperties['minDepositAmount']
    MAX_DEPOSIT_AMOUNT = dicProperties['maxDepositAmount']
    CAMPAIGN_TRANSLATION = dicProperties['campaignTranslation']
    PLAYNGO_GAME_ID = dicProperties['playngoGameId']

    '''
    campaign type
    '''
    # Campaign_type contain: deposit_code, deposit_all, n_deposit, registration_code,
    # registration_all, player_campaign, player_campaign_with_code, n_deposit_with_code,

    CAMPAIGN_REWORD_TYPE_DIRECT = 'direct'
    CAMPAIGN_REWORD_TYPE_VOUCHER = 'voucher'
    CAMPAIGN_DEPOSIT_CODE = "deposit_code"
    CAMPAIGN_DEPOSIT_ALL = "deposit_all"
    CAMPAIGN_N_DEPOSIT = "n_deposit"
    CAMPAIGN_REGISTATION_CODE = "registration_code"
    CAMPAIGN_REGISTATION_ALL = "registration_all"
    CAMPAIGN_PLAYER_CAMPAIGN = "player_campaign"
    CAMPAIGN_PLAYER_CAMPAIGN_WITH_CODE = "player_campaign_with_code"
    CAMPAIGN_N_DEPOSIT_WITH_CODE = "n_deposit_with_code"
    NO_CAMPAIGN = "no_campaign"

    PROVIDER_DEFAULT = "Default"
    PROVIDER_PLAYNGO = "Playngo"
    PROVIDER_YGGDRASIL = "Yggdrasil"
    PROVIDER_NETENT = "NetEnt"
    PROVIDER_ELK = "ELK"
    PROVIDER_THUNDERKICK = "Thunderkick"
    PROVIDER_QUICKSPIN = "Quickspin"
    PROVIDER_REDTIGER = "RedTiger"
    PROVIDER_ORYX = "Oryx"
    PROVIDER_PUSHGAMING = "Push Gaming"
    PROVIDER_RELEXGAMING = "Relax Gaming"

    '''
    Rebate
    '''
    REBATE_CATEGORY_NAME = utils.get_rebate_name()
    REBATE_CATEGORY_SLUG = dicProperties['rebateCategorySlug']
    REBATE_CATEGORY_CASH_REBATE_FACTOR = dicProperties['rebateCategoryFactor']
    REBATE_GAME_ID = dicProperties['rebateGameId']

    REBATE_TEMPLATE_NAME = utils.get_rebate_template_name()
    REBATE_TEMPLATE_DESCRIPTION = dicProperties['rebateTemplateDescription']
    REBATE_TEMPLATE_TITLE = dicProperties['rebateTemplateTitle']
    REBATE_TEMPLATE_SLUG = dicProperties['rebateTemplateSlug']
    REBATE_TEMPLATE_DURATION = dicProperties['rebateTemplateDuration']
    REBATE_TEMPLATE_NOTE = dicProperties['rebateTemplateNote']
    REBATE_TEMPLATE_TYPE = dicProperties['rebateTemplateType']
    REBATE_TEMPLATE_MULTIPLIER = dicProperties['rebateTemplateMultiplier']
    REBATE_TEMPLATE_MAX_NUMBER_OF_ROUND = dicProperties['rebateTemplateMaxNumberOfRound']
    REBATE_TEMPLATE_MAX_TOTAL_REBATE = dicProperties['rebateTemplateMaxTotalRebate']
    REBATE_TEMPLATE_MIN_BET_REQUIREMENT = dicProperties['rebateTemplateMinBetRequirement']
    REBATE_TEMPLATE_MAX_BET_CONTRIBUTION = dicProperties['rebateTemplateMaxBetContribution']
    REBATE_TEMPLATE_CAP_MAX_BET = dicProperties['rebateTemplateCapMaximumBet']
    REBATE_TEMPLATE_MAX_REBATE_POINTS_PER_ROUND = dicProperties['rebateTemplateMaximumRebatePointsPerRound']
    # value is instant or completion
    REBATE_TEMPLATE_PAYOUT_SETTINGS = dicProperties['rebateTemplatePayoutSettings']
    REBATE_TEMPLATE_RULE_REBATE_CATEGORY = dicProperties['rebateTemplateRuleRebateCategory']
    REBATE_TEMPLATE_RULE_GAME_PROVIDER = dicProperties['rebateTemplateRuleGameProvider']
    REBATE_TEMPLATE_RULE_GAME = dicProperties['rebateTemplateRuleGame']
    REBATE_TEMPLATE_RULE_GAME_CATEGORY = dicProperties['rebateTemplateRuleGameCategory']

    REBATE_INSTANCE_NAME = utils.get_rebate_instance_name()
    REBATE_INSTANCE_TYPE = dicProperties['rebateInstanceType']
    REBATE_INSTANCE_MULTIPLIER = dicProperties['rebateInstanceMultiplier']
    REBATE_INSTANCE_TITLE = dicProperties['rebateInstanceTitle']
    REBATE_INSTANCE_SLUG = dicProperties['rebateInstanceSlug']
    REBATE_INSTANCE_NOTE = dicProperties['rebateInstanceNote']
    REBATE_INSTANCE_END_TIME = utils.get_rebate_instance_end_time()
    REBATE_INSTANCE_DURATION = dicProperties['rebateInstanceDuration']
    REBATE_INSTANCE_USER_ID = dicProperties['rebateInstanceUserId']
    REBATE_INSTANCE_IS_EXCLUDE_USER = dicProperties['rebateInstanceIsExcludeUser']
    REBATE_INSTANCE_MAX_NUMBER_OF_ROUND = dicProperties['rebateInstanceMaxNumberOfRound']
    REBATE_INSTANCE_MAX_TOTAL_REBATE = dicProperties['rebateInstanceMaxTotalRebate']
    REBATE_INSTANCE_MIN_BET_REQUIREMENT = dicProperties['rebateInstanceMinBetRequirement']
    REBATE_INSTANCE_MAX_BET_CONTRIBUTION = dicProperties['rebateInstanceMaxBetContribution']
    REBATE_INSTANCE_CAP_MAX_BET = dicProperties['rebateInstanceCapMaximumBet']
    REBATE_INSTANCE_MAX_REBATE_POINTS_PER_ROUND = dicProperties['rebateInstanceMaximumRebatePointsPerRound']
    # value is instant or completion
    REBATE_INSTANCE_PAYOUT_SETTINGS = dicProperties['rebateInstancePayoutSettings']
    REBATE_INSTANCE_RULE_REBATE_CATEGORY = dicProperties['rebateInstanceRuleRebateCategory']
    REBATE_INSTANCE_RULE_GAME_PROVIDER = dicProperties['rebateInstanceRuleGameProvider']
    REBATE_INSTANCE_RULE_GAME = dicProperties['rebateInstanceRuleGame']
    REBATE_INSTANCE_RULE_GAME_CATEGORY = dicProperties['rebateInstanceRuleGameCategory']

    '''
    API request Urls
    '''
    SITE_PREFIX = requestProperties['sitePrefix']
    REGISTER_URL = requestProperties['registrationUrl']
    LOGIN_URL = requestProperties['loginUrl']
    FAMILY_FAVORITES_URL = requestProperties['familyFavoritesUrl']
    FAMILY_FAVORITES_SEARCH_TEXT = requestProperties['familyFavoriteSearchText']
    POSITIONING_GROUP_URL = requestProperties['positioningGroupUrl']
    POSITIONING_URL = requestProperties['positioningUrl']
    LOGOUT_URL = requestProperties['logoutUrl']
    FAMILY_GROUP_NAME = requestProperties['familyGroupName']
    POSITIONING_SEARCH_TEXT = requestProperties['positioningSearchText']
    POSITIONING_GROUP_SEARCH_TEXT = requestProperties['positioningGroupSearchText']


    TEST_USEREMAIL_FOR_API = requestProperties['testUserEmailForAPI']
    TEST_PASSWORD_FOR_API = requestProperties['testPasswordForAPI']
