import re
import random
import logging
from requests import Response
from cloudscraper import CloudScraper
from typing import Optional, Union, Dict

from . import atjsparse
from .aterrors import CredentialsError, CloudflareError

REQUA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.47'
REQHEADERS = {
	'Host': 'aternos.org',
	'User-Agent': REQUA,
	'Sec-Ch-Ua': '" Not A;Brand";v="99", "Chromium";v="100", "Opera";v="86"',
	'Sec-Ch-Ua-Mobile': '?0',
	'Sec-Ch-Ua-Platform': '"Linux"',
	'Sec-Fetch-Dest': 'document',
	'Sec-Fetch-Mode': 'navigate',
	'Sec-Fetch-Site': 'same-origin',
	'Sec-Fetch-User': '?1',
	'Upgrade-Insecure-Requests': '1'
}

class AternosConnect:

	def __init__(self) -> None:

		self.session = CloudScraper()
		self.atsession = ''

	def parse_token(self) -> str:

		loginpage = self.request_cloudflare(
			f'https://aternos.org/go/', 'GET'
		).content

		# Using the standard string methods
		# instead of the expensive xml parsing
		head = b'<head>'
		headtag = loginpage.find(head)
		headend = loginpage.find(b'</head>', headtag + len(head))

		# Some checks
		if headtag < 0 or headend < 0:
			pagehead = loginpage
			raise RuntimeWarning('Unable to find <head> tag, parsing the whole page')

		# Extracting <head> content
		headtag = headtag + len(head)
		pagehead = loginpage[headtag:headend]

		try:
			text = pagehead.decode('utf-8', 'replace')
			js_code = re.findall(r'\(\(\)(.*?)\)\(\);', text)
			token_func = js_code[1] if len(js_code) > 1 else js_code[0]

			ctx = atjsparse.exec(token_func)
			self.token = ctx.window['AJAX_TOKEN']

		except (IndexError, TypeError):
			raise CredentialsError(
				'Unable to parse TOKEN from the page'
			)

		return self.token

	def generate_sec(self) -> str:

		randkey = self.generate_aternos_rand()
		randval = self.generate_aternos_rand()
		self.sec = f'{randkey}:{randval}'
		self.session.cookies.set(
			f'ATERNOS_SEC_{randkey}', randval,
			domain='aternos.org'
		)

		return self.sec

	def generate_aternos_rand(self, randlen:int=16) -> str:

		# a list with randlen+1 empty strings:
		# generate a string with spaces,
		# then split it by space
		rand_arr = (' ' * (randlen+1)).split(' ')

		rand = random.random()
		rand_alphanum = self.convert_num(rand, 36) + ('0' * 17)

		return (rand_alphanum[:18].join(rand_arr)[:randlen])

	def convert_num(
		self, num:Union[int,float,str],
		base:int, frombase:int=10) -> str:

		if isinstance(num, str):
			num = int(num, frombase)

		if isinstance(num, float):
			sliced = str(num)[2:]
			num = int(sliced)

		symbols = '0123456789abcdefghijklmnopqrstuvwxyz'
		basesym = symbols[:base]
		result = ''
		while num > 0:
			rem = num % base
			result = str(basesym[rem]) + result
			num //= base
		return result

	def add_headers(self, headers:Optional[Dict[str,str]]=None) -> Dict[str,str]:

		headers = headers or {}
		headers.update(REQHEADERS)
		return headers

	def request_cloudflare(
		self, url:str, method:str,
		params:Optional[dict]=None, data:Optional[dict]=None,
		headers:Optional[dict]=None, reqcookies:Optional[dict]=None,
		sendtoken:bool=False, redirect:bool=True, retry:int=0) -> Response:

		if retry > 3:
			raise CloudflareError('Unable to bypass Cloudflare protection')

		try:
			self.atsession = self.session.cookies['ATERNOS_SESSION']
		except KeyError:
			pass

		if method not in ('GET', 'POST'):
			raise NotImplementedError('Only GET and POST are available')

		params = params or {}
		data = data or {}
		reqcookies = reqcookies or {}
		headers = self.add_headers(headers)

		if sendtoken:
			params['TOKEN'] = self.token
			params['SEC'] = self.sec
			headers['X-Requested-With'] = 'XMLHttpRequest'

		# requests.cookies.CookieConflictError bugfix
		reqcookies['ATERNOS_SESSION'] = self.atsession
		del self.session.cookies['ATERNOS_SESSION']

		logging.debug(f'Requesting({method})' + url)
		logging.debug('headers=' + str(headers))
		logging.debug('params=' + str(params))
		logging.debug('data=' + str(data))
		logging.debug('req-cookies=' + str(reqcookies))
		logging.debug('session-cookies=' + str(self.session.cookies))
		
		if method == 'POST':
			req = self.session.post(
				url, data=data, params=params,
				headers=headers, cookies=reqcookies,
				allow_redirects=redirect
			)
		else:
			req = self.session.get(
				url, params={**params, **data},
				headers=headers, cookies=reqcookies,
				allow_redirects=redirect
			)
		
		if '<title>Please Wait... | Cloudflare</title>' in req.text:
			logging.info('Retrying to bypass Cloudflare')
			self.request_cloudflare(
				url, method,
				params, data,
				headers, reqcookies,
				sendtoken, redirect,
				retry - 1
			)
		
		logging.info(
			f'{method} completed with {req.status_code} status'
		)

		return req
