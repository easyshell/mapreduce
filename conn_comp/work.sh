#!/bin/bash

relation_file=$1
home="hdfs://DEV-m162p111/dev/maoxu.wang/conn_comp"
relation="$home/relation"
across="$home/across"
left="$home/left"
gather="$home/gather"
record="$home/record"

hadoop fs -rm -r $relation
hadoop fs -rm -r $across
hadoop fs -rm -r $record
hadoop fs -mkdir $relation
hadoop fs -mkdir $across
hadoop fs -mkdir $record
hadoop fs -copyFromLocal $relation_file $relation

function mergeset {
	hadoop fs -rm -R -skipTrash $gather
	hadoop jar /opt/hadoop-2.2.0/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar \
	-D stream.num.map.output.key.fields=1 \
	-input $relation \
	-input $across \
	-output $gather \
	-mapper map1.py \
	-reducer reduce1.py \
	-numReduceTasks 20 \
	-file map1.py reduce1.py \
	-cmdenv "bothway=False" 
	if !(hadoop fs -test -d $gather); then
		echo "$(basename $gather) is not gensrate"
		exit 1
	fi
	hadoop fs -rm -R -skipTrash $across
	hadoop fs -mkdir $across
}

function isleftuniq {
	hadoop fs -rm -R -skipTrash $left
	hadoop jar /opt/hadoop-2.2.0/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar \
	-D stream.num.map.output.key.fields=1 \
	-input $gather \
	-output $left \
	-mapper map2.py \
	-reducer reduce2.py \
	-numReduceTasks 1 \
	-file map2.py reduce2.py 
	if !(hadoop fs -test -d $left); then
		echo "$(basename $left) is not gensrate"
		exit 1
	fi
}

function isfinish {
	hadoop fs -rm -R -skipTrash $across
	hadoop jar /opt/hadoop-2.2.0/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar \
	-D stream.num.map.output.key.fields=1 \
	-input $gather \
	-output $across \
	-mapper map3.py \
	-reducer reduce3.py \
	-numReduceTasks 20 \
	-file map3.py reduce3.py 
	if !(hadoop fs -test -d $across); then
		echo "$(basename $across) is not gensrate"
		exit 1
	fi
}

function dirsize {
	dir=$(basename $1)
	hadoop fs -du $1 > $dir""size.txt
	cat $dir""size.txt | awk 'BEGIN{size=0} {size += $1} END{print size}'
}

echo "start main"
round=1
while [ 1 -lt 2 ]; do
	mergeset
	isleftuniq
	if [ $(dirsize $left) == "0" ]; then
		isfinish
		if [ $(dirsize $across) == "0" ]; then
			break
		fi
	fi
	hadoop fs -cp $gather $record/$round 
	hadoop fs -rm -R -skipTrash $relation
	hadoop fs -mv $gather $relation
	round=$(echo "1+$round" | bc)
	echo $round": "$(date +%H:%M:%S) >> log.txt
done

