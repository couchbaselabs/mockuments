import argparse
from couchbase.bucket import Bucket
from templateloader import TemplateLoader
from docgenerator import DocGenerator
import multiprocessing
import math
import uuid
import sys

DEFAULT_BATCH_SIZE = 25
DEFAULT_POOL_SIZE = 8


def main():
    parse_arguments(sys.argv[1:])
    template_loader = TemplateLoader('/Users/matt/Documents/test.json')
    bkt = connect_to_cb()
    generated_docs = generate_documents(template_loader.template)
    store_in_cb(generated_docs, bkt)


def generate_documents(template):
    # TODO: Improve document generation, currently will use a lot of memory
    # Unfortunately storage has to be serial, maybe use a lock?

    manager = multiprocessing.Manager()
    generated_docs = manager.dict()
    processes = list()
    for _ in xrange(0, DEFAULT_POOL_SIZE):
        p = multiprocessing.Process(target=per_process_doc_generator,
                                    args=(template, generated_docs,))
        p.start()
        processes.append(p)

    for process in processes:
        process.join()

    # Converts docs back to normal dict
    generated_docs = {key: generated_docs[key]
                      for key in generated_docs.keys()}
    return generated_docs


def per_process_doc_generator(template, generated_docs):
    doc_generator = DocGenerator(template)
    for _ in xrange(0, args.number_of_docs/DEFAULT_POOL_SIZE):
        document = doc_generator.generate_document()
        while document['key'] in generated_docs:
            # Keep regenerating uuid until no collision
            document['key'] = str(uuid.uuid4())
        generated_docs[document['key']] = document['value']


def store_in_cb(documents, bucket):
    batches = int(math.ceil(len(documents)/float(DEFAULT_BATCH_SIZE)))
    for i in xrange(0, batches):
        start = i * DEFAULT_BATCH_SIZE
        try:
            batch = {key: documents[key] for key in
                     documents.keys()[start:start+25]}
        except IndexError:
            batch = {key: documents[key] for key in
                     documents.keys()[start:]}
        bucket.upsert_multi(batch)


def connect_to_cb():
    conn_str = 'couchbase://{}/{}'.format(args.host, args.bucket)
    return Bucket(conn_str)


def parse_arguments(arguments):
    parser = argparse.ArgumentParser(description='Mockuments - a tool to '
                                     'generate random datasets which are of a'
                                     ' particular format and store them in'
                                     ' Couchbase Server')
    parser.add_argument('template', nargs=1, help='Path to your template '
                                                  'JSON document')
    parser.add_argument('--number_of_docs', '-n', type=int, default=1000,
                        help='Number of documents to generate')
    parser.add_argument('--host', default='localhost',
                        help='IP/Hostname of your Couchbase Server instance')
    parser.add_argument('--bucket', '-b', default='default',
                        help='Name of the Couchbase bucket in which to store'
                        ' the data')
    global args
    args = parser.parse_args(arguments)


if __name__ == '__main__':
    main()
