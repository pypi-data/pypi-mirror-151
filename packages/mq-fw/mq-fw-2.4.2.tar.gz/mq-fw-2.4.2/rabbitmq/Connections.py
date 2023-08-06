# -*- coding: UTF-8 -*-
# @Time : 2021/12/2 下午5:55
# @Author : 刘洪波
from rabbitmq.Consumers import Consumer
from rabbitmq.Producers import Producer
from rabbitmq.Services import ConsumeProduce, ProduceConsume, ConsumeProduceFlow


class Connection(object):
    def __init__(self, host, port, username, password, heartbeat):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.heartbeat = heartbeat

    def create_consumer(self, exchange, routing_key, durable=False, random_tag=False):
        """
        消费者
        :param exchange:
        :param routing_key:
        :param durable:
        :param random_tag: 是否随机 exchange， routing_key
        :return:
        """
        return Consumer(self.host, self.port, self.username, self.password,
                        self.heartbeat, exchange, routing_key, durable, random_tag)

    def create_producer(self, exchange, routing_key, durable=False):
        """
        生产者
        :param exchange:
        :param routing_key:
        :param durable:
        :return:
        """
        return Producer(self.host, self.port, self.username, self.password,
                        self.heartbeat, exchange, routing_key, durable)

    def consume_produce(self, consumer_exchange, consumer_routing_key,
                        producer_exchange=None, producer_routing_key=None, durable=False,
                        consumer_durable=None, producer_durable=None):
        """
        服务端（先消费再生产）
        :param consumer_exchange:
        :param consumer_routing_key:
        :param producer_exchange:
        :param producer_routing_key:
        :param durable:
        :param consumer_durable:
        :param producer_durable:
        :return:
        """
        producer = None
        if producer_exchange and producer_routing_key:
            producer = self.create_producer(producer_exchange, producer_routing_key,
                                            producer_durable if producer_durable else durable)
        elif producer_exchange:
            raise ValueError('producer_routing_key is None, need producer_routing_key')
        elif producer_routing_key:
            raise ValueError('producer_exchange is None, need producer_exchange')
        return ConsumeProduce(self.create_consumer(consumer_exchange, consumer_routing_key,
                                                   consumer_durable if consumer_durable else durable),
                              producer, self.create_producer if not producer else None)

    def produce_consume(self, producer_exchange, producer_routing_key,
                        consumer_exchange=None, consumer_routing_key=None, durable=False,
                        consumer_durable=None, producer_durable=None):
        """
        调用端（先生产再消费）
        :param consumer_exchange:
        :param consumer_routing_key:
        :param producer_exchange:
        :param producer_routing_key:
        :param durable:
        :param consumer_durable:
        :param producer_durable:
        :return:
        """
        consumer = None
        if consumer_exchange and consumer_routing_key:
            consumer = self.create_consumer(consumer_exchange, consumer_routing_key,
                                            consumer_durable if consumer_durable else durable)
        elif consumer_exchange:
            raise ValueError('consumer_routing_key is None, need consumer_routing_key')
        elif consumer_routing_key:
            raise ValueError('consumer_exchange is None, need consumer_exchange')
        return ProduceConsume(consumer,
                              self.create_producer(producer_exchange, producer_routing_key,
                                                   producer_durable if producer_durable else durable),
                              self.create_consumer if not consumer else None)

    def consume_produce_flow(self, consumer_exchange: str, consumer_routing_key: str,
                             producer_next_exchange: str, producer_next_routing_key: str,
                             producer_error_exchange: str, producer_error_routing_key: str,
                             durable=False, consumer_durable=None,
                             producer_next_durable=None, producer_error_durable=None):
        """
        流服务，用于组成服务流
        1）当服务正常运行无报错时将结果发送至下一个服务的exchange 与 routing_key，
        2）当服务运行异常有报错时将结果发送至收集error的exchange 与 routing_key。
        :param consumer_exchange:
        :param consumer_routing_key:
        :param producer_next_exchange:
        :param producer_next_routing_key:
        :param producer_error_exchange:
        :param producer_error_routing_key:
        :param durable:
        :param consumer_durable:
        :param producer_next_durable:
        :param producer_error_durable:
        :return:
        """
        return ConsumeProduceFlow(self.create_consumer(consumer_exchange, consumer_routing_key,
                                                       consumer_durable if consumer_durable else durable),
                                  self.create_producer(producer_next_exchange, producer_next_routing_key,
                                                       producer_next_durable if producer_next_durable else durable),
                                  self.create_producer(producer_error_exchange, producer_error_routing_key,
                                                       producer_error_durable if producer_error_durable else durable))
