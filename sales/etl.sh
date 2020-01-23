#!/bin/sh
$PATH:/usr/local/bin
export PATH

cd /home/jeenal/etl/etl/sales
#activate virtual env
. ../../venv/bin/activate

dt=$(date '+%d/%m/%Y %H:%M:%S');
echo "Execution Start At : $dt"
python sales_data_fetch_interm.py
dt=$(date '+%d/%m/%Y %H:%M:%S');
echo "Execution End At : $dt"
