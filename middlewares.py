from fake_useragent import UserAgent

class RandomMiddleware(object):
    """This middleware allows spiders to override the user_agent"""

    def __init__(self):
        self.ua = UserAgent()

    def process_request(self, request, spider):
        request.headers.setdefault('Cookie', 'ig_cb=1; csrftoken=PFHzNDj4FCUS6qP1M4JfgUsh9r5Qxfo1; mid=W5dkEQAEAAEwaLkxt9NHNJ09zJ9G; rur=FRC; mcd=3; csrftoken=PFHzNDj4FCUS6qP1M4JfgUsh9r5Qxfo1; ds_user_id=8568922729; sessionid=IGSCb4b07b2a011429bbcc040185579e59309ca8aa94d8a40736ac3c88f305404a95%3A1g2GF2BLnzEp3j9j31JMizvNnD0ImIjC%3A%7B%22_auth_user_id%22%3A8568922729%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_platform%22%3A4%2C%22_token_ver%22%3A2%2C%22_token%22%3A%228568922729%3Ar9AST7KP1MnKoySxTr8nzQUdOAIvFZe6%3A96f606757eab963ac0ae57c7936004ed50dea487448ce065b9404502fbc2606c%22%2C%22last_refreshed%22%3A1536648554.6300349236%7D; urlgen="{\"178.128.117.45\": 14061}:1fzcrQ:g0cK-t5UC8_8ch8CpJf1DG-o6Fc"')
        request.headers.setdefault('Host', 'www.instagram.com')
        request.headers.setdefault(b'User-Agent', self.ua.random)
