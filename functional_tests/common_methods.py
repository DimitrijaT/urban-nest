from functional_tests.template_classes.login import LoginPage


class CommonMethods:
    @staticmethod
    def login(browser, live_server_url):
        login_page = LoginPage(browser, live_server_url)
        login_page.navigate_to_login_page()
        login_page.assert_login_page_url()
        login_page.login('testuser', 'testpassword')
        login_page.assert_index_page_url()
        return browser, live_server_url
