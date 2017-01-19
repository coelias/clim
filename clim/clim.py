#!/usr/bin/python

HELP='''
clim - CoLumn IMproved by Carlos del Ojo Elias (deepbit@gmail.com)

* clim is an improved version for the standard *IX column command.

* It is used to create human readable tables from TSV/CSV files.

* It can convert single column files into tables

* It can use regexps for each field extracting only the desired data.

Examples:

  - file1 (tab separated):
    col1 col2 col3 col4
    1 2 3 4
    5 6 7 8


      # if separator is something different than tab (eg ,)
      # replace -t by -s,

      $ clim -t file1
      col1 col2 col3 col4
      1    2    3    4
      5    6    7    8

      $ clim -t -f file1
      | col1 | col2 | col3 | col4 |
      | 1    | 2    | 3    | 4    |
      | 5    | 6    | 7    | 8    |
      =============================

      $ clim -t -f -hd1 file1
      =============================
      | col1 | col2 | col3 | col4 |
      =============================
      | 1    | 2    | 3    | 4    |
      | 5    | 6    | 7    | 8    |
      =============================

      $ clim -t -f -hd name,address,age,height file1
      ==================================
      | name | address | age  | height |
      ==================================
      | col1 | col2    | col3 | col4   |
      | 1    | 2       | 3    | 4      |
      | 5    | 6       | 7    | 8      |
      ==================================

      $ clim -t -d "-NEWSEP-" file1
      col1-NEWSEP-col2-NEWSEP-col3-NEWSEP-col4
      1-NEWSEP-2-NEWSEP-3-NEWSEP-4
      5-NEWSEP-6-NEWSEP-7-NEWSEP-8

      $ clim -t -f -j ">" file1
      | col1 | col2 | col3 | col4 |
      |    1 |    2 |    3 |    4 |
      |    5 |    6 |    7 |    8 |
      =============================

      $ clim -t -f -j ">" file1
      | col1 | col2 | col3 | col4 |
      |    1 |  2   | 3    |  4   |
      |    5 |  6   | 7    |  8   |
      =============================

  - file2:
    1
    2
    3
    4
    5
    6

      $ clim -c2 -f file2
      | 1 | 2 |
      | 3 | 4 |
      | 5 | 6 |
      =========

  - file3:
    1
    2
    log: two lines printed
    3
    log: three lines printed
    4
    5
    log: five lines printed
    6

      $ clim -c2 -f -ir '^log:' file3
      | 1 | 2 |
      | 3 | 4 |
      | 5 | 6 |
      =========

  - file4:
    name: john
    surname: smith
    age: 43
    weight: 72
    name: mary
    surname: wallace
    age: 38
    weight: 86

      $ clim -c4 -f -hd name,surname,age,weight -fr ';\S+$;\S+$;\S+$;\S+$' file4
      =================================
      | name | surname | age | weight |
      =================================
      | john | smith   | 43  | 72     |
      | mary | wallace | 38  | 86     |
      =================================


'''

import argparse
import sys
import re
from itertools import *

def flattern(l):
    res = []
    for i in l:
        if type(i) == str:
            res.append(i)
        else:
            res.extend(flattern(i))
    return res

