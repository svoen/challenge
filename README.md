# Doodle Data Engineer Callenge


## How to build and runn!

Install Java JDK if it is not already installed (Homebrew)
```
 brew tap adoptopenjdk/openjdk
 brew cask install adoptopenjdk8
```
Install on OS X Kafka and Zookeeper also very comfortable with homebrew.
Open a terminal window and enter the following.
```
 Brew install kafka
```
(This command installs Zookeaper and Kafka. Nice!)

When Kafka and Zookeeper are installed, open 2 terminal windows and start the Kafka and Zookeeper server with the following commands
Zookeeper:
```
 zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties
```
Kafka:
```
 kafka-server-start /usr/local/etc/kafka/server.properties
```
Leave the two terminal windows open and open 2 more to create the Kafka topics
(in my case 1: Doodle, 2: UID_INFO)

1:
```
 kafka-console-producer --broker-list localhost:9092 --topic Doodle
```
2:
```
 kafka-console-producer --broker-list localhost:9092 --topic UID_INFO
```
the next step is to produce the json file as a message into the kafka ecosystem using Kafka console producer. To do this in the terminal window where we created the topic Doodle, just type the following command
```
 gzcat stream.gz | kafka-console-producer --broker-list localhost:9092 --topic Doodle
```
Then open a last terminal window and start a consumer to the topic UID_INFO with the following command
```
 kafka-console-consumer --bootstrap-server localhost:9092 --topic IUD_INFO
```
Your machine should now have 5 terminal windows open:
1: Zookeeperserver
2: Kafkaserver
3: UID_INFO (created topic)
4: Doodle Producer
5: UID_CONSUMER

Next step ist o install kafka-python by running following command.
```
 pip install kafka-python 
```
To receive and analyze the information of the doodleproducer in a small application just execute the python script analyst.py. It serves as consumer for the doodleproducer. The script extracts the users per minute and sends the extracted information back to kafka as a stream. Thus the script acts as a consumer and producer


## Report:

I decided to use Python because I currently had to deal more often with python than with java.
The idea is to receive the stream, extract the information of interest and pack it into a list.  To get the information users per minute from this list I used a double ended queue structure to ensure that only the time period of one minute is considered. (if something comes in front something goes out behind)
A disadvantage of this solution is that it delivers a usable statement only after a running time of one minute.
I have decided that the information user per minute immediately go live again to get as little delay as possible.

Unfortunately, I did not have time (8 hours) to take care of the delay (source error) of 5 seconds in 99.9% of all cases mentioned in the task definition.
In addition, I made a logic error - my solution counts all users and not the unique users per minute.


## If I had more time.

Consideration of the source error by adjusting the received ts values by an averaged error constant.
Consideration of the unuque users by means of e.g. a set (Python), which ensures that only unique values are included in the set


## Answerd questions:

Different time frames by ontime parcing a json?
I would solve it with a loop and several conditions

App crash?
If the app crashed I could imagine a potential solution would be that all processed data would be considered processed or not by means of an identefier. In case of a crash, a second application could be started by the error handling and could start at the right place thanks to the identefier
