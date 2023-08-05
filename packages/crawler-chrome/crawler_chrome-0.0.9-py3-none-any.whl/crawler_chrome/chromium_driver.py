import os

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.webdriver import WebDriver

from crawler_chrome.base_driver import BaseDriver


class ChromiumDriver(BaseDriver, WebDriver):

    def __init__(self,
                 executable_path,
                 binary_location,
                 headless=True,
                 rec_log=False,
                 user_data_dir=None,
                 default_directory=None,
                 disable_images=False,
                 auto_tip_close=False,
                 no_sandbox=True,
                 proxy=None):
        self.udata = {}
        self.screenshot_list = []
        prefs = {}

        chrome_options = Options()
        chrome_options.binary_location = binary_location
        if auto_tip_close:
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option("useAutomationExtension", 'False')
        chrome_options.accept_insecure_certs = True
        if user_data_dir:
            chrome_options.add_argument(f"user-data-dir={user_data_dir}")
        if headless:
            chrome_options.add_argument("--headless")
        if no_sandbox:
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument('--hide-scrollbars')
        if rec_log:
            chrome_options.add_experimental_option('w3c', False)
        if proxy:
            chrome_options.add_argument(f"--proxy-server={proxy}")
        else:
            chrome_options.add_argument('--no-proxy-server')
        if default_directory:
            os.makedirs(default_directory, exist_ok=True)

            prefs.update({"profile.default_content_settings.popups": 0,
                          "download.default_directory": default_directory,
                          'safebrowsing.enabled': False,
                          'safebrowsing.disable_download_protection': True,
                          'download.prompt_for_download': False,
                          "directory_upgrade": True})
        if disable_images:
            prefs.update({"profile.managed_default_content_settings.images": 2})

        chrome_options.add_experimental_option('prefs', prefs)
        # super().__init__(executable_path=executable_path, desired_capabilities=d, options=chrome_options)
        super().__init__(executable_path=executable_path, options=chrome_options)
        self.set_window_position(0, 0)
        self.set_window_size(1200, 1000)
