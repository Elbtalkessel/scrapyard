import threading
import os
import tempfile
import sys
import shutil

from selenium import webdriver


class BrowserFactory:
    def __init__(self, proxies=None, useragents=None):
        self.lock = threading.Lock()
        self.proxies = proxies
        self.useragents = useragents

    def driver(self, thread_id):
        raise NotImplementedError

    def driver_dispatch(self, thread_id):
        self.lock.acquire()
        try:
            return self.driver(thread_id)
        except Exception as e:
            raise e
        finally:
            self.lock.release()

    def next(self, thread_id):
        return self.driver_dispatch(thread_id)

    def __next__(self):
        return self.driver_dispatch(0)


class ChromeFactory(BrowserFactory):
    def driver(self, thread_id) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-web-security')
        options.add_argument(f'--bot={thread_id}')
        options.set_capability('pageLoadStrategy', 'none')

        if self.proxies:
            proxy = next(self.proxies)
            options.add_argument(f'--proxy-server=socks5://{proxy.string}')
        if self.gen_user_agent:
            user_agent = next(self.gen_user_agent).strip()
            options.add_argument(f'user-agent={user_agent}')
        options.add_extension(os.path.join(
            settings.BASE_DIR, 'extensions', 'mimic', 'mimic.crx'
        ))
        caps = options.to_capabilities()

        browser = webdriver.Chrome(
            executable_path=shutil.which('chromedriver'),
            desired_capabilities=caps,
        )
        browser.maximize_window()
        return browser



def rmtree(directory):
    for d in os.listdir(directory):
        curdir = os.path.join(directory, d)
        try:
            rmtree(curdir)
        except OSError:
            try:
                os.remove(curdir)
            except (PermissionError, FileNotFoundError):
                pass


def cleanup_tempdir():
    """
    If selenium cannot close and quit browser it will leave temporary files in temp dir
    """
    if sys.platform == 'linux':
        dprefix = ('.com.google.Chrome.', 'rust_')
    else:
        dprefix = ('scoped_dir', 'rust_')
    tempdir = tempfile.gettempdir()
    junk = [os.path.join(tempdir, d) for d in os.listdir(tempdir) if d.startswith(dprefix)]
    for junk_dir in junk:
        rmtree(junk_dir)
