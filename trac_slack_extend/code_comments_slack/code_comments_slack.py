from trac.core import Component, implements
from trac_slack_extend.common.functions_abstract import FunctionsAbstract
from code_comments.api import ICodeCommentChangeListener


class CodeCommentsSlack(Component, FunctionsAbstract):
    implements(ICodeCommentChangeListener)

    def comment_created(self, comment):
        # TODO: GET domain
        print dir(comment)
        print vars(comment)
        print ("Author = {0}\n Text = {1}\n Href={2}\n".format(comment.author, comment.text, comment.href()))

    def convert_to_slack_format(self, code_comment):
        pass
