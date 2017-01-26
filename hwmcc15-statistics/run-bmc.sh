$MYDIR=`pwd`
TIMEOUT=600
TOOL=ebmc-bmc
BENCHMARKLIST=`cat benchmarks.txt`
PWD=`pwd`
PROGRESSLOG=${PWD}/progress.log-${TOOL}
LOG=${PWD}/log-${TOOL}
TEMP=${PWD}/progress.log-tmp-${TOOL}
MODULE="m"
FLAG=1

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
   MODULE=""
   MODULE+=$file
   echo "Module name is $MODULE" >> ${PROGRESSLOG} 
  else  
   file=${file:1}
   MODULE+=$file
   echo "Module name is $MODULE" >> ${PROGRESSLOG}
  fi  
  BOUND=50
  FLAGS="--module $MODULE --bound $BOUND"
  runsolver -C $TIMEOUT -W $TIMEOUT -d 1 -M 32768 ${EXEC} ${FLAGS} $filename > ${LOG}
  
  grep -r 'SUCCESS' ${LOG} >> ${TEMP}
  OUT1=$?
  if [ $OUT1 -eq 0 ];then
    echo "Property Successful" >> ${PROGRESSLOG}
    FLAG=0
  fi
  grep -r 'FAILURE' ${LOG} >> ${TEMP}
  OUT2=$?
  if [ $OUT2 -eq 0 ];then
    echo "Property FAILED" >> ${PROGRESSLOG}
    FLAG=0
  fi
  if [ $FLAG -eq 1 ];then
    grep -r 'runsolver_max_cpu_time_exceeded' ${LOG} >> ${TEMP}
    OUT3=$?
    if [ $OUT3 -eq 0 ];then
      echo "Command TIMEOUT" >> ${PROGRESSLOG}
      pidno=`pidof ebmc`
      echo "Killing process $pidno" >> ${PROGRESSLOG}
      kill -9 $pidno
    fi

    grep -r 'runsolver_max_memory_limit_exceeded' ${LOG} >> ${TEMP}
    OUT4=$?
    if [ $OUT4 -eq 0 ];then
      echo "Command MEMORY OUT" >> ${PROGRESSLOG}
      pidno=`pidof ebmc`
      echo "Killing process $pidno" >> ${PROGRESSLOG}
      kill -9 $pidno
    fi
    
    grep -r 'Maximum wall clock time exceeded' ${LOG} >> ${TEMP}
    OUT5=$?
    if [ $OUT5 -eq 0 ];then
      echo "Command TIMEOUT" >> ${PROGRESSLOG}
      pidno=`pidof ebmc`
      echo "Killing process $pidno" >> ${PROGRESSLOG}
      kill -9 $pidno
    fi
  fi
  echo "done at `date`" >> ${PROGRESSLOG}
  file=""
  MODULE="m"
  OUT1=""
  OUT2=""
  OUT3=""
  OUT4=""
  FLAG=1
  pidno=""
done
