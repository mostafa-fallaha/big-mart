#!/bin/bash
cd '/home/mostafa/Desktop/FSD Projects/big_mart'
dvc add dags/data/dvc_df.csv
dvc add dags/data/df.csv
git add .
git commit -m "add data"
dvc push
git push

# continue the process to add training model and these stuffw