__author__ = 'joern'

import yaml

class AppKey:
    def __init__(self, appkey):
        k=dict((k.lower(), v) for k,v in appkey.iteritems())
        self.ApplicationKeyName =  k["applicationkeyname"]

    @classmethod
    def fromyaml(cls,appkeyyaml):
        return cls(yaml.load(appkeyyaml))