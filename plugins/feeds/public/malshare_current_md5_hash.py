from datetime import timedelta
import logging

from core.observables import Hash
from core.feed import Feed
from core.errors import ObservableValidationError


class MalshareCurrentMD5(Feed):
    default_values = {
        'frequency': timedelta(hours=1),
        'source': 'http://www.malshare.com/daily/malshare.current.txt',
        'name': 'MalshareCurrentMD5',
        'description': 'Malshare Current List MD5 Hashes'
    }

    def update(self):
        for line in self.update_lines():
            self.analyze(line)

    def analyze(self, line):
        if line.startswith('#'):
            return

        try:
            parts = line.split()
            hash = str(parts[0]).strip()
            context = {
                'source': self.name
            }

            try:
                hash = Hash.get_or_create(value=hash)
                hash.add_context(context)
                hash.add_source('feed')
                hash.tag(['malware'])
            except ObservableValidationError as e:
                logging.error(e)
        except Exception as e:
            logging.debug(e)