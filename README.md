# Mockuments
## Introduction
This is a tool designed to generate random documents which match a certain
specification (based on a template passed to the tool). Its intended use is to
generate a sample dataset based on specific parameters for use in N1QL sizing
and testing, although this can be used for any purpose which requires a
specific dataset.

This is currently in a very very basic stage, with only a few data types
supported, although there is scope to improve on this in future.

This is not designed to be a benchmarking tool in any way, all operations to
Couchbase are synchronous and the document generation can be slow, as such
this tool does not reflect the true throughput that could be achieved using
Couchbase Server, [cbc pillowfight](http://docs.couchbase.com/sdk-api/couchbase-c-client-2.4.0/md_cbc-pillowfight.html)
is a far better tool for that.
This tool is designed to run as a one-off to generate a dataset (and perhaps
modify that dataset at a future point).

Hopefully this tool should be useful to TSEs, SEs as well as any users of
Couchbase wishing to easily randomly generate a dataset.

Disclaimer: Unfortunately in its current incarnation it is very slow when
creating large datasets, so I would not recommend doing so for the time being,
this will be improved over time.

## Usage
`python mockuments.py [file_name]`

The full list of commands be found by typing
`python mockuments.py -h`

#### Templates
Templates are specified in JSON format, an example can be seen here:
```
{
  "string_example": {
    "type": "string",
    "upper_bound": 20,
    "lower_bound": 10
  },
  "float_example": {
    "type": "float",
    "upper_bound": 100000,
    "lower_bound": 10
  },
  "int_example": {
    "type": "int",
    "upper_bound": 100000,
    "lower_bound": 10
  },
  "date_example": {
    "type": "datetime"
  },
  "bool_example": {
    "type": "bool"
  }
}
```
This example can also be found (and used) in the `example_template.json` file.

Currently the accepted data types are:
- `"string"` - String (e.g abcdefg)
- `"datetime"` - Datetime (e.g 1915-05-12T00:00:00Z)
- `"int"` - Integer (e.g 42)
- `"float"` - Float (e.g 2.245)
- `"bool"` - Boolean (True/False)

The fields `string`, `int` and `float` must also have their upper and lower
bounds supplied, a value will be randomly selected between these bounds (for
`string` this value is the length of the string).

## Roadmap
- Allow for document referencing (document keys within other documents)
- Allow user to specify key length and format (only uses a UUID at the moment)
- Add a mode which does not persist the data to Couchbase, perhaps to files
instead
- Allow the user to specify a sample document and all of the relevant metadata
required to generate the documents is calculated
- Allow the user to specify the datetime format, as well as any bounds
- Allow user to specify template using a REPL rather than a json file
