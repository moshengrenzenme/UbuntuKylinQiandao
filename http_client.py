# coding: utf-8
'''
Created on 2018年8月19日

@author: root
'''
#模块改自smartqq（网页版qq），项目地址：https://github.com/Yinzo/SmartQQBot.git
import http.cookiejar as cookielib
import time
import os
import logging
COOKIE_FILE='cookie.txt'
SSL_VERIFY=True
import requests
from requests import exceptions as excps
def _get_cookiejar(cookie_file):
    return cookielib.LWPCookieJar(cookie_file)
class HttpClient(object):
    def __init__(self,cookie_file=COOKIE_FILE):
        self._cookie_file = cookie_file
        self._cookies = _get_cookiejar(cookie_file)
        
        self.session = requests.session()
        self.session.cookies = self._cookies
    @staticmethod
    def _get_headers():
        """
        :type headers: dict
        :rtype: dict
        """
        _headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
            'Referer': 'https://www.ubuntukylin.com/ukylin/forum.php',
        }
        #_headers.update(headers)
        return _headers
    def load_cookie(self):
        try:
            self._cookies.load(ignore_discard=True, ignore_expires=True)
        except :
            logging.warn("Failed to load cookie file {0}".format(self._cookie_file))
        finally:
            self._cookies.save(ignore_discard=True, ignore_expires=True)
    def get(self, url, refer=None):
        try:
            resp = self.session.get(
                url,
                
                headers=self._get_headers(),
                verify=SSL_VERIFY,
            )
        except (excps.ConnectTimeout, excps.HTTPError):
            error_msg = "Failed to send finish request to `{0}`".format(
                url
            )
            logging.exception(error_msg)
            return error_msg
        except requests.exceptions.SSLError:
            logging.exception("SSL连接验证失败，请检查您所在的网络环境。")
        else:
            self._cookies.save(COOKIE_FILE, ignore_discard=True, ignore_expires=True)
            return resp.text

    def post(self, url, data,params=None, refer=None):
        try:
            resp = self.session.post(
                url,
                params=params,
                data=data,
                headers=self._get_headers(),
                verify=SSL_VERIFY,
            )
        except requests.exceptions.SSLError:
            logging.exception("SSL连接验证失败，请检查您所在的网络环境。如果需要禁用SSL验证，请修改config.py中的SSL_VERIFY为False")
        except (excps.ConnectTimeout, excps.HTTPError):
            error_msg = "Failed to send request to `{0}`".format(
                url
            )
            logging.exception(error_msg)
            return error_msg
        else:
            self._cookies.save(COOKIE_FILE, ignore_discard=True, ignore_expires=True)
            return resp.text

    def get_cookie(self, key):
        for c in self._cookies:
            if c.name == key:
                return c.value
        return ''

    def download(self, url, fname):
        with open(fname, "wb") as o_file:
            try:
                resp = self.session.get(url, headers=self._get_headers(),stream=True, verify=SSL_VERIFY)
            except requests.exceptions.SSLError:
                logging.exception("SSL连接验证失败，请检查您所在的网络环境。")
            except (excps.ConnectTimeout, excps.HTTPError):
                error_msg = "Failed to send request to `{0}`".format(
                    url
                )
                logging.exception(error_msg)
                return error_msg
            else:
                self._cookies.save(COOKIE_FILE, ignore_discard=True, ignore_expires=True)
                o_file.write(resp.raw.read())