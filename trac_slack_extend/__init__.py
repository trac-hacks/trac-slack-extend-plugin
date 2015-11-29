from trac.core import Component
from trac_slack_extend.common import functions_abstract
from trac_slack_extend.common.logging_format import *

try:
    from slack_notification import *
except ImportError as ex:
    logging.error("Slack Notification plugin does not found", exc_info=True)

try:
    from trac_slack_extend import code_comments_slack
except ImportError as ex:
    logging.error("Code comments plugin does not found", exc_info=True)


class TracSlackExtend(Component):
    pass
