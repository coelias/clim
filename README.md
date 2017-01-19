# clim
CoLumn IMproved

* clim is an improved version for the standard *IX column command.

* It is used to create human readable tables from TSV/CSV files.

* It can convert single column files into tables

* It can use regexps for each field extracting only the desired data.

## Installation


```bash
pip install clim
```

Examples:

```bash
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

```
