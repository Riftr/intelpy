from mechanize import Browser
import webbrowser
from PyQt5.QtCore import *


class lookupExternal(QRunnable):
    def __init__(self, pilot):
        super(lookupExternal, self).__init__()
        self.br = Browser()
        self.pilot = pilot

    @pyqtSlot()
    def run(self):
        try:
            self.br.open("http://zkillboard.com/")
            self.br.select_form(name="search")
            self.br["searchbox"] = self.pilot
            response = self.br.submit()
            webbrowser.open_new_tab(response.geturl())
        except Exception as e:
            return str(e)
        return

    def evewho(self):
        # gives robot.txt error if you try to do it, 503 if you fake it. zkill works fine however.
        self.br.set_handle_equiv(False)
        self.br.set_handle_robots(False)
        self.br.addheaders = [
            ('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:18.0)Gecko/20100101 Firefox/18.0 (compatible;)'),
            ('Accept', '*/*')]
        self.br.open("https://evewho.com/")
        self.br.select_form(onsubmit="return false;")
        self.br["autocomplete"] = self.pilot
        response = self.br.submit()
        try:
            webbrowser.open_new_tab(response.geturl())
        except Exception as e:
            return str(e)
        return
