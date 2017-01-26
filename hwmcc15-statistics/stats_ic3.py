#!/usr/bin/python
# works for ic3 log files

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
  
  report_file=open(src+'_statistics.csv', 'wb')
  report = csv.writer(report_file, delimiter=',',
     quotechar='|', quoting=csv.QUOTE_MINIMAL)

  report.writerow(['file_name', '#timeframe', '#clause', '#total_calls', '#ctg', 'result', 'time']) 

  for line in lines:
    if status_file_name.search(line):
      list_of_words = line.split()
      search_word="processing"
      f_name = list_of_words[list_of_words.index(search_word) + 1] 
    if status_timeframe.search(line):
      list_of_words = line.split()
      search_word="="
      timeframe = list_of_words[list_of_words.index(search_word) + 1] 
    if status_clauses.search(line):
      list_of_words = line.split()
      search_word="is"
      clauses = list_of_words[list_of_words.index(search_word) + 1] 
    if status_solvers.search(line):
      cols=line.split(':')
      str1=cols[1].lstrip()
      solver=str1.split(' ',1)[0]
    if status_ctg.search(line):
      list_of_words = line.split()
      search_word="#CTGs"
      ctg = list_of_words[list_of_words.index(search_word) + 2]
      ctg = ctg.replace(',', '')
    if status_property.search(line):
      list_of_words = line.split()
      search_word="property"
      result = list_of_words[list_of_words.index(search_word) + 1] 
    if status_time.search(line):
      list_of_words = line.split()
      search_word="is"
      time = list_of_words[list_of_words.index(search_word) + 1] 
    if status_command.search(line):
       report.writerow([f_name,timeframe,clauses,solver,ctg,result,time]) 
       f_name=""
       timeframe=""
       clauses=""
       solver=""
       ctg=""
       result=""
       time=""
    if status_timeout.search(line):
       timeframe="NA"
       clauses="NA"
       solver="NA"
       ctg="NA"
       result="NA"
       time="timeout"
       report.writerow([f_name,timeframe,clauses,solver,ctg,result,time]) 
       timeframe=""
       clauses=""
       solver=""
       ctg=""
       result=""
       time=""
       f_name=""
  
processfile("progress.log-ebmc-ic3")
