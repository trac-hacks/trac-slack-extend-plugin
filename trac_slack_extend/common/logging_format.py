import logging
from time import gmtime, strftime

str_time = strftime("%H:%M:%S %p", gmtime())
FORMAT = str_time + ' Trac[track_slack_extend] %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)
