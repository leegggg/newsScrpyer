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

        self.channel.queue_declare(queue=queue)

        return

    def pop(self):
        respon = self.channel.basic_get(
            queue=self.queue)
        body = respon[2]
        # body = str(body)
        return body

    def push(self, data):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue,
                                   body=data)
        return


def main():
    mqClient = RabbitmqClient(host="172.17.0.1")
    # mqClient.push("test_message")
    print(mqClient.pop())


if __name__ == "__main__":
    main()
