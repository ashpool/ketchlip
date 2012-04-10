#-*- coding: utf-8 -*-

class Querystring:

    def __init__(self, url):
        self.url = url

    def get_values(self, key):
        start_point = self.url.find("?")
        querystring = self.url[start_point + 1:]
        keys = {}
        if querystring:
            key_values = querystring.split("&")
            for kv in key_values:
                keyvalue = kv.split("=")
                k = keyvalue[0]
                if len(keyvalue) == 1:
                    return []
                values = keyvalue[1].split("+")
                value = []
                for v in values:
                    value.append(v)
                keys[k] = value

        return keys[key]

    def page(self):
        end_point = self.url.find("?")
        if end_point > 0:
            uri = self.url[:end_point]
        else:
            uri = self.url
        start_point = uri.rfind("/") + 1
        page = uri[start_point:]
        print page
        if page.find(".twp", -len(".twp")) > 0:
            return page

