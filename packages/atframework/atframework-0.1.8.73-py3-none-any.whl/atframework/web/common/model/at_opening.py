"""
Created on Mar 03, 2021

@author: Siro

"""

from atframework.web.common.model.model import Model


class AtOpening(Model):
    def setup_browser(self, browser_name):
        return self._open_browser(browser_name)

    def max_browser(self):
        self._max_browser()

    def access_web_url(self, url):
        self._access_website(url)

    def access_web_url_till_one_time(self, site_name):
        self._access_website_till_one_time(site_name)

    def bring_to_front(self):
        self._bring_to_front()
