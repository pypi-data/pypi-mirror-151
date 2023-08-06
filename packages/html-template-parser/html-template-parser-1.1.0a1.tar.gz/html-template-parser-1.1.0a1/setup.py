# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['HtmlTemplateParser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'html-template-parser',
    'version': '1.1.0a1',
    'description': 'A parser for HTML templates.',
    'long_description': '<h1 align="center">HTML Template Parser</h1>\n\n<h4 align="center">Modified version of Python\'s HTMLParser for HTML template parsing</h4>\n\n<p align="center">\n  <a href="https://codecov.io/gh/Riverside-Healthcare/html-template-parser">\n    <img src="https://codecov.io/gh/Riverside-Healthcare/html-template-parser/branch/master/graph/badge.svg?token=Chqq9Mai1h"/>\n  </a>\n  <a href="https://github.com/Riverside-Healthcare/html-template-parser/actions/workflows/test.yml">\n    <img src="https://github.com/Riverside-Healthcare/html-template-parser/actions/workflows/test.yml/badge.svg" alt="Test Status">\n  </a>\n  <a href="https://www.codacy.com/gh/Riverside-Healthcare/html-template-parser/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Riverside-Healthcare/html-template-parser&amp;utm_campaign=Badge_Grade">\n    <img src="https://app.codacy.com/project/badge/Grade/43736e5b780a49d88d8ce588f5cfb9bc"/>\n  </a>\n  <a href="https://pepy.tech/project/html-template-parser">\n    <img src="https://static.pepy.tech/badge/html-template-parser" alt="Downloads">\n  </a>\n  <a href="https://pypi.org/project/html-template-parser/">\n    <img src="https://badgen.net/pypi/v/html-template-parser" alt="Pypi Version">\n  </a>\n</p>\n\n## 🤔 For What?\n\nThe is an HTML template parser. It is a modified version of Python\'s HTMLParse library, expanded to handle template tags.\n\n### Currently Supported\n\n- [x] Comments\n- [ ] Template tags (if/for/...)\n\n## 💾 Install\n\n```sh\npip install html-template-parser\n\n# or\n\npoetry add html-template-parser\n```\n\n## ✨ How to Use\n\nA basic usage example is remarkably similar to Python\'s HTMLParser:\n\n```py\nfrom HtmlTemplateParser import Htp\n\nclass MyHTMLParser(Htp):\n    def handle_starttag(self, tag, attrs):\n        print("Encountered a start tag:", tag)\n\n    def handle_endtag(self, tag):\n        print("Encountered an end tag :", tag)\n\n    def handle_data(self, data):\n        print("Encountered some data  :", data)\n\nparser = MyHTMLParser()\nparser.feed(\'<html><head><title>Test</title></head>\'\n            \'<body><h1>Parse me!</h1></body></html>\')\n\n```\n\n## 🏷 Function Naming Conventions\n\n### Comments\n\n- comment `<!-- -->`\n- comment_curly_hash `{# data #}`\n- comment_curly_exlaim `{{! data }}`\n- comment_curly_exlaim_dash `{{!-- data }}`\n- comment_curly_perc `{% comment "attrs" %}data {% endcomment %}`\n- comment_at_star `@* data *@`\n',
    'author': 'Christopher Pickering',
    'author_email': 'cpickering@rhc.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Riverside-Healthcare/html-void-elements',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
