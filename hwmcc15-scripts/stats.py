#!/usr/bin/python
# works for bmc, bdd, k-induction log files

import sys
import re
import subprocess
import csv

def processfile(src):

  properties=0
  verified_prop=0
  false_prop=0
  inconclusive_prop=0
  timeout_prop=0
  memout_prop=0
  error_prop=0
  sum_runtime=0.0
  sum_peak_memory=0.0
  decisions=0
  propagations=0
  conflicts=0
  conflict_literals=0
  restarts=0

  # temporary variable
  f_name=""
  timeframe=""
  clauses=""
  solver=""
  ctg=""
  result=""
  time=""
  search_word="processing"
  str1=""
   
  file=open(src)
  lines=[line for line in file]
  
  status_file_name = re.compile("Starting to processing") 
  status_timeframe = re.compile("num of time frames = ") 
  status_clauses = re.compile("total number of generated clauses is") 
  status_solvers  = re.compile("all solvers")
  status_ctg = re.compile("#CTGs")
  status_property = re.compile("property")
  status_time = re.compile("total time")
  status_timeout = re.compile("Command timeout")
  status_command = re.compile("Command successful")
  
  report_file=open('statistics.csv', 'wb')
  report = csv.writer(report_file, delimiter=',',
     quotechar='|', quoting=csv.QUOTE_MINIMAL)

  report.writerow(['file_name', 'result']) 

  for line in lines:
    if status_file_name.search(line):
      list_of_words = line.split()
      search_word="processing"
      f_name = list_of_words[list_of_words.index(search_word) + 1] 
    if status_command.search(line):
       result="successful"
       report.writerow([f_name,result]) 
       f_name=""
       result=""
    if status_timeout.search(line):
       result="NA"
       time="timeout"
       report.writerow([f_name,time]) 
       result=""
       f_name=""
  
processfile("progress.log-ebmc-bdd")
