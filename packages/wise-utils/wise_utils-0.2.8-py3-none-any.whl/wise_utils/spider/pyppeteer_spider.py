# -*- coding: utf-8 -*-
import sys
import logging

from pyppeteer import launcher, launch

launcher.DEFAULT_ARGS.remove("--enable-automation")

from wise_utils.spider.basespider import BaseSpider


class PyppeteerBaseSpider(BaseSpider):
    def __init__(self, task_name, log_level=logging.DEBUG, log_file_path=None):
        super(PyppeteerBaseSpider, self).__init__(task_name=task_name, log_level=log_level, log_file_path=log_file_path)
        self.ignoreHTTPSErrors = True  # Whether to ignore HTTPS errors. Defaults to False.
        self.headless = True  # Whether to run browser in headless mode. Defaults to True unless appMode or devtools options is True.
        self.executable_path = ""  # Path to a Chromium or Chrome executable to run instead of default bundled Chromium.
        self.slow_mo = 0.1  # Slow down pyppeteer operations by the specified amount of milliseconds.
        self.devtools = False  # Whether to auto-open a DevTools panel for each tab. If this option is True, the headless option will be set False.
        self.autoClose = True  # Automatically close browser process when script completed. Defaults to True.

    async def create_browser(self):
        """
        初始化一个chrome
        """
        options_dict = {
            "headless": self.headless,
            "dumpio": True,
            # "devtools": self.devtools,
            'autoClose': self.autoClose,
            "timeout": 60000,
            "ignoreHTTPSErrors": True,  # 忽略证书错误
            "args": [
                # '--disable-gpu',  # 谷歌文档提到需要加上这个属性来规避bug
                "--allow-running-insecure-content",  # 允许不安全内容
                # "--disable-xss-auditor",  # 关闭 XSS Auditor
                '--no-sandbox',
                # '--disable-setuid-sandbox',
                '--disable-infobars',  # 关闭提示条
                # '--disable-extensions',
                # '--hide-scrollbars',  # 隐藏滚动条, 应对一些特殊页面
                # '--disable-bundled-ppapi-flash',
                # '--mute-audio',
                '--disable-dev-shm-usage'
            ],
        }

        if self.executable_path:
            # 指定chrome位置
            options_dict["executablePath"] = self.executable_path

        if sys.platform == "linux":
            # 打开虚拟窗口
            from pyvirtualdisplay import Display
            self.display = Display(visible=False, size=(1792, 1120))
            self.display.start()

        browser = await launch(options=options_dict)
        page = await browser.newPage()  # 启动个新的浏览器页面
        return browser, page

    async def init_page(self, page):
        await page.setUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3477.0 Safari/537.36")
        await page.evaluate('''() => {
    window.navigator.chrome = {
runtime: {},
// etc.
};
}'''
)
        await page.evaluate('''() =>{
Object.defineProperty(navigator, 'languages', {
  get: () => ['en-US', 'en']
});
    }'''

)
        await page.evaluate('''() =>{
Object.defineProperty(navigator, 'plugins', {
get: () => [1, 2, 3, 4, 5,6],
});
}''')
        await page.setViewport({"width": 1080, "height": 1080})
        return page

    async def close_browser(self, browser, page):
        try:
            await page.close()
            await browser.close()
            self.display.stop()
        except:
            pass
