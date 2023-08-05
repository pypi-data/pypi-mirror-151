# -*- coding: utf-8 -*-
from selenium.webdriver.firefox.service import Service


class FService(Service):

    @property
    def service_url(self):
        """
        Gets the url of the Service
        """
        return f"http://127.0.0.1:{self.port}"
