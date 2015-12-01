import json
import requests
from trac.core import Component, implements
from trac_slack_extend.common.functions_abstract import FunctionsAbstract
from code_comments.api import ICodeCommentChangeListener


class CodeCommentsSlack(Component, FunctionsAbstract):
    implements(ICodeCommentChangeListener)

    def __init__(self):
        super(CodeCommentsSlack, self).__init__()

    def comment_created(self, comment):
        domain = FunctionsAbstract.get_only_main_domain(self.env.abs_href())
        code_comment = {
            'url': '{0}{1}'.format(domain, comment.href()),
            'comment': comment
        }
        self.convert_to_slack_format(code_comment)

    def convert_to_slack_format(self, code_comment):
        template = u'_{project}_ :incoming_envelope: \n{type} <{url}|{id}>: [*{action}* by @{author}]\n>>>{comment}'
        values = {
            'project': self.env.project_name.encode('utf-8').strip(),
            'type': 'code comment',
            'url': code_comment['url'],
            'id': code_comment['comment'].line,
            'action': 'created',
            'author': code_comment['comment'].author,
            'comment': code_comment['comment'].text
        }
        message = template.format(**values)
        data = {
            "channel": self.channel,
            "username": self.username,
            "link_names": 1,
            "text": message.encode('utf-8').strip()
        }
        try:
            requests.post(self.webhook, data={"payload": json.dumps(data)})
        except requests.exceptions.RequestException:
            self.log.error("(Code comments slack) Request cannot be sent", exc_info=True)
