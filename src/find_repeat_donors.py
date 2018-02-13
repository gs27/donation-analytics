#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
this is for donation analytics , Insight challange
Created_by: gurdeep
Creation_dt : Feb 13, 2018.
"""
import numpy as np
import pandas as pd
import datetime as datetime
import sys


class FindRepeatDonors():
    def __init__(self,file):
        #reads and converts the input into a dataframe
        raw_data=open(file).readlines()
        self.data=[line.rstrip() for line in raw_data]
        self.data_df=pd.DataFrame()
        
    def preProcessing(self):
        #declare the empty variable to be used later in the program
        CMTE_ID=[]
        ZIP_CODE=[]
        TRANSACTION_DT=[]
        TRANSACTION_AMT=[]
        OTHER_ID=[]
        TRANSACTION_YEAR=[]
        for line in self.data:
            #remove the pipe-delimiter
            d=line.split("|")
            #check empty or null Committee ID (CMTE_ID)
            #check empty of null Transaction Amount (TRANSACTION_AMT)
            if ((d[0]!="") or (d[0]!=np.nan) or (d[14]!="") or (d[14]!=np.nan)):
                CMTE_ID.append(d[0])
                ZIP_CODE.append(d[10])
                TRANSACTION_DT.append(d[13])
                TRANSACTION_AMT.append(d[14])
                OTHER_ID.append(d[15])
                
                #check for invalid Transaction Date (TRANSACTION_DT). 
                try:
                    x=d[13]
                    year=int(str(x)[4:])
                    month=int(str(x)[0:2])
                    day=int(str(x)[2:4])
                    date1=datetime.datetime(year=year,month=month,day=day)
                    TRANSACTION_DT_FORMAT.append(date1)
                except:
                    pass
           
	      # Identify year of donation
                  data_df['TRANSACTION_YEAR'] = data_df['TRANSACTION_DT']%10000
           
        #processed DataFrame        
        data_df=pd.DataFrame({"CMTE_ID":CMTE_ID ,"ZIP_CODE":ZIP_CODE,\
                               "TRANSACTION_DT":TRANSACTION_DT,\
                               "TRANSACTION_AMT":TRANSACTION_AMT,"OTHER_ID":OTHER_ID,"TRANSACTION_YEAR":TRANSACTION_YEAR})
        #remove Other Identification Number (OTHER_IDs) that are non-empty  
        data_df=data_df[data_df['OTHER_ID']==""]
        #use only first five digits of ZIP_CODE
        data_df['ZIP_CODE']=data_df['ZIP_CODE'].map(lambda x: str(x)[0:5])
        
        return(data_df)
        
    def percentile_by_zip(self,df,zip_output):
         file=open(zip_output,"w")
         data_df=df.copy()
         # Create a dictionary with key as Transaction Date and value as a list of Transaction Amounts
         dic_zips={}
         for index,row in data_df.iterrows():
             CMTE_ID=row['CMTE_ID']
             ZIP_CODE=row['ZIP_CODE']
             TRANSACTION_AMT=row['TRANSACTION_AMT']
             if ZIP_CODE in dic_zips.keys():
                 #if there is a ZIP Code key entry in the dictionary, add the Transaction Amount to the list
                 dic_zips[ZIP_CODE].append(int(TRANSACTION_AMT))
             else:
                 #if no entry in dictionary, add a new ZIP entry in the dictionary and populate the Transaction amount to the list
                 dic_zips[ZIP_CODE]=[]
                 dic_zips[ZIP_CODE].append(int(TRANSACTION_AMT))
                 
                 # Identify duplicate/ return donors
                   df1 = data_df[df.duplicated(subset={'NAME','ZIP_CODE'},keep='first')]
                 
             #write to the output file in the required format    
             
             df['ZIP_CODE'] = df['ZIP_CODE'].apply(lambda x:x[:5])
	             
	             # for cumulative donations
            df1['SUM_AMT'] = df1['TRANSACTION_AMT'].cumsum()
             
	                  percentile_index=(math.ceil((self.percentile/100)*index))-1
             
             file.write("{}|{}|{}|{}|{}\n".format(CMTE_ID,ZIP_CODE,YEAR,df1[TRANSACTION_AMT].iloc[percentile_index],row[CUMSUM],index)
         file.close()   
         return(None)
         
         
    
if __name__ == "__main__":
    #take in first input as input file name
    file=sys.argv[1]
    #second input as output file name 2
    zip_output=sys.argv[2]
    #third input as output file name 3
    date_output=sys.argv[3]
    political_donors=FindRepeatDonors(file)
    #call the cladd FindRepeatDonors and the functions to create the output files
    df=political_donors.preProcessing()
    political_donors.percentile_by_zip(df,zip_output)
