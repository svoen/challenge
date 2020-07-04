
import datetime
from collections import deque
from kafka import KafkaConsumer
from kafka import KafkaProducer
import json


class Analyst(object):
    def __init__(self):
        self.uid_last_min = deque()
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.consumer = KafkaConsumer('Doodle', bootstrap_servers=['localhost:9092'], auto_offset_reset="earliest", value_deserializer=lambda m: json.loads(m.decode('utf-8')))


    def evt_p_min(self):
        while self.uid_last_min[0][0] < datetime.datetime.now() - datetime.timedelta(seconds=60):
            self.uid_last_min.popleft()

        min_rate = len(set([e[1] for e in  self.uid_last_min]))
        #print(min_rate)
        self.producer.send('UID_INFO',  {"unique_uid_per_min": str(min_rate)})


    def get_stream(self):
        while True:
            msg_pack = self.consumer.poll(timeout_ms=500)
            for topic, messages in msg_pack.items():
                for msg in messages:
                    if msg.value["ts"]:
                        #print(msg.value["uid"])
                        self.uid_last_min.append((datetime.datetime.now(), msg.value["uid"],msg.value["ts"]))
                        self.evt_p_min()


if __name__ == '__main__':

    counter = Analyst()
    counter.get_stream()

