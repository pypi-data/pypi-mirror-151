# -*- coding:utf-8 -*-
"""
@Author  :   g1879
@Contact :   g1879@qq.com
@File    :   listener.py
"""
from json import loads, JSONDecodeError
from queue import Queue
from threading import Thread
from time import perf_counter, sleep
from typing import Union, Tuple, List, Iterable
from warnings import filterwarnings

from DrissionPage.mix_page import MixPage
from pychrome import Tab, CallMethodException
from requests import get

filterwarnings("ignore")


class ResponseData(object):
    """返回的数据包管理类"""

    def __init__(self, request_id: str, response: dict, body: str, tab: str, target: str):
        """初始化                               \n
        :param response: response格式化的数据
        :param body: response包含的内容
        :param tab: 产生这个数据包的tab的id
        :param target: 监听目标
        """
        self.request_id = request_id
        self.response = response
        self.raw_body = body
        self.tab = tab
        self.target = target
        self.post_data = None
        self._json_body = None

    def __getattr__(self, item):
        """可用：url、status、statusText、headers、headersText、mimeType、requestHeaders、requestHeadersText、
        connectionReused、connectionId、remoteIPAddress、remotePort、fromDiskCache、fromServiceWorker、
        fromPrefetchCache、encodedDataLength、timing、serviceWorkerResponseSource、responseTime、
        cacheStorageCacheName、protocol、securityState、securityDetails"""
        return self.response.get(item, None)

    @property
    def body(self) -> str:
        """返回body内容，如果是json格式，自动进行转换，其它格式直接返回文本"""
        if self._json_body is not False and self.response.get('mimeType', None) == 'application/json':
            if self._json_body is None:
                try:
                    self._json_body = loads(self.raw_body)
                except JSONDecodeError:
                    self._json_body = False
                    return self.raw_body
            return self._json_body

        else:
            return self.raw_body


