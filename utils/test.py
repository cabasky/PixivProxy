class Cookies:
    rawcookies = ''
    cookiesdict = {}

    def init(self, cstr):
        rawcookies = cstr.replace(' ', '')
        for i in rawcookies.split(';'):
            a, b = i.split('=', 1)
            self.cookiesdict[a] = b

    def __init__(self, cstr=None):
        if cstr == None:
            return
        else:
            rawcookies = cstr.replace(' ', '')
            for i in rawcookies.split(';'):
                a, b = i.split('=', 1)
                self.cookiesdict[a] = b


class Headers:
    rawheaders = ''
    headersdict = {}

    def __init__(self, hstr):
        rawheaders = hstr.replace(' ', '')
        for i in rawheaders.split('|'):
            a, b = i.split(':', 1)
            self.headersdict[a] = b
