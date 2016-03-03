#!/bin/bash
cd `dirname $0`
#ipnumber is the ip number of each /24 subnet e.g. ipnumber=10 represents *.*.*.10
#hopstart is the number that first recommend when traceroute e.g. hopstart=4 represents the first three hop is *
inputfile=$1
subnet=$2
ipnumber=$3
hopstart=$4
echo "command: sh main.sh $1 $2 $3 $4"
echo $(date )"\t start extractorip from cn-allocated-delegated-apnic"
python extractorip.py -f $inputfile -o $subnet".extractorip" -m $subnet -n $ipnumber
echo $(date )"\t start scamper "$subnet".extractorip"

starttime=`date +%s`
##scamper -f ./19.ip -O warts -o ./19.warts -p 500 
scamper -c "trace -f $hopstart" -f $subnet".extractorip" -O warts -o $subnet".warts" -p 800 

endtime=`date +%s`

echo "\t scamper has spent time: "$(((endtime - starttime)/60/60))" hours "$(((endtime - starttime)/60%60))" minutes "$(((endtime - starttime)%60))" seconds"
echo $(date )"\t transfer formate  warts to text"
sc_warts2text $subnet".warts" > $subnet".text"
echo $(date )"\t start count edges with inputfile "$subnet".text"
python countedge.py -f $subnet".text" -o $subnet".result" --route --serial-nodes
echo $(date )"\t end"
exit
