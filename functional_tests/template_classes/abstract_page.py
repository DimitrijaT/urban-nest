class AbstractPage:

    def __init__(self, browser, live_server_url):
        self.browser = browser
        self.live_server_url = live_server_url
