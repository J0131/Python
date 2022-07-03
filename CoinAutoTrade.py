import time
import pyupbit
import datetime

avail=[]
avail_buy_list=[]
buy_tricker=[]
access = "본인의 access 코드"
secret = "본인의 secret 코드"
buy_count = 0
sell_count = 0
krw_count = 0
krw_count2 = 0

# 로그인
upbit = pyupbit.Upbit(access, secret)[p]
print("autotrade start")

tricker = pyupbit.get_tickers(fiat="KRW")
avail_tricker = ["KRW-BTC","KRW-ETH","KRW-NEO","KRW-MTL","KRW-LTC","KRW-XRP","KRW-ETC",
"KRW-OMG","KRW-SNT","KRW-WAVES"]

df_ex = pyupbit.get_ohlcv("KRW-BTC", interval="day", count=1)
start_time = df_ex.index[0]

real_krw=upbit.get_balance("KRW")
#buy_krw = real_krw*0.2495

balance = upbit.get_balances()
for k in range(0,len(balance)):
    if balance[k]['currency'] == "KRW" or balance[k]['currency'] == "APENFT":
                continue
    buy_tricker.append("KRW-" + balance[k]['currency'])
    buy_count += 1
    krw_count += 1
    
# 하루에 최대 4종목만 거래함
if krw_count == 0:
    buy_krw = real_krw*0.2495
elif krw_count == 1:
    buy_krw = real_krw/3-0.0005
elif krw_count == 2:
    buy_krw = real_krw/2-0.0005
elif krw_count == 3:
    buy_krw = real_krw/1-0.0005

if buy_krw < 5025:
    sell_count = 4-buy_count
    buy_count = 4


print(len(balance))
print("buy_count : %d" % buy_count)
print("sell_count : %d" % sell_count)
print(buy_tricker)

while True:
    
    for i in tricker:
        print(i)
        print(pyupbit.get_current_price(i))
        df = pyupbit.get_ohlcv(i,count=4)
        close = df['close']
        print(close[2])
        time.sleep(0.1)

        # 전날 종가에 비해 1% 상승했을 때 그 종목 매수
        if pyupbit.get_current_price(i)>=1.009*close[2] and pyupbit.get_current_price(i)<=1.011*close[2] and (i in buy_tricker)!=True:
            avail_buy_list.append(i)
            krw=upbit.get_balance("KRW")
            if  krw>=5025 and buy_count<4:
                upbit.buy_market_order(i,buy_krw)
                print('buy: %s' % i) 
                buy_count += 1
                buy_tricker.append(i)

        # avail.append(i)
        # 전날 종가에 비해 2% 상승했을 때 그 종목 매도
        coin = upbit.get_balance(i)
        if pyupbit.get_current_price(i)>=1.021*close[2] and coin>0:
            if upbit.sell_market_order(i,coin) != None:
                print('sell: %s' % i) 
                sell_count += 1
                buy_tricker.remove(i)
            else:
                print('cant sell(잔액부족): %s' % i) 
                sell_count += 1
                buy_tricker.remove(i)
        time.sleep(0.1)

    while buy_count>=4:
        for l in buy_tricker:
           
            print(l)
            print(pyupbit.get_current_price(l))
            df = pyupbit.get_ohlcv(l,count=4)
            close = df['close']
            print(close[2])
            time.sleep(0.1)
            coin = upbit.get_balance(l)
            if pyupbit.get_current_price(l)>=1.02*close[2] and coin>0:
                if upbit.sell_market_order(l,coin) != None:
                    print('sell: %s' % l) 
                    sell_count += 1
                    buy_tricker.remove(l)
                else:
                    print('cant sell(잔액부족): %s' % l) 
                    sell_count += 1
                    buy_tricker.remove(l)
            time.sleep(0.1)
        print("buy_count : %d" % buy_count)
        print("sell_count : %d" % sell_count)
        print(buy_tricker)
        
        if sell_count >= 4  or start_time + datetime.timedelta(days=1) >= datetime.datetime.now():
            break
        #print(upbit.get_balances())


    if start_time + datetime.timedelta(days=1) < datetime.datetime.now():

        buy_count=len(buy_tricker)
        krw_count2 = len(buy_tricker)
        sell_count=0
        start_time = start_time + datetime.timedelta(days=1)
        real_krw=upbit.get_balance("KRW")
        #buy_krw = real_krw*0.2495


        if krw_count2 == 0:
            buy_krw = real_krw*0.2495
        elif krw_count2 == 1:
            buy_krw = real_krw/3-0.0005
        elif krw_count2 == 2:
            buy_krw = real_krw/2-0.0005
        elif krw_count2 == 3:
            buy_krw = real_krw/1-0.0005

    
    print("buy_count : %d" % buy_count)
    print("sell_count : %d" % sell_count)
    print(buy_tricker)

#print(avail_buy_list)
#print(df.index[0])
