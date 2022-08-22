# Get the CIK of a ticker from the downloaded cik.csv file
# cik.csv is a tab delimited file with all tickers and CIKs

# imports
import pandas as pd
import os
import yfinance as yf
import json
import csv

# location of cik.csv
cikDir = 'cik.csv'

# read cik.csv as a pandas DataFrame
tkrDF = pd.read_csv(cikDir, delimiter='\t', header=None)
ciksDF = pd.read_csv(cikDir, delimiter='\t', header=None)

# set the column with all the tickers as the index
ciksDF = ciksDF.set_index(0)

# function to return CIK of a ticker
def getCIK(ticker):
    # return CIK if it exists
    try:
        return int(ciksDF.loc[ticker.lower(), 1])
    # return None there's no CIK for the ticker
    except:
        return None

# Check whether the tkrFiles folder exists or not
#   Create folder if it doesn't exist
path = 'tkrFiles/'
isExist = os.path.exists(path)
if(False == isExist):
    os.makedirs(path)

# Setup Data for processing TKRs
allTkrData = {}
allTkrFilterData=[]
start = 1
tkrCt = 1
tkrTotal = len(tkrDF[0])

# Loop through TKRs
for symbol in tkrDF[0]:
    # [Optional] If a specified start number was given, then wait until then to start processing
    if tkrCt >= start:
        # Convert symbol to uppercase
        Symbol = str(symbol).upper()
        print("("+str(tkrCt)+"/"+str(tkrTotal)+") Getting Data for: "+Symbol)
        tkrJson = {}
        tkrData = yf.Ticker(Symbol)
        try:
            # Convert exchange to RO Toolbox friendly
            match(tkrData.info['exchange']):
                case "ASE":
                    tkrJson['exchange'] = "AMEX"
                case "NMS":
                    tkrJson['exchange'] = "NAS"
                case "NYQ":
                    tkrJson['exchange'] = "NYS"
                case _:
                    tkrJson['exchange'] = None
            
            # If an exchange we were familiar with showed up, then contine to process the tkr info
            if(None != tkrJson['exchange']):

                tkrJson['shortName'] = tkrData.info['shortName']
                tkrJson['longName'] = tkrData.info['longName']
                
                # Create a url-friendly name for the BamSEC link
                bsName = tkrJson['longName'].replace(" ", "-")
                bsName = bsName.replace("Inc.", "Inc")
                bsName = bsName.replace("Corp.", "Corp")
                bsName = bsName.replace(".", "-")
                bsName = bsName.replace(",", "")
                bsName = bsName.replace("&-", "")
                bsName = bsName.replace("&", "-")
                bsName = bsName.replace("'", "-")
                bsName = bsName.replace("The-", "")
                bsName = bsName.replace("Corporation", "Co")
                bsName = bsName.lower()
                bsName = bsName.replace("--", "-")
                if ('-' == bsName[-1:]):
                    bsName = bsName + "1"

                tkrJson['cik'] = getCIK(Symbol)
                tkrJson['roURL'] = "https://ruleonetoolbox.com/ticker/" + \
                    tkrJson['exchange']+":"+Symbol+"/company/brief"
                tkrJson['bsURL'] = "https://www.bamsec.com/companies/" + \
                    str(tkrJson['cik'])+"/"+bsName
                allTkrData[Symbol] = tkrJson
                tkrFilterData = [Symbol, tkrJson['shortName'], Symbol]
                allTkrFilterData.append(tkrFilterData)
            else:
                print("\t->Discarding due to the exchange: "+tkrData.info['exchange'])
            
        except:
            print("\t->Discarding due to the exchange: ERROR in tkr.info['exchange']")
        
        tkrCt = tkrCt + 1
        if(0 == (tkrCt %100)):
            # Every 100 TKRs, save data to a specific file in case something happens later down the line
            f = open('tkrFiles/tkrData_'+str(tkrCt)+'.json', "w", encoding="utf8")
            json_data = json.dumps(allTkrData)
            f.write(json_data)
            f.close()
            
            filterCSV = open('tkrFiles/tkrFilter_'+str(tkrCt)+'.csv', 'w')
            writer = csv.writer(filterCSV)
            writer.writerows(allTkrFilterData)
            filterCSV.close()

f = open('tkrData.json', "w", encoding="utf8")
json_data = json.dumps(allTkrData)
f.write(json_data)
f.close()

filterCSV = open('tkrFilter.csv', 'w')
writer = csv.writer(filterCSV)
writer.writerows(allTkrFilterData)
filterCSV.close()


# AMEX = ASE
# NASDAQ = NMS
# NYSE = NYQ


#JNJ
#JPM
#PG
#MA
#HD
#DIS
#KO
#T
#ASML
#MCD
#SAP
#LOW
#BA
#WFC

#RTX
#MS
#AMT
#TD
