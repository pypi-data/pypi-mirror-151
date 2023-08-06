# `rabbitmq_consume` project #

The `rabbitmq_consume` project contains both the `rabbitmq_consume` package that provides a simple `Consumer` class for processing messages from a RabbitMQ queue, `rmq-consume` that is an executable that can be used to run that class and `rmq-inject` that cna be used to inject messages into the originating RabbitMQ queue.


## `rmq-consume` executable ##

More details about the `rmq-consume` executable can be found using its help option

    rmq-consume -h

The typical usage is the following:

    rmq-consume <queue> <module>[.<class>]

where `<queue>` is that name of the RabbitMQ queue from which the XML messages should be consumed and `<class>` is a python class in the `<module>` python module that will actually process the messages. If the `.<class> is omitted from the comand line, the class whose name matches the module name will be used.

The "consumption" class need to derived from the `Consumption.Consumption` as shown in the following trivial example.

    from Consumption import Consumption

    class TrivialConsumption(Consumption):

        def __init__(self,
                     properties,
                     body,
                     redelivered):

        def consume(self):
            pass

Most real implementations will save the `properties`, `body` and `redelivered` arguments for use in the `consume` method.


## `rmq-inject` executable ##

More details about the `rmq-inject` executable can be found using its help option

    rmq-inject -h

The typical usage is the following:

    rmq-inject -l <queue>

This injects a "stop listening message" into the queue and when the consumer encounters this it will stop listening for an more messages and shut down.
