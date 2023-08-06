#
# Module: inject
#
# Description: Command to inject specified messages into a RabbitMQ queue
#

import pika

def get_channel(parameters,
                task_queue):
    """
    Gets the channel that will be supplying the processing requests.
    """
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue = task_queue,
                          durable=True)
    return connection, channel


def getIgnoreMessage():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<execution_request action="ignore"/>
"""


def getSleepWorkerMessage(duration):
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<execution_request action="sleep:""" + str(duration) +""""/>
"""


def getStopListeningMessage():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<execution-request action="stop_listening" />
"""


def getStopWorkerMessage():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<execution-request action="stop_worker" />
"""


def main():
    import argparse
    import os
    import sys

    from rabbitmq_consume import parameter_utils

    parser = argparse.ArgumentParser(description='Generic Client to consume a RabbitMQ queue.')
    parser.add_argument('-d',
                      '--debug',
                      dest='DEBUG',
                      help='print out detail information to stdout.',
                      action='store_true',
                      default=False)
    parser.add_argument('-i',
                        '--rabbit_ini',
                        dest='RABBITMQ_INI',
                        help='The path to the file contains the RabbitMQ INI file, the default is $HOME/.rabbitMQ.ini')
    parser.add_argument('-l',
                        '--stop_listening',
                        dest='STOP_LISTENING',
                        help='injects a "stop listening" message onto the stream',
                        action='store_true',
                        default=False)
    parser.add_argument('-n',
                        '--sleep_worker',
                        dest='SLEEP_WORKER',
                        help='injects a "sleep worker for n seconds" message onto the stream',
                        type=int,
                        default=0)
    parser.add_argument('-s',
                        '--ini_section',
                        dest='INI_SECTION',
                        help='The section of the INI file to use for this execution, the default is "RabbitMQ"',
                        default='RabbitMQ')
    parser.add_argument('-w',
                        '--stop_worker',
                        dest='STOP_WORKER',
                        help='injects a "stop worker" message onto the stream',
                        action='store_true',
                        default=False)
    parser.add_argument('queue',
                        help='The rabbitMQ queue which this client should consume',
                        default=None)
    options = parser.parse_args()

    if None == options.queue:
        print >> sys.stderr, "RabbitMQ queue must be supplied"
        sys.exit(-1)

    parameters = parameter_utils.get_parameters(options.RABBITMQ_INI,
                                                options.INI_SECTION)
    (connection, channel) = get_channel(parameters,
                                        options.queue)

    if options.STOP_LISTENING:
        message = getStopListeningMessage()
    elif options.STOP_WORKER:
        message = getStopWorkerMessage()
    elif None != options.SLEEP_WORKER:
        message = getSleepWorkerMessage(options.SLEEP_WORKER)
    else:
        message = getIgnoreMessage()
    channel.basic_publish(exchange = '',
                          routing_key = options.queue,
                          body = message,
                          properties=pika.BasicProperties(delivery_mode = 2,))

    connection.close()
