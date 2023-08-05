"""
Created on Aug 17, 2021

@author: Siro

"""


class BoPaymentElementsMaps(object):
    bo_payment_search_link_css = "a[class='bo-nav__control'][href='paymentSearch!view']"
    bo_payment_search_header_xpath = "//*[@id='bo-page-payments-list']/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]"
    bo_payment_search_header_text = "Payment Search"

    bo_payment_reference_field_css = "input[type='text'][name='payment.reference'][id='paymentSearch_payment_reference']"
    bo_payment_payment_id_field_css = "input[type='text'][name='payment.paymentId'][id='paymentSearch_payment_paymentId']"
    bo_payment_user_id_field_css = "input[type='text'][name='payment.userId'][id='paymentSearch_payment_userId']"

    bo_payment_reference_field_xpath = "//*[@id='paymentSearch_payment_reference']"
    bo_payment_payment_id_field_xpath = "//*[@id='paymentSearch_payment_paymentId']"
    bo_payment_user_id_field_xpath = "//*[@id='paymentSearch_payment_userId']"

    bo_payment_search_button_xpath = "//*[@id='paymentSearch_0']"
    bo_payment_table_first_row_user_id_item = "//*[@id='payments']/tbody/tr[1]/td[12]/a"
    bo_payment_table_first_row_reference_item = "//*[@id='payments']/tbody/tr[1]/td[10]/a"
    bo_payment_table_first_row_payment_id_item = "//*[@id='payments']/tbody/tr[1]/td[9]/a"
