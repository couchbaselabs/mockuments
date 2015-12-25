import random
import string
import datetime
import uuid


class DocGenerator(object):
    def __init__(self, template):
        self.template = template
        self.DATA_TYPE_MAPPING = dict(datetime=(self.generate_random_date,
                                                False),
                                      string=(self.generate_random_string,
                                              True),
                                      int=(self.generate_random_int, True),
                                      float=(self.generate_random_float, True),
                                      bool=(self.generate_random_bool, False))

    def generate_document(self):
        # The big problem here is that random generation is slow, perhaps look
        # at making this not-so-random in future to improve throughput,
        # maybe offer this as an option
        document = dict()
        document['key'] = str(uuid.uuid4())
        document['value'] = dict()
        generate_field_value = self.generate_field_value
        for field_name, metadata in self.template.iteritems():
            document['value'][field_name] = generate_field_value(metadata)
        return document

    def generate_field_value(self, metadata):
        need_bounds = self.DATA_TYPE_MAPPING[metadata['type']][1]
        if need_bounds:
            return self.DATA_TYPE_MAPPING[metadata['type']][0](
                metadata['lower_bound'], metadata['upper_bound'])
        else:
            return self.DATA_TYPE_MAPPING[metadata['type']][0]()

    @staticmethod
    def generate_random_date():
        year = random.randint(1900, datetime.datetime.now().year)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return ''.join([datetime.datetime(year, month, day).isoformat(), 'Z'])

    @staticmethod
    def generate_random_string(lower_bound, upper_bound):
        length = random.randint(lower_bound, upper_bound)
        value = ''.join(random.choice(string.lowercase)
                        for _ in xrange(0, length))
        return value

    @staticmethod
    def generate_random_int(lower_bound, upper_bound):
        value = int(random.randint(lower_bound, upper_bound))
        return value

    @staticmethod
    def generate_random_float(lower_bound, upper_bound):
        value = random.uniform(lower_bound, upper_bound)
        return value

    @staticmethod
    def generate_random_bool():
        value = random.choice([True, False])
        return value
