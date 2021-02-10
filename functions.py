import khayyam 
import datetime
import pandas as pd

df=pd.read_excel('data1.xlsx')
df.index +=1
df.drop(['name','floor'],inplace=True,axis=1)
df.columns=['vahed','tedad_sakenin','masahat','tedad_parking']

# for understanding the category
def sub_cat(a):
        if a[2]=='bill':
            return a[3];
        else:
            return a[2];
# equal division
def e(a,i):
    return 1/df.vahed.count()*int(a[1]);
# division based on resident 
def r(a,i):
    return df.loc[i,'tedad_sakenin']/df.tedad_sakenin.sum()*int(a[1]);
#  division based on area 
def s(a,i):
    return df.loc[i,'masahat']/df.masahat.sum()*int(a[1]);
# division based on parking 
def p(a,i):
    return df.loc[i,'tedad_parking']/df.tedad_parking.sum()*int(a[1]);
# division based on percent of each unit 
def percent(a : list):
    global df_transaction
    percentage=input('enter the percentage share of each unit: ').split('-')
    for i in range(1,df.vahed.count()+1):
        if z[0]=='now':
              time=str(khayyam.JalaliDate.today())
        else:
            time=z[0]
               
        amount=int(percentage[i-1])*int(z[1])/100
        category=sub_cat(z)
        rel_unit=i
        res_unit=z[5]
        df_append=pd.DataFrame([[time,amount,category,rel_unit,res_unit]],columns=['time','amount','category','related_unit','resposible_unit'])           
        df_transaction=df_transaction.append(df_append,ignore_index=True)  
# a function that realises which type of division must be used
def operation(a,i):
    if a[4]=='d':
        if sub_cat(a) in ['water','electricity']:
            return r(a,i)
        elif sub_cat(a) in ['city_hall','elevator','cleaning','repairing','charge','others']:
            return e(a,i)
        elif sub_cat(a)=='parking':
            return p(a,i)
        elif sub_cat(a)=='gas':
            return s(a,i)               
    else:
        if a[4]=='r':
            return r(a,i)
        if a[4]=='s':
            return s(a,i)
        if a[4]=='p':
            return p(a,i)
        if a[4]=='e':
            return e(a,i)
# for announcing the codition of budget        
def budget(df_transaction,a):
    budget=df_transaction[df_transaction['category']=='charge'].amount.sum()-df_transaction[df_transaction['category']!='charge'].amount.sum()
    if budget<=-a:
        print('your budget is :')
        print(budget)
        print('codition is red')
    elif (budget>-a/2) & (budget<0):
        print('your budget is :')
        print(budget)
        print('codition is yellow')
    else:
        print('your budget is :')
        print(budget)
        print('codition is green')