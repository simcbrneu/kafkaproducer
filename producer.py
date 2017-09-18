#!/usr/bin/env python
#
# https://docs.confluent.io/current/clients/confluent-kafka-python/
#

import os
import tempfile

from confluent_kafka import Producer

def get_keytab(url):
    try:
        # python 3
        from urllib.request import urlopen
    except ImportError:
        # python 2
        from urllib2 import urlopen

    fd, keytab_file = tempfile.mkstemp()
    r = urlopen(url)
    with os.fdopen(fd, "w+b") as f:
        while True:
            chunk = r.read(4096)
            if not chunk:
                break
            f.write(chunk)
    return keytab_file

def producer():
    env_list = [
        'kafka_principal',
        'kafka_keytab',
        'kafka_brokers',
        'kafka_topic',
    ]
    for env in env_list:
        envv = os.environ.get(env)
        if envv:
            globals()[env] = envv
        else:
            raise Exception("missing env '{}'".format(env))

    p = Producer({
        'security.protocol': 'sasl_plaintext',
        'sasl.kerberos.principal': kafka_principal,
        'sasl.kerberos.keytab': get_keytab(kafka_keytab),
        'bootstrap.servers': kafka_brokers,
    })

    data = ['1', '2', '3', '4', '5']
    for d in data:
        p.produce(kafka_topic, d.encode('utf-8'))
        print "produce:", d

    p.flush()

