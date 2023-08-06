# -*- coding: UTF-8 -*-
# @Time : 2021/11/28 上午12:03 
# @Author : 刘洪波
import pulsar
from pulsar_mq.Consumers import Consumer
from pulsar_mq.Producers import Producer
from pulsar_mq.Services import ConsumeProduce, ProduceConsume, ConsumeProduceFlow
from pulsar_mq.Schema import StringSchema


class Client(object):
    def __init__(self, url: str):
        self.client = pulsar.Client(url)

    def create_consumer(self, topic, consumer_name: str, schema=StringSchema(), consumer_type='Shared'):
        """
        创建 消费者
        :param topic
        :param consumer_name: 消费者名字
        :param schema: 详情见 pulsar_mq.Schema
        :param consumer_type: 详情见 pulsar_mq.ConsumerType
        :return:
        """
        return Consumer(self.client, topic, consumer_name, schema, consumer_type)

    def create_producer(self, topic: str, schema=StringSchema()):
        """
        创建生产者
        :param topic: topic
        :param schema: 详情见 pulsar_mq.Schema
        :return:
        """
        return Producer(self.client, topic, schema)

    def consume_produce(self, consumer_topic, consumer_name: str, producer_topic=None,
                        schema=StringSchema(), consumer_type='Shared'):
        """
        服务端
        pulsar 消费数据后 并且发送数据的 服务
        1. 订阅pulsar
        2. 处理消费的数据
        3. 发送得到的结果
        4. 发送的 队列 可以是 随机的
        :param consumer_topic:
        :param consumer_name:
        :param producer_topic:
        :param schema: 详情见 pulsar_mq.Schema
        :param consumer_type: 详情见 pulsar_mq.ConsumerType
        :return:
        """
        return ConsumeProduce(self.client, consumer_topic, consumer_name, consumer_type, producer_topic, schema)

    def produce_consume(self, producer_topic: str, consumer_topic=None, consumer_name=None,
                        schema=StringSchema(), consumer_type='Shared'):
        """
        调用端
        发送数据至pulsar，然后从 pulsar消费数据的服务
        1. 发送数据至pulsar
        2. 订阅pulsar得到业务数据
        3. 消费的 队列 可以是 随机的
        :param producer_topic:
        :param consumer_topic:
        :param consumer_name:
        :param schema: 详情见 pulsar_mq.Schema
        :param consumer_type: 详情见 pulsar_mq.ConsumerType
        :return:
        """
        return ProduceConsume(self.client, producer_topic, consumer_type, consumer_topic, consumer_name, schema)

    def consume_produce_flow(self, consumer_topic: str, consumer_name: str, producer_next_topic: str,
                             producer_error_topic: str, schema=StringSchema(), consumer_type='Shared'):
        """
        流服务，用于组成服务流
        1. 订阅pulsar
        2. 处理消费的数据
        3. 发送业务数据
           1）当服务正常运行无报错时将结果发送至下一个服务的topic，
           2）当服务运行异常有报错时将结果发送至收集error的topic。
        4. 发送的 队列只能是固定的
        :param producer_next_topic: 下一个服务的 topic
        :param producer_error_topic: 当服务报错时 将错误信息发送至的 topic
        :param consumer_topic:
        :param consumer_name:
        :param schema: 详情见 pulsar_mq.Schema
        :param consumer_type: 详情见 pulsar_mq.ConsumerType
        :return:
        """
        return ConsumeProduceFlow(self.client, consumer_topic, consumer_name, consumer_type,
                                  producer_next_topic, producer_error_topic, schema)

    def close(self):
        """
        关闭 client
        :return:
        """
        self.client.close()
