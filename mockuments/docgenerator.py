import random
import string
import datetime
import uuid


class DocGenerator(object):
    def __init__(self, template):
        self.template = template
        self.DATA_TYPE_MAPPING = {
                                  'datetime': self.generate_random_date,
                                  'string': self.generate_random_string,
                                  'int': self.generate_random_int,
                                  'float': self.generate_random_float,
                                  'bool': self.generate_random_bool,
                                  }
        self.DEFAULT_LENGTH = 32

    def generate_document(self):
        document = dict()
        document['key'] = str(uuid.uuid4())
        document['value'] = dict()
        for field_name, metadata in self.template.iteritems():
            document['value'][field_name] = self.generate_field_value(metadata)
        return document

    def generate_field_value(self, metadata):
        return self.DATA_TYPE_MAPPING[metadata['type']](
            metadata['length'] if 'length' in metadata
            else self.DEFAULT_LENGTH)

    @staticmethod
    def generate_random_date(_):
        year = random.randint(1900, datetime.datetime.now().year)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        datetime_fmt = '%m/%d/%Y'
        return datetime.datetime(year, month, day).strftime(datetime_fmt)

    @staticmethod
    def generate_random_string(length):
        value = ''.join(random.choice(string.lowercase)
                        for _ in xrange(0, length))
        return value

    def generate_random_int(self, length):
        # FIXME: This can generate values too big to be ints
        return int(self.generate_random_float(length))

    @staticmethod
    def generate_random_float(length):
        # FIXME: Floats become truncated, bounds would be more sensible than
        # lengths
        value = random.random() * pow(10, length)
        return value

    @staticmethod
    def generate_random_bool(_):
        value = random.choice([True, False])
        return value
