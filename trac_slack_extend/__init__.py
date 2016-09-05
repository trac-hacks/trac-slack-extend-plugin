from trac.core import Component
from trac_slack_extend.common.logging_format import *

try:
    from slack_notification import *
except ImportError as ex:
    logging.error("Slack Notification plugin does not found", exc_info=True)

try:
    from trac_slack_extend.code_comments_slack import *
except ImportError as ex:
    logging.error("Code comments plugin does not found", exc_info=True)

try:
    from trac_slack_extend.roadmap_tickets_slack import *
except ImportError as ex:
    logging.error("Roadmap Tickets plugin does not found", exc_info=True)


class TracSlackExtend(Component):
    pass
