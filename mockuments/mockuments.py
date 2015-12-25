import argparse
from couchbase.bucket import Bucket
from templateloader import TemplateLoader
from docgenerator import DocGenerator
import multiprocessing
import sys
import time

DEFAULT_POOL_SIZE = 8
DEFAULT_BATCH_SIZE = 1000


def main():
    parse_arguments(sys.argv[1:])
    template_loader = TemplateLoader(args.template)
    generate_documents(template_loader.template)


def generate_documents(template):
    # Potential issue is that the keys may collide, but this is unlikely
    # with UUIDs
    cb_queue = multiprocessing.Queue()
    processes = list()
    start = time.time()
    for _ in xrange(0, DEFAULT_POOL_SIZE):
        p = multiprocessing.Process(target=per_process_doc_generator,
                                    args=(template, cb_queue,))
        p.start()
        processes.append(p)
    p = multiprocessing.Process(target=store_in_cb, args=(cb_queue,))
    p.start()
    processes.append(p)
    for process in processes:
        process.join()
    end = time.time()
    time_elapsed = end - start
    print('Took {} seconds to generate {} documents'.format(
        time_elapsed, args.number_of_docs))


def per_process_doc_generator(template, cb_queue):
    doc_generator = DocGenerator(template)
    start = time.time()
    put = cb_queue.put
    generate_document = doc_generator.generate_document
    for i in xrange(0, args.number_of_docs/DEFAULT_POOL_SIZE):
        document = generate_document()
        put((document['key'], document['value']))
    end = time.time()
    print('docs generated in {} seconds'.format(end-start))


def store_in_cb(work_queue):
    bkt = connect_to_cb()
    get = work_queue.get
    upsert_multi = bkt.upsert_multi
    while not work_queue.empty():
        docs = dict()
        for _ in xrange(0, DEFAULT_BATCH_SIZE):
            doc = get()
            docs[doc[0]] = doc[1]
        upsert_multi(docs)


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