class TextColumns:
    def __init__(self,buflen=1024*1024, sep=None, columns=0,frame=False,headers=[],hd1=False,fieldregex=None,ignoreregex=None,justify='<', out_delim=None):
        assert (sep and columns) or sep or columns
        self.buffering = True
        self.buffer = []
        self.buflen = buflen
        self.columns = columns
        self.sep = sep
        self.current_row = []
        self.field_sizes = []
        self.frame = frame
        self.printed = 0
        self.headers = headers
        self.hd1 = hd1
        self.out_delim = out_delim

        if self.headers:
            self.field_sizes = [len(i) for i in self.headers]

        assert all([i in '<>-' for i in justify]),'Justify character must be either < or > or -'
        self.justify = [{'<':str.ljust,'>':str.rjust,'-':str.center}[i] for i in justify]

        if ignoreregex:
            self.ignore_regex = re.compile(ignoreregex)
        else:
            self.ignore_regex = None

        if fieldregex:
            fieldregex = fieldregex[1:].split(fieldregex[0])
            self.field_regex = []
            for i in fieldregex:
                if i:
                    self.field_regex.append(re.compile(i))
                else:
                    self.field_regex.append(None)
        else:
            self.field_regex = None



    def process(self,inp):
        current = 0
        for line in inp:
            line = line.strip()
            self.append(line)
            current += len(line)
            if current > self.buflen:
                self.buffering = False
                break

        self.workout_format()
        self.dump_buffer()

        for line in inp:
            line = line.strip()
            self.append(line)


    def append(self, line):
        if self.sep:
            data = line.split(self.sep)
        else:
            data = [line]

        if not self.columns:
            self.process_row(data)
        else:
            if self.ignore_regex:
                data=[i for i in data if not self.ignore_regex.findall(i)]

            self.current_row.extend(data)

            while len(self.current_row) >= self.columns:
                row,self.current_row=self.current_row[:self.columns],self.current_row[self.columns:]
                self.process_row(row)

    def process_row(self,row):
        if self.field_regex:
            for pos, val, regex in izip(count(), row, self.field_regex):
                if not regex: 
                    continue
                res = regex.findall(val)
                if res:
                    row[pos] = ' '.join(flattern(res))

        if self.buffering:
            self.buffer.append(row)
        else:
            self.print_row(row)


    def workout_format(self):
        for i in chain(self.buffer, [self.current_row]):
            for pos, value in enumerate(i):
                if len(self.field_sizes) < pos+1:
                    self.field_sizes.append(len(value))
                else:
                    self.field_sizes[pos] = max(self.field_sizes[pos], len(value))


    def dump_buffer(self):
        for i in self.buffer:
            self.print_row(i)

    def print_horizline(self):
        print (-3+sum(self.field_sizes)+3*len(self.field_sizes)+4)*'='

    def finish(self):
        if self.current_row:
            self.print_row(self.current_row)
        if self.frame:
            self.print_horizline()


    def print_row(self,row):
        if not self.printed and self.hd1 and self.frame:
            self.print_horizline()

        if not self.printed and self.headers:
            if self.frame:
                self.print_horizline()
            self.printed += 1
            self.print_row(headers)
            if self.frame:
                self.print_horizline()

        row2 = []
        for pos, val in enumerate(row):
            if pos+1 > len(self.field_sizes):
                size = 20
            else:
                size = self.field_sizes[pos]
            if len(val) > size:
                val = val[:size-4]+" ..."

            if len(self.justify) == 1:
                row2.append(self.justify[0](val, size, ' '))
            elif len(self.justify) < pos+1:
                row2.append(str.ljust(val, size, ' '))
            else:
                row2.append(self.justify[pos](val, size, ' '))

        if self.out_delim:
            print (self.out_delim.join([j.strip() for j in row2]))
        elif not self.frame:
            print (' '.join(row2))
        else:
            print ('| '+' | '.join(row2)+' |')


        if not self.printed and self.hd1 and self.frame:
            self.print_horizline()

        self.printed += 1


def main():
    parser = argparse.ArgumentParser(description='',usage=HELP)
    parser.add_argument("-c",dest="columns",help="Force columns, assumes input is all in one column (linear)",required=False,default=0,type=int)
    parser.add_argument("-s",dest="separator",help="input character/string separator (eg: csv/tsv files) (non-linear)",required=False,type=str)
    parser.add_argument("-t",dest="tab_sep",help="input tab-character separator",action='store_true')
    parser.add_argument("-f",dest="frame",help="Print columns and table frame in the output",action='store_true')
    parser.add_argument("-hd",dest="headers",help="Specify headers for the output  (comma sepparated)")
    parser.add_argument("-hd1",dest="hd1",help="Grab headers from the first line",action='store_true')
    parser.add_argument("-fr",dest="fieldregex",help="field regexps: [SEP]regexp1[SEP]regexp2, (eg: ;[a-z]+;^[0-9]+([a-z]+)[0-9]+$;^([0-9]+[a-z]+([0-9]+) )")
    parser.add_argument("-ir",dest="ignoreregex",help="Lines to ignore using regexp (only linear mode)")
    parser.add_argument("-j",dest="justify",help="field justify (<, >, -) (multiple operators accepted, eg: <->>><-)", default='<')
    parser.add_argument("-d",dest="out_delim",help="Output with no format, just delimiter", default=None)


    parser.add_argument('FILE', nargs='?',default="-")
    args = parser.parse_args()

    if args.tab_sep:
        args.separator='\t'

    if not args.columns and not args.separator:
        print ("Either columns or separator must be provided")
        sys.exit(-1)

    if args.headers and args.hd1:
        print ("You can only choose one type of headers")
        sys.exit(-1)

    if args.ignoreregex and (not args.columns or args.tab_sep):
        print ("ignore regexp not compatible with non-linear mode")
        sys.exit(-1)

    if args.FILE == '-':
        INPUT = sys.stdin
    else:
        INPUT = open(args.FILE)

    if args.out_delim:
        if args.frame:
            print ("You cannot specify format when outputting with delimiters")
            sys.exit(-1)
        args.out_delim = args.out_delim.replace('\\t','\t')


    headers=[]
    if args.headers:
        headers=args.headers.split(',')

    a=TextColumns(sep=args.separator,
                  columns=args.columns,
                  frame=args.frame,
                  headers=headers,
                  hd1=args.hd1,
                  fieldregex=args.fieldregex,
                  ignoreregex=args.ignoreregex,
                  justify=args.justify,
                  out_delim=args.out_delim)
    a.process(INPUT)
    a.finish()
