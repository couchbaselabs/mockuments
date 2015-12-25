import json


class TemplateLoader(object):

    def __init__(self, file_name):
        self.file_name = file_name
        self.template = self._load_from_file()
        self.ACCEPTABLE_TYPES = ['string', 'int', 'datetime', 'float', 'bool']
        self.ACCEPTABLE_FIELDS = ['type', 'length']
        if not self._validate_input():
            print('Exiting due to validation failure, see error messages for '
                  'further information')
            exit(1)

    def _load_from_file(self):
        return json.load(open(self.file_name, 'r'))

    def _validate_input(self):
        valid = True
        type_error_fmt = ('Error - Unexpected type found: `{}` - Only `{}` are'
                          ' accepted')
        not_enough_fields_fmt = ('Error - Not enough fields found, ensure that'
                                 ' each element has fields `{}`')
        too_many_fields_fmt = ('Error - Unexpected fields found `{}`, only '
                               '`{}` are accepted')

        for value in self.template.itervalues():
            if len(value.keys()) < len(self.ACCEPTABLE_FIELDS):
                print(not_enough_fields_fmt.format(
                    ', '.join(self.ACCEPTABLE_FIELDS)))
                valid = False
                continue

            elif len(value.keys()) > len(self.ACCEPTABLE_FIELDS):
                unexpected_fields = [key for key in value.iterkeys()
                                     if key not in self.ACCEPTABLE_FIELDS]
                print(too_many_fields_fmt.format(
                    ', '.join(unexpected_fields),
                    ', '.join(self.ACCEPTABLE_FIELDS)))
                valid = False
                continue

            if value['type'] not in self.ACCEPTABLE_TYPES:
                print(type_error_fmt.format(
                    value['type'], ', '.format(self.ACCEPTABLE_TYPES)))
                valid = False

            try:
                value['length'] = int(value['length'])
            except Exception:
                print('Error - Length value cannot be converted to int')
                valid = False

        return valid