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
  status_property = re.compile("property")
  status_time = re.compile("total time")
  status_timeout = re.compile("Command TIMEOUT")
  status_memout = re.compile("Command MEMORY OUT")
  status_success = re.compile("Property Successful")
  status_failed = re.compile("Property FAILED")
  status_unknown = re.compile("UNKNOWN")
  
  #file_name = 'statistics'+src
  report_file=open(src+'_statistics.csv', 'wb')
  report = csv.writer(report_file, delimiter=',',
     quotechar='|', quoting=csv.QUOTE_MINIMAL)

  report.writerow(['file_name', 'result']) 

  for line in lines:
    if status_file_name.search(line):
      list_of_words = line.split()
      search_word="processing"
      f_name = list_of_words[list_of_words.index(search_word) + 1] 
    if status_success.search(line):
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
    if status_unknown.search(line):
       result="unknown"
       report.writerow([f_name,result]) 
       result=""
       f_name=""
    if status_failed.search(line):
       result="failed"
       report.writerow([f_name,result]) 
       result=""
       f_name=""
    if status_memout.search(line):
       result="memout"
       report.writerow([f_name,result]) 
       result=""
       f_name=""
  
processfile("progress.log-ebmc-kinduction")
