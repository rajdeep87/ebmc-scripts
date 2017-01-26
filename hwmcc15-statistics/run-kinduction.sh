$MYDIR=`pwd`

TOOL=ebmc-kinduction
BENCHMARKLIST=`cat benchmarks.txt`
PWD=`pwd`
PROGRESSLOG=${PWD}/progress.log-${TOOL}
TEMP=${PWD}/progress.log-tmp-${TOOL}
MODULE="m"

EXEC=/users/rajdeep/hw-cbmc/trunk/src/ebmc/ebmc
echo "Starting experiments at `date` on `hostname`" > ${PROGRESSLOG}
for FILE in $BENCHMARKLIST
do
  filename=${FILE}
  echo "Starting to processing $filename at `date`" >> ${PROGRESSLOG}
  file=$(echo $FILE | cut -d'.' -f 1)
  # extract first letter of filename
  #l=echo "$file" | awk '{print substr($0,0,1)}'
  l=$(echo "$file" | sed 's/\(^.\).*/\1/')
  #echo "The first letter is $l"
  re='^[0-9]+$'
  if ! [[ $l =~ $re ]] ; then
   MODULE+=$file
   echo "Module name is $MODULE" >> ${PROGRESSLOG} 
  else  
   file=${file:1}
   MODULE+=$file
   echo "Module name is $MODULE" >> ${PROGRESSLOG}
  fi  
  BOUND=1
  FLAG=0
  while [[ $FLAG -le 0 ]] && [[ $BOUND -le 50 ]]; do
    FLAGS="--k-induction --module $MODULE --bound $BOUND"
    # echo "Starting to processing $filename at `date`" >> ${PROGRESSLOG}
    timeout 600s ${EXEC} ${FLAGS} $filename >> ${PROGRESSLOG}
    OUT=$?
    if [ $OUT -eq 124 ];then
      echo "Command timeout" >> ${PROGRESSLOG}
      FLAG=1
    elif [ $OUT -eq 0 ];then
      # check PROGRESSLOG for UNKNOWN
      sed -e '$!d' ${PROGRESSLOG} | grep 'UNKNOWN' >> ${TEMP}  
      OUT1=$?
      if [ $OUT1 -eq 0 ];then
       BOUND=`expr $BOUND + 1`
      else  
       echo "Command successful" >> ${PROGRESSLOG}
       FLAG=1
      fi 
    fi
  done
  echo "done at `date`" >> ${PROGRESSLOG}
  file=""
  MODULE="m"
done
