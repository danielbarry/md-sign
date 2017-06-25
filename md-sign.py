#!/usr/bin/env python

import os
import subprocess
import sys

req_prog =  ["git --version", "pandoc --version", "git status"]
req_check = ["git version",   "Copyright (C)",    "On branch" ]

# main()
#
# Start the main program and parses the command line parameters.
#
# @param args The arguments to the program to be parsed.
def main(args) :
  # Setup initial variables
  in_file = ""
  out_file = ""
  # Iterate of the parameters
  for x in range(0, len(args)) :
    if args[x] == '-h' or args[x] == '--help' :
      display_help()
      continue
    if len(in_file) <= 0 :
      in_file = args[x]
      continue
    if len(out_file) <= 0 :
      out_file = args[x]
      continue
  # Check if we can run the program
  if len(in_file) > 0 and len(out_file) > 0 :
    # Check that required programs are installed
    if check_env() :
      parse_data(in_file, out_file)
    else :
      error("programs not correctly installed")
  return

# display_help()
#
# Display the program's help.
def display_help() :
  print("md-sign [OPT] [<FILE_IN> <FILE_OUT>]")
  print("")
  print("  OPTions")
  print("")
  print("    -h  --help  Display this help")
  print("")
  print("  FILE_IN and FILE_OUT")
  print("")
  print("    FILE_IN   The input Markdown file")
  print("    FILE_OUT  The output HTML file")
  sys.exit()
  return

# parse_data()
#
# Parse the markdown file and sign for the authors.
#
# @param in_file The input file.
# @param out_file The output file.
def parse_data(in_file, out_file) :
  # Initialise buffer
  data = "<table>"
  # Read and split out file
  lines = open(in_file, "r").readlines()
  buff = []
  cont = []
  # Check over the lines
  for x in range(0, len(lines)) :
    # Clean line
    lines[x] = lines[x].replace("\n", "")
    lines[x] = lines[x].replace("\r", "")
    # Check for end of paragraph
    if lines[x] == "" :
      # Remove repeats from authors list
      cont = list(set(cont))
      # Format contributor list
      contributor = ""
      for z in range(0, len(cont)) :
        if z > 0 :
          contributor += "<br>"
        contributor += "<tt>" + cont[z] + "</tt>"
      contributor += "</tt>"
      # Build the markdown into HTML
      tmp = open(".temp.md", "w")
      for z in range(0, len(buff)) :
        tmp.write(buff[z] + "\n")
      run("pandoc .temp.md -o .temp.html")
      html = open(".temp.html", "r").read()
      # Add data to the output buffer
      data += "<tr>"
      data +=   "<td>"
      data +=     contributor
      data +=   "</td>"
      data +=   "<td>"
      data +=     html
      data +=   "</td>"
      data += "</tr>"
      # Reset the collectors
      buff = []
      cont = []
    else :
      # Add the line to the buffer
      buff += [lines[x]]
      blame = run("git blame -L " + str(x + 1) + ",+1 " + in_file)
      cont += [blame.split(' ')[1][1:]]
  data += "</table>"
  open(out_file, "w").write(data)
  # Remove build files
  os.remove(".temp.md")
  os.remove(".temp.html")
  return

# check_env()
#
# Check the environment for whether programs are installed.
#
# @return True if everything is okay, otherwise false.
def check_env() :
  # Try to run our checks
  try :
    # Check for our requirements
    for x in range(0, len(req_prog)) :
      if not req_check[x] in run(req_prog[x]) :
        return False
  except :
    return False
  return True

# run()
#
# Run a program and return it's output.
#
# @param prg The program to be run with it's parameters.
# @return The output from the program.
def run(prg) :
  return subprocess.check_output(prg.split(' '))

# error()
#
# Display error message and quit.
#
# @param msg The message to be displayed.
def error(msg) :
  print("ERROR: " + msg)
  sys.exit()
  return

if __name__ == "__main__" :
  main(sys.argv[1:])
