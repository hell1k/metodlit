from pages.base_page import BasePage
from pages.common.header import Header


class ProfilePage(BasePage):
    
    def __init__(self):
        self.header = Header()
