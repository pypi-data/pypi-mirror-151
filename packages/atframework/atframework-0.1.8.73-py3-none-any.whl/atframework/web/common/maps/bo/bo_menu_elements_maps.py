"""
Created on Aug 12, 2021

@author: Siro

"""


class BoMenuElementsMaps(object):

    bo_menu_reports_css = "li[class='bo-nav__item bo-nav__item--report bo-nav__item--nested']"
    bo_menu_configuration_css = "li[class='bo-nav__item bo-nav__item--config bo-nav__item--nested']"
    bo_menu_blacklist_css = "a[class='bo-nav__control'][href='blacklist!view']"
    bo_menu_alarms_css = "a[class='bo-nav__control'][href='alarms!view?alarmStatus=open']"
    bo_menu_payment_css = "li[class='bo-nav__item bo-nav__item--payment bo-nav__item--nested']"
    bo_menu_game_transaction_css = "li[class='bo-nav__item bo-nav__item--games bo-nav__item--nested']"
    bo_menu_campaigns_css = "li[class='bo-nav__item bo-nav__item--campaigns bo-nav__item--nested']"
    bo_menu_campaigns_create_new_campaign_css = "a[class='bo-nav__control'][href='campaignCreate']"
    bo_menu_campaigns_expand_icon_css = 'i[class="bo-icon__elem fa fa-caret-down"]'
    bo_menu_rebate_expand_icon_css = 'i[class="bo-icon__elem fa fa-caret-down"]'
    bo_menu_rebate_categories_css = 'a[class="bo-nav__control"][href="rebateCategories!search"]'
    bo_menu_rebate_games_css = 'a[class="bo-nav__control"][href="rebateGames!search"]'
    bo_menu_rebate_templates_css = 'a[class="bo-nav__control"][href="rebateTemplates!search"]'
    bo_menu_rebate_instances_css = 'a[class="bo-nav__control"][href="rebateInstances!search?status=ACTIVE"]'