class Listener(object):
    """浏览器的数据包监听器"""

    def __init__(self,
                 browser: Union[str, int, MixPage, None] = None,
                 tab_handle: str = None):
        """初始化                                                                      \n
        :param browser: 要监听的url、端口或MixPage对象，MixPage对象须设置了local_port参数。
                        为None时自动从系统中寻找可监听的浏览器
        :param tab_handle: 要监听的标签页的handle，不输入读取当前活动标签页
        """
        self._browser = None
        self._tab = None  # Tab对象
        self._response_count = None
        self._requestIds = None
        self._tmp_response = None  # 捕捉到的所有数据格式[ResponseData, ...]

        self.listening = False
        self.targets = True  # 默认监听所有
        self.results: list = []
        self.tab_id = None  # 当前tab的id
        self._set_browser(browser)
        self.to_tab(tab_handle)

    @property
    def current_tab(self) -> str:
        """返回当前活动标签页的id"""
        return _get_active_tab_id(self._browser)

    def to_tab(self,
               tab_handle: str = None,
               browser: Union[str, int, MixPage, None] = None) -> None:
        """设置要监听的标签页                                                   \n
        :param tab_handle: 要监听的标签页的handle，不输入读取当前活动标签页
        :param browser: 更换别的浏览器
        :return: None
        """
        if browser:
            self._set_browser(browser)

        self.tab_id = tab_handle.split('-')[-1] if tab_handle else self.current_tab
        tab_data = {"id": self.tab_id, "type": "page",
                    "webSocketDebuggerUrl": f"ws://{self._browser}/devtools/page/{self.tab_id}"}
        self._tab = Tab(**tab_data)
        self._tab.start()
        self._tab.Network.enable()
        if self.listening:
            self._tab.Network.responseReceived = self._response_received
            self._tab.Network.loadingFinished = self._loading_finished

    def set_targets(self, targets: Union[str, List[str], Tuple[str], bool, None]) -> None:
        """设置要拦截的目标，可以设置多个                               \n
        :param targets: 要监听的目标字符串或其组成的列表，True监听所有
        :return: None
        """
        if isinstance(targets, str):
            self.targets = [targets]
        elif isinstance(targets, tuple):
            self.targets = list(targets)
        elif isinstance(targets, list) or targets is True:
            self.targets = targets
        else:
            raise TypeError('targets参数只接收字符串、字符串组成的列表、True、None')

    def listen(self,
               targets: Union[str, List[str], Tuple, bool, None] = None,
               count: int = None,
               timeout: float = None,
               asyn: bool = True) -> None:
        """拦截目标请求，直到超时或达到拦截个数，每次拦截前清空结果                                     \n
        可监听多个目标，请求url包含这些字符串就会被记录                                               \n
        :param targets: 要监听的目标字符串或其组成的列表，True监听所有，None则保留之前的目标不变
        :param count: 要记录的个数，到达个数停止监听
        :param timeout: 监听最长时间，到时间即使未达到记录个数也停止，None为无限长
        :param asyn: 是否异步执行
        :return: None
        """
        if targets:
            self.set_targets(targets)

        self.listening = True
        self.results = []
        self._response_count = 0
        self._requestIds = {}
        self._tmp_response = Queue(maxsize=0)

        self._tab.Network.responseReceived = self._response_received
        self._tab.Network.loadingFinished = self._loading_finished

        if asyn:
            Thread(target=self._do_listen, args=(count, timeout)).start()
        else:
            self._do_listen(count, timeout)

    def stop(self) -> None:
        """停止监听"""
        self.listening = False
        print('停止监听')

    def wait(self) -> None:
        """等等监听结束"""
        while self.listening:
            sleep(.5)

    def get_results(self, target: str = None) -> List[ResponseData]:
        """获取结果列表                                        \n
        :param target: 要获取的目标，为None时获取第一个
        :return: 结果数据组成的列表
        """
        return [i for i in self.results if i.target == target]

    def steps(self, gap: int = 1) -> Iterable[List[ResponseData]]:
        """用于单步操作，可实现没收到若干个数据包执行一步操作（如翻页）                 \n
        于是可以根据数据包是否加载完成来决定是否翻页，无须从页面dom去判断是否加载完成     \n
        大大简化代码，提高可靠性                                                   \n
        eg: for i in listener.steps(2):                                        \n
                btn.click()                                                    \n
        :param gap: 每接收到多少个数据包触发
        :return: 用于在接收到监听目标时触发动作的可迭代对象
        """
        while self.listening:
            while self._tmp_response.qsize() >= gap:
                yield [self._tmp_response.get(False) for _ in range(gap)]

            sleep(.1)

    def _do_listen(self,
                   count: int = None,
                   timeout: float = None) -> None:
        """执行监听                                                         \n
        :param count: 要记录的个数，到达个数停止监听
        :param timeout: 监听最长时间，到时间即使未达到记录个数也停止，None为无限长
        :return: None
        """
        print('开始监听')
        t1 = perf_counter()
        # 当收到停止信号、到达须获取结果数、到时间就停止
        while self.listening \
                and (count is None or self._response_count < count) \
                and (timeout is None or perf_counter() - t1 < timeout):
            sleep(.5)

        self._tab.Network.responseReceived = self._null_function
        self._tab.Network.loadingFinished = self._null_function
        self.stop()

    def _loading_finished(self, **kwargs) -> None:
        """请求完成时处理方法"""
        requestId = kwargs['requestId']
        if target := self._requestIds.pop(requestId, None) is None:
            return

        target, response = target.values()
        response = ResponseData(requestId, response, self._get_response_body(requestId), self.tab_id, target)
        if (r := response.response.get('requestHeaders', None)) and r.get(':method', '').lower() == 'post':
            response.post_data = self._get_post_data(requestId)

        self._response_count += 1
        self._tmp_response.put(response)
        self.results.append(response)

    def _response_received(self, **kwargs) -> None:
        """接收到返回信息时处理方法"""
        if self.targets is True:
            self._requestIds[kwargs['requestId']] = {'target': True, 'response': kwargs['response']}

        else:
            for target in self.targets:
                if target in kwargs['response']['url']:
                    self._requestIds[kwargs['requestId']] = {'target': target, 'response': kwargs['response']}

    def _set_browser(self, browser: Union[str, int, MixPage, None] = None) -> None:
        """设置浏览器ip:port                                                               \n
        :param browser: 要监听的url、端口或MixPage对象，MixPage对象须设置了local_port参数。
                        为None时自动从系统中寻找可监听的浏览器
        :return: None
        """
        if isinstance(browser, MixPage):
            browser = browser.drission.driver_options.debugger_address

        elif isinstance(browser, int):
            browser = f'127.0.0.1:{browser}'

        self._browser = browser or _find_chrome()
        if self._browser is None:
            raise RuntimeError('未找到可监听的浏览器。')

    def _null_function(self, **kwargs) -> None:
        """空方法，用于清除绑定的方法"""
        pass

    def _get_response_body(self, request_id: str) -> Union[str, None]:
        """获取返回的内容                  \n
        :param request_id: 请求的id
        :return: 返回内容的文本
        """
        try:
            return self._tab.call_method('Network.getResponseBody', requestId=request_id)['body']
        except CallMethodException:
            return ''

    def _get_post_data(self, response_or_id: Union[str, ResponseData]) -> Union[str, None]:
        """获取请求的post数据"""
        if isinstance(response_or_id, ResponseData):
            response_or_id = response_or_id.request_id

        try:
            return self._tab.call_method('Network.getRequestPostData', requestId=response_or_id)['postData']
        except:
            return None


def _find_chrome() -> Union[str, None]:
    """在系统进程中查找开启调试的Chrome浏览器，只能在Windows系统使用            \n
    :return: ip:port
    """
    from os import popen
    from re import findall, DOTALL, search

    txt = popen('tasklist  /fi "imagename eq chrome.exe" /nh').read()
    pids = findall(r' (\d+) [c,C]', txt, flags=DOTALL)
    for pid in pids:
        txt = popen(f'netstat -ano | findstr "{pid}"').read()
        r = search(r'TCP {4}(\d+.\d+.\d+.\d+:\d+).*?LISTENING.*?\n', txt, flags=DOTALL)
        if r:
            return r.group(1)


def _get_active_tab_id(url: str) -> str:
    """获取浏览器活动标签页id          \n
    :param url: 浏览器ip:port
    :return: 文本形式返回tab id
    """
    try:
        r = get(f'http://{url}/json', json=True, timeout=2).json()
        for i in r:
            if i['type'] == 'page':
                return i['id']

    except Exception:
        raise RuntimeError('未能定位标签页。')
