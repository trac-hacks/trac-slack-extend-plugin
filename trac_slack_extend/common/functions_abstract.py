from urlparse import urlparse


class FunctionsAbstract(object):
    def __init__(self):
        self.webhook = self.env.config.get('slack', 'webhook')
        self.channel = self.env.config.get('slack', 'channel')
        self.username = self.env.config.get('slack', 'username', 'Trac-Bot')
        self.fields = self.env.config.get('slack', 'fields')

    def convert_to_slack_format(self, code_comment):
        raise NotImplementedError

    @staticmethod
    def get_only_main_domain(abs_url):
        parsed_uri = urlparse(abs_url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        return domain
