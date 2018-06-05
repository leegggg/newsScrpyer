from MqClient import MqClient
import pika


class RabbitmqClient(MqClient):
    connection = None
    channel = None
    queue = ""

    def __init__(self, host="localhost", port=5672,
                 virtual_host="vhost", user="user", passwd="pass",
                 queue="scrpy"):
        self.queue = queue
        credential = pika.credentials.PlainCredentials(
            user, passwd, erase_on_connect=False)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port,
                                      virtual_host=virtual_host,
                                      credentials=credential))

        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=queue, durable=True)

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
        respon = self.channel.basic_get(queue=self.queue, no_ack=True)
        # for respon in self.channel.consume(self.queue):
        #    try:
        #        body = respon[2]
        #        break
        #    except:
        #        pass

        # body = str(body)
        return respon[2]

    def push(self, data):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue,
                                   body=data,
                                   properties=pika.BasicProperties(
                                       delivery_mode=2,  # make message persistent
                                   ))
        return


def main():
    mqClient = RabbitmqClient(host="172.17.0.1")
    mqClient.push("http://news.sina.com.cn/")
    # print(mqClient.pop())


if __name__ == "__main__":
    main()
