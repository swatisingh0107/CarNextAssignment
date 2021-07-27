FROM puckel/docker-airflow:latest

USER root
RUN whoami
RUN apt-get update
RUN apt-get install sudo
RUN apt-get install -y wget

RUN apt-get update \
 && apt-get install -y locales \
 && dpkg-reconfigure -f noninteractive locales \
 && locale-gen C.UTF-8 \
 && /usr/sbin/update-locale LANG=C.UTF-8 \
 && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
 && locale-gen \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Users with other locales should set this in their derivative image
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN mkdir -p /usr/share/man/man1
# JAVA
RUN apt-get update && apt-get install -y software-properties-common \
&& add-apt-repository  'deb http://security.debian.org/debian-security stretch/updates main'\
&& apt-get update\
&& apt-get install -y openjdk-8-jre\
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*



#RUN apk add --no-cache bash openjdk8-jre
# Define commonly used JAVA_HOME variable
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

# Install Hadoop
ENV HADOOP_VERSION=2.7.3
ENV HADOOP_HOME /opt/hadoop-$HADOOP_VERSION

ENV HADOOP_CONF_DIR=$HADOOP_HOME/conf
ENV PATH $PATH:$HADOOP_HOME/bin
RUN mkdir -p $HADOOP_HOME
RUN curl -sL \
"https://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz" \
| gunzip \
| tar -x -C /opt/ \
&& rm -rf $HADOOP_HOME/share/doc \
&& chown -R root:root $HADOOP_HOME \
&& mkdir -p $HADOOP_HOME/logs \
&& mkdir -p $HADOOP_CONF_DIR \
&& chmod 777 $HADOOP_CONF_DIR \
&& chmod 777 $HADOOP_HOME/logs
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
RUN hadoop fs -mkdir -p /hdfs/carnext-data-engineering-assignment/raw
RUN hadoop fs -mkdir -p /hdfs/carnext-data-engineering-assignment/cleased




# Install Spark
ENV SPARK_VERSION=2.3.1
ENV SPARK_HOME=/opt/spark-$SPARK_VERSION-bin-hadoop2.7
ENV SPARK_CONF_DIR=$SPARK_HOME/conf
ENV PATH $PATH:$SPARK_HOME/bin
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/build:$PYTHONPATH
ENV PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH
RUN mkdir -p $SPARK_HOME

RUN curl -sL \
"https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop2.7.tgz" \
| gunzip \
| tar -x -C /opt/ \
&& chown -R root:root $SPARK_HOME \
&& mkdir -p /data/spark/ \
&& mkdir -p $SPARK_HOME/logs \
&& mkdir -p $SPARK_CONF_DIR \
&& chmod 777 $SPARK_HOME/logs
RUN echo $pwd
#Add JDBC Driver

RUN wget "https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.11/mysql-connector-java-8.0.11-sources.jar" -O $SPARK_HOME/jars/mysql-connector-java-8.0.11.jar
#&& unzip tmp/mysql-connector-java-commercial-5.1.7-bin.jar.zip -d $SPARK_HOME/jars \
#&& rm tmp/mysql-connector-java-commercial-5.1.7-bin.jar.zip





COPY requirements.txt /usr/local/airflow/
RUN pip install -r /usr/local/airflow/requirements.txt
USER $USERNAME
RUN whoami
EXPOSE 22
EXPOSE 4040
EXPOSE 9083
EXPOSE 10000

CMD ["bin/spark-class", "org.apache.spark.deploy.master.Master"]