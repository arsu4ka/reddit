# import httpx
# from bs4 import BeautifulSoup
# from loguru import logger
# from httpx import AsyncClient
# from fake_useragent import UserAgent

# class RedditProfile():

#     def __init__(self, username: str, password: str, proxy: dict, debug: bool = False) -> None:
#         self.username = username
#         self.password = password
#         self.token = None
#         self.logged = False
#         self.debug = debug
#         self.proxy = {}
#         if proxy["host"] != "" and proxy["port"] != "":
#             self.proxyStr = f"http://{proxy['proxy_user']}:{proxy['proxy_pass']}@{proxy['host']}:{proxy['port']}"
#             self.proxy["https://"] = self.proxyStr
#             self.proxy["http://"] = self.proxyStr
#         self.session = AsyncClient(proxies=self.proxy, headers={"user-agent": UserAgent().random}, timeout=httpx.Timeout(10.0, connect=60.0))

#     async def get_cookies(self):
#         return dict(self.session.cookies.items())

#     async def valid_proxy(self):
#         try:
#             response_proxy = await self.session.get("https://api.ipify.org")
#             async with AsyncClient() as aioSession:
#                 response_defIp = await aioSession.get("https://api.ipify.org")
#             assert response_proxy.text != response_defIp.text
#             return True
#         except:
#             logger.error(f"Proxy for account {self.username} is not valid!")
#             return False
    
#     async def login(self) -> None:
#         if bool(self.proxy):
#             if not await self.valid_proxy():
#                 return None

#         formResponse = await self.session.get("https://www.reddit.com/login/")
#         soup = BeautifulSoup(await formResponse.aread(), "lxml")

#         csrf_token = soup.find("input", {'name': 'csrf_token'})["value"]
#         data = {
#             "csrf_token": csrf_token,
#             'otp': '',
#             'password': self.password,
#             'dest': 'https://www.reddit.com/',
#             'username': self.username,
#         }
#         r = await self.session.post('https://www.reddit.com/login', data=data)
        
#         if self.debug:
#             try:
#                 print(await r.json())
#             except:
#                 print(r.text)
#         if int(r.status_code) != 200:
#             logger.error("Unexpected error occured while logging in")
#             return

#         self.logged = True

#         r = await self.session.get("https://www.reddit.com/")

#         soup = BeautifulSoup(r.text, "lxml")
#         script_block = soup.find("script", {"id": "data"}).text
#         list_1 = script_block.split('"')
#         self.token = list_1[list_1.index("accessToken") + 2]

#         logger.info(f"Successfully logged into reddit account '{self.username}'")
#         logger.info(f"Bearer token for acc '{self.username}' is '{self.token}'")

#     async def vote(self, reddit_post, upvote = True) -> None:
#         if (not self.logged) or (not self.token):
#             logger.error(f"Can't vote post from account {self.username} because login wasn't done")
#             return
        
#         temp = reddit_post.split("/")
#         postID = temp[temp.index("comments") + 1]
#         cookie_dict = await self.get_cookies()
#         params = {
#             'redditWebClient': 'desktop2x',
#             'app': 'desktop2x-client-production',
#             'raw_json': '1',
#             'gilding_detail': '1',
#         }
#         data = {
#             'id': f't3_{postID}',
#             'dir': '1' if upvote else "-1",
#             'api_type': 'json',
#         }
#         headers = {
#             'x-reddit-loid': cookie_dict['loid'],
#             'x-reddit-session': cookie_dict['reddit_session'],
#             'authorization': f'Bearer {self.token}',
#         }

#         response = await self.session.post('https://oauth.reddit.com/api/vote', params=params, data=data, headers=headers)
        
#         if self.debug:
#             try:
#                 print(await response.json())
#             except:
#                 print(response.text)
#         if int(response.status_code) != 200:
#             if upvote:
#                 logger.error("Unexpected error occured while upvoting the post")
#             else:
#                 logger.error("Unexpected error occured while downvoting the post")
#             return
#         else:
#             if upvote:
#                 logger.info(f"Reddit post '{postID}' was successfully upvoted from profile '{self.username}'")
#             else:
#                 logger.info(f"Reddit post '{postID}' was successfully downvoted from profile '{self.username}'")
    
#     async def logout(self):
#         await self.session.aclose()
