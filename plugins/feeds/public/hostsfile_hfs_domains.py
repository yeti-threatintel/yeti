from datetime import timedelta
import logging

from core.observables import Hostname
from core.feed import Feed
from core.errors import ObservableValidationError


class HostsFileHFSDomains(Feed):
    default_values = {
        'frequency': timedelta(hours=1),
        'source': 'https://hosts-file.net/hfs.txt',
        'name': 'HostsFileHFSDomains',
        'description': 'Contains spamming sites listed in the hpHosts database by Domain.'
    }

    def update(self):
        for line in self.update_lines():
            self.analyze(line)

    def analyze(self, line):
        if line.startswith('#'):
            return

        try:
            hostname = str(parts[1]).strip()
            context = {
                'source': self.name
            }

            try:
                host = Hostname.get_or_create(value=hostname)
                host.add_context(context)
                host.add_source('feed')
                host.tag(['spam'])
            except ObservableValidationError as e:
                logging.error(e)
        except Exception as e:
            logging.debug(e)