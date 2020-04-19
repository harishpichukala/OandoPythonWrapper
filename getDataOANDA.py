import requests
import pandas as pd
import numpy as np
from datetime import datetime
import json

class TokenAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def generate_API_URL(instrument,count,granularity):
    endpoint="https://api-fxpractice.oanda.com/v3/instruments/{}/candles?count={}&granularity={}&alignmentTimezone=America/New_York".format(instrument,count,granularity)
    return endpoint

def convert_dataframe(j):
    data=[]
    for element in j:
       data.append([element['volume'],element['time'],element['mid']['o'],element['mid']['h'],element['mid']['l'],element['mid']['c']])
    #print(data)
    df = pd.DataFrame(data)
    df.columns = ["Volumne", "Date", "Open", "High","Low","Close"]
    return df
def convert_timestamp(dlist):
    cdlist=[]
    for element in dlist:
        date = datetime.strptime(element,'%Y-%m-%dT%H:%M:%S.%f0000Z')
        print(date)
        timestamp = datetime.timestamp(date)
        cdlist.append(timestamp)
    return cdlist

def convert_timestamp_Date(dlist):
    ctlist=[]
    for element in dlist:
        dt = datetime.fromtimestamp(element)
        ctlist.append(dt)
    return ctlist

def rsiValue(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)
    for i in range(n, len(prices)):
        delta = deltas[i-1]
        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta
        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n
        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)
    return rsi

def main():
    IList=["AUD_CAD"]
    token= "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    for i in IList:
        r=requests.get(generate_API_URL(i,90,'D'),auth=TokenAuth(token))
        if r.status_code is 200:
            data=r.json()
            df=convert_dataframe(data['candles'])
            df['Date']=convert_timestamp(df['Date'])
            df["Close"]=pd.to_numeric(df["Close"])
            closep=df["Close"].to_numpy()
            rsi = rsiValue(closep)
            print(rsi)
            lvalue=rsi[-1]
            if lvalue < 30 or lvalue >70:
                print("Send SMS")

main()
