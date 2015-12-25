import json


class TemplateLoader(object):

    def __init__(self, file_name):
        self.file_name = file_name
        self.template = self._load_from_file()
        self.ACCEPTABLE_TYPES = dict(string=True, int=True, datetime=False,
                                     float=True, bool=False)
        self.ACCEPTABLE_FIELDS = ['type', 'lower_bound', 'upper_bound', ]
        if not self._validate_input():
            print('Exiting due to validation failure, see error messages for '
                  'further information')
            exit(1)

    def _load_from_file(self):
        return json.load(open(self.file_name, 'r'))

    def _validate_input(self):
        valid = True
        type_error_fmt = ('Error - Unexpected type for field `{}`: Only '
                          '`{}` are accepted')
        unexpected_fields_fmt = ('Error - Unexpected inputs for field `{}`: '
                                 '`{}`')
        no_type_fmt = 'Error - No `type` input in template for field `{}`'
        upper_bound_int_fmt = ('Error - Upper bound for field `{}` cannot be '
                               'converted to an int')
        no_upper_bound_fmt = ('Error - No upper bound value specified for '
                              'field `{}`')
        lower_bound_int_fmt = ('Error - Lower bound for field `{}` cannot be '
                               'converted to an int')
        no_lower_bound_fmt = ('Error - No lower bound value specified for '
                              'field `{}`')
        invalid_bounds_fmt = ('Error - Lower bound is higher than upper bound '
                              'for field `{}`')

        for field in self.template.iterkeys():
            unexpected_fields = [key for key in self.template[field].iterkeys()
                                 if key not in self.ACCEPTABLE_FIELDS]
            if unexpected_fields:
                print(unexpected_fields_fmt.format(
                    field,
                    ', '.join(self.ACCEPTABLE_FIELDS)))
                valid = False
                continue

            if 'type' in self.template[field]:
                need_bounds = self.ACCEPTABLE_TYPES[self.template[field]
                                                    ['type']]
            else:
                print(no_type_fmt.format(field))
                continue

            if self.template[field]['type'] not in self.ACCEPTABLE_TYPES:
                print(type_error_fmt.format(
                    self.template[field]['type'], ', '.format(
                        self.ACCEPTABLE_TYPES)))
                valid = False
                continue

            if need_bounds:
                upper_bound = None
                lower_bound = None
                try:
                    upper_bound = int(self.template[field]['upper_bound'])
                except ValueError:
                    print(upper_bound_int_fmt.format(field))
                    valid = False
                except KeyError:
                    print(no_upper_bound_fmt.format(field))
                    valid = False

                try:
                    lower_bound = int(self.template[field]['lower_bound'])
                except ValueError:
                    print(lower_bound_int_fmt.format(field))
                    valid = False
                except KeyError:
                    print(no_lower_bound_fmt.format(field))
                    valid = False

                if upper_bound and lower_bound and upper_bound < lower_bound:
                    print(invalid_bounds_fmt.format(field))
                    valid = False

        return valid
