from MqClient import MqClient
import pika


class RabbitmqClient(MqClient):
    connection = None
    channel = None
    queue = ""
    maxPriority = 9
    defaultLevel = 5
    maxLevel = 6

    def getPriority(self, level, priorityOffset):
        priority = self.maxPriority - level + priorityOffset
        if priority > self.maxPriority:
            priority = self.maxPriority
        if priority < 0:
            priority = 0

        return priority

    def __init__(self,
                 host="localhost",
                 port=5672,
                 virtual_host="vhost",
                 user="user",
                 passwd="pass",
                 queue="scrpy"):
        self.queue = queue
        credential = pika.credentials.PlainCredentials(
            user, passwd, erase_on_connect=False)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port,
                virtual_host=virtual_host,
                credentials=credential))

        self.channel = self.connection.channel()
        queueArgument = {"x-max-priority": self.maxPriority + 1}
        self.channel.queue_declare(
            queue=queue, durable=True, arguments=queueArgument)

        return

    # def pop(self):
    #     respon = ""

    #     def on_message(channel, method_frame, header_frame, body):
    #         respon = body
    #         channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    #         channel.stop_consuming()
    #         return respon

    #     self.channel.basic_consume(
    #         consumer_callback=on_message, queue=self.queue)

    #     self.channel.start_consuming()
    #     return respon

    # def pop(self):
    #    body = None
    #    for respon in self.channel.consume(self.queue):
    #        try:
    #            body = respon[2]
    #            break
    #        except:
    #            pass

    #    # body = str(body)
    #    return body

    def pop(self):
        import json
        respon = self.channel.basic_get(queue=self.queue, no_ack=True)
        task = {}
        if not respon[0] is None:
            priority = self.maxPriority - self.defaultLevel
            try:
                priority = respon[1].priority
            except:
                pass
            data = respon[2]
            task = json.loads(data)
            task["priority"] = priority
        return task

    def push(self, task):
        import json
        data = json.dumps(task)

        priority = self.getPriority(
            level=task.get("level"), priorityOffset=task.get("priorityOffset"))
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            body=data,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
                priority=priority))
        return


def main():
    # mqClient = RabbitmqClient(host="172.17.0.1")
    #mqClient = RabbitmqClient(host="rabbitmq.news.linyz.net")
    mqClient = RabbitmqClient("rabbitmq.news.linyz.net")
    import logging
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")
    import sys
    task = {
        "url": "http://news.sina.com.cn/",
        "level": 0,
        "maxLevel": 5,
        "priorityOffset": 0,
        "type": "defaultWeb"
    }

    if len(sys.argv) >= 3:
        url = sys.argv[1]
        level = int(float(sys.argv[2]))
        logging.critical("[{}]{}".format(level, url))
        task["level"] = level
        task["url"] = url
        mqClient.push(task)
        return

    if len(sys.argv) == 2:
        level = 0
        with open(sys.argv[1]) as f:
            for url in f:
                url = url.strip()
                logging.critical("[{}]{}".format(level, url))
                task.update("level", level)
                task.update("url", url)
                mqClient.push(task)
        return

    mqClient.push(task)
    #print(mqClient.pop())


if __name__ == "__main__":
    main()
