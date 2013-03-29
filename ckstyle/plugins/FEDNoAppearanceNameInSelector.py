#/usr/bin/python
#encoding=utf-8

from Base import *
from helper import existsAppearanceWords

class FEDNoAppearanceNameInSelector(RuleSetChecker):
    
    '''{
        "summary":"xxx",
        "desc":"xxx"
    }'''

    def __init__(self):
        self.id = 'no-appearance-word-in-selector'
        self.errorLevel = ERROR_LEVEL.WARNING
        self.errorMsg_origin = 'should not use appearance word "%s" in "${selector}"'
        self.errorMsg = ''

    def check(self, ruleSet, config):
        selector = ruleSet.selector.lower()

        if selector.find('@media') != -1:
            return True
        if selector.find('@-moz-document') != -1:
            return True

        word = existsAppearanceWords(selector)
        if word is not None:
            self.errorMsg = self.errorMsg_origin % word
            return False

        return True
