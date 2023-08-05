"""
Created on Aug 18, 2021

@author: Siro

"""


class BoGameTransactionElementsMaps(object):
    bo_game_transaction_link_css = "a[class='bo-nav__control'][href='gameTransactions!view']"
    bo_game_transaction_search_header_xpath = "//*[@id='bo-page-games-transactions']/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]"
    bo_game_transaction_header_text = "Search transaction(s)"

    bo_game_transaction_round_id_field_css = "input[type='text'][name='gameRoundId'][id='gameTransactions_gameRoundId']"
    bo_game_transaction_round_id_field_xpath = "//*[@id='gameTransactions_gameRoundId']"
    bo_game_transaction_from_xpath = "//*[@id='gameTransactions_from']"
    bo_game_transaction_to_xpath = "//*[@id='gameTransactions_to']"

    bo_game_transaction_search_button_xpath = "//*[@id='gameTransactions_0']"
    bo_game_transaction_table_first_row_round_id_item_live = '//*[@id="transactionsLive"]/tbody/tr/td[14]/a'

