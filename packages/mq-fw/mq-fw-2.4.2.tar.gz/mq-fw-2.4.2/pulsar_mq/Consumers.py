# -*- coding: UTF-8 -*-
# @Time : 2021/11/27 下午5:36 
# @Author : 刘洪波
from concurrent.futures import ThreadPoolExecutor
from pulsar_mq.ConsumerType import get_consumer_type


class Consumer(object):
    def __init__(self, client, topic, consumer_name, schema, consumer_type):
        self.consumer = client.subscribe(topic, consumer_name, schema=schema,
                                         consumer_type=get_consumer_type(consumer_type))

    def receive(self, task, thread_count=None, logger=None):
        """
        :param task: 任务程序
        :param thread_count: 指定最大线程数
        :param logger: 日志收集器
        :return:
        """
        if thread_count:
            """多线程处理"""
            pool = ThreadPoolExecutor(max_workers=thread_count)
            while True:
                msg = self.consumer.receive()
                self.consumer.acknowledge(msg)
                pool.submit(self._acknowledge, task, msg, logger)
        else:
            """消费一个，处理一个"""
            while True:
                msg = self.consumer.receive()
                self.consumer.acknowledge(msg)
                self._acknowledge(task, msg, logger)

    def receive_one(self, task, logger=None):
        """
        只消费处理一个
        :param task:
        :param logger:
        :return:
        """
        msg = self.consumer.receive()
        self.consumer.acknowledge(msg)
        self._acknowledge(task, msg, logger)
        self.consumer.close()

    @staticmethod
    def _acknowledge(task, msg, logger):
        try:
            task(msg.value())
        except Exception as e:
            # 消息未被成功处理
            if logger:
                logger.error('消费异常，报错信息如下：')
                logger.error(e)
            else:
                print('消费异常，报错信息如下：')
                print(e)

    def unsubscribe(self):
        """取消订阅，并关闭消费者"""
        self.consumer.unsubscribe()

    def close(self):
        """关闭消费者"""
        self.consumer.close()
