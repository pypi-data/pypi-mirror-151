"""
Markdown Text Decorator Extension
========================================

This is a [Python-Markdown](https://pypi.org/project/Markdown/) Text Decorator extension package.

Copyright 2022 Silver Bullet Software All rigths reserved.

License: MIT see) file:LICENSE

"""
from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagInlineProcessor


DECO_TARGET_TBL = {
    "strikethrough" : {
        "p": r'(\~\~)(.*)(\~\~)',
        "t": "s"
    },
    "delete": {
        "p": r'(\-\-)(.*)(\-\-)',
        "t": "del"
    },
    "insert": {
        "p": r'(\+\+)(.*)(\+\+)',
        "t": "ins"
    },
}
PROC_BASE_PRIORITY=100


class MarkdownTextDecoratorExtension(Extension):


    def extendMarkdown(self, md):
        priority = PROC_BASE_PRIORITY
        for proc_name, props in DECO_TARGET_TBL.items():
            proc_item = SimpleTagInlineProcessor(pattern=props["p"], tag=props["t"])
            md.inlinePatterns.register(item=proc_item, name=proc_name, priority=priority)
            priority += 1


def makeExtension(**kwargs):
    return MarkdownTextDecoratorExtension(**kwargs)
