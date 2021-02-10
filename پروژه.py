import khayyam 
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import functions as func

df=pd.read_excel('data1.xlsx')
df.index +=1
df.drop(['name','floor'],inplace=True,axis=1)
df.columns=['vahed','tedad_sakenin','masahat','tedad_parking']

df_transaction=pd.read_csv('transaction.csv')
for i in df_transaction.columns:
    if i not in ['time','amount','category','related_unit','resposible_unit']:
        df_transaction.drop(columns=i, inplace=True)

l=['water','gas','electricity','city_hall','elevator','cleaning','parking','repairing','others']                 
        


while True :
    # be karbar vaziat mojoodi ra neshan midahad
    func.budget(df_transaction,1000)
    
    x=input('enter the command: ')
    
    if x=='exit':
        break
    
    if x=='append':
        y=input('for all or for one? ')
        if y=='for all':
            z0=input('enter the time: ')
            z1=input('enter the amount: ')
            z2=input('enter the category: ')
            z3=input('enter the sub category: ')
            z4=input('enter the type of division: ')
            z5=input('enter the resposible unit: ')
            z=[z0,z1,z2,z3,z4,z5]
            if z[4]=='percent':
                func.percent(z)
            else:
                for i in range(1,df.vahed.count()+1):
                    if z[0]=='now':
                          time=str(khayyam.JalaliDate.today())
                    else:
                        time=z[0]
                            
                    amount=func.operation(z,i)
                    category=func.sub_cat(z)
                    rel_unit=i
                    res_unit=z[5]
                    df_append=pd.DataFrame([[time,amount,category,rel_unit,res_unit]],columns=['time','amount','category','related_unit','resposible_unit'])           
                    df_transaction=df_transaction.append(df_append,ignore_index=True)

        elif y=='for one':
            z0=input('enter the time: ')
            z1=input('enter the amount: ')
            z2=input('enter the category: ')
            z3=input('enter the sub category: ')
            z4=input('enter the related unit: ')
            z5=input('enter the resposible unit: ')
            z=[z0,z1,z2,z3,z4,z5]
            if z0=='now':
                time=str(khayyam.JalaliDate.today())
            else:
                time=z0
                   
            amount=int(z1)
            category=func.sub_cat(z)
            rel_unit=z4
            res_unit=z5
            s=pd.DataFrame([[time,amount,category,rel_unit,res_unit]],columns=['time','amount','category','related_unit','resposible_unit'])           
            df_transaction=df_transaction.append(s,ignore_index=True)
        

                  
    elif x=='report':
        z=input('specify the type of report: ')
        
        if z=='financial balance':
            t1=input('enter the starting time of the period: ')
            t2=input('enter the ending time of the period: ')
            if t2=='now':
                t2=str(khayyam.JalaliDate.today())
            z1=input('with units do you want? ').split('-')
            if z1==['all']:
                    z1=list(df.vahed)
            else:
                for i in range(len(z1)):
                    z1[i]=int(z1[i])        
            output=df_transaction[(df_transaction.time>=t1) & (df_transaction.time<=t2) & (df_transaction.related_unit).isin(z1)]
            output1=output[output['category']!='charge'].groupby('related_unit',as_index=False).aggregate({'amount':'sum'})
            output=output[output['category']=='charge'].groupby('related_unit',as_index=False).aggregate({'amount':'sum'})     
            output.amount -= output1.amount
            print(output)
            output.to_csv('financial balance')
        
        if z=='receipt':
            t1=input('enter the starting time of the period: ')
            t2=input('enter the ending time of the period: ')
            if t2=='now':
                t2=str(khayyam.JalaliDate.today())
            output=df_transaction[(df_transaction.time>=t1) & (df_transaction.time<=t2)]   
            print(output)
            output.to_csv('receipt')            

        if z=='budget':
            t1=input('enter the starting time of the period: ')
            t2=input('enter the ending time of the period: ')
            if t2=='now':
                t2=str(khayyam.JalaliDate.today())
            output=df_transaction[(df_transaction.time>=t1) & (df_transaction.time<=t2)]
            budget=output[output['category']=='charge'].amount.sum()-output[output['category']!='charge'].amount.sum()
            print(budget)
            
        if z=='portion':
            y=input('portion in group or total? ')
            
            if y=='in group':
                z1=input('enter sub categories: ').split('-')
                l1=[]
                l2=[]
                others=df_transaction[df_transaction['category'].isin(['water','gas','electricity','city_hall'])].amount.sum()
                for i in z1:
                    l1.append(df_transaction[df_transaction['category']==i].amount.sum())
                    l2.append(i)
                    others-=df_transaction[df_transaction['category']==i].amount.sum()
                l1.append(others)
                l2.append('others')
                plt.pie(l1,labels=l2,autopct='%1.1f%%',startangle=90)
                plt.show()
            
            if y=='in total':
                z1=input('enter sub categories: ').split('-')
                l1=[]
                l2=[]
                others=df_transaction[df_transaction['category']!='charge'].amount.sum()
                for i in z1:
                    l1.append(df_transaction[df_transaction['category']==i].amount.sum())
                    l2.append(i)
                    others-=df_transaction[df_transaction['category']==i].amount.sum()
                l1.append(others)
                l2.append('others')
                plt.pie(l1,labels=l2,autopct='%1.1f%%',startangle=90)
                plt.show()
            
        if z=='cost trend':
            y=input('for units or sub categories? ')
            if y=='units':
                z1=input('with units do you want? ').split('-')
                if z1==['all']:
                    z1=list(df.vahed)
                else:
                    for i in range(len(z1)):
                        z1[i]=int(z1[i])        
                z2=input('with sub categories do you want? ').split('-')
                if z2==['all']:
                    z2=l
                t1=input('enter the starting time of the period: ')
                t2=input('enter the ending time of the period: ')
                if t2=='now':
                    t2=str(khayyam.JalaliDate.today())
                output=df_transaction[(df_transaction.time>=t1) & (df_transaction.time<=t2) & (df_transaction.related_unit.isin(z1)) & (df_transaction.category.isin(z2))] 
                output=output.groupby(['related_unit','time'],as_index=False).aggregate({'amount':'sum'})
                output_average=df_transaction[(df_transaction.time>=t1) & (df_transaction.time<=t2) ].groupby(['time'],as_index=False).aggregate({'amount':'sum'})
                output_average.amount=output_average.amount/df.vahed.count()
                plt.plot(output_average.time,output_average.amount.cumsum(),marker='.',label='average')
                for i in output['related_unit'].unique():
                    output1=output[output['related_unit']==i]
                    output1=output1.groupby(['related_unit','time'],as_index=False).aggregate({'amount':'sum'})
                    plt.plot(output1.time,output1.amount.cumsum(),marker='.',label=i)
                plt.legend()
                plt.xticks(rotation=45)
                plt.show() 
    
        
            if y=='sub categories':
                z2=input('with sub categories do you want? ').split('-')
                if z2==['all']:
                    z2=l
                t1=input('enter the starting time of the period: ')
                t2=input('enter the ending time of the period: ')
                if t2=='now':
                    t2=str(khayyam.JalaliDate.today())
                output=df_transaction[(df_transaction.time>=t1) & (df_transaction.time<=t2) & (df_transaction.category.isin(z2))]
                output=output.groupby(['category','time'],as_index=False).aggregate({'amount':'sum'})
                output_average=df_transaction[(df_transaction.time>=t1) & (df_transaction.time<=t2) ].groupby(['time'],as_index=False).aggregate({'amount':'sum'})
                output_average.amount=output_average.amount/df.vahed.count()
                plt.plot(output_average.time,output_average.amount.cumsum(),marker='.',label='average')
                for i in output['category'].unique():
                    output1=output[output['category']==i]
                    output1=output1.groupby(['category','time'],as_index=False).aggregate({'amount':'sum'})
                    plt.plot(output1.time,output1.amount.cumsum(),marker='.',label=i)
                plt.legend()
                plt.xticks(rotation=45)
                plt.show()   
                
        if z=='predicting the charge cost':
            t1=input('enter the starting time of the period: ')
            t2=input('enter the ending time of the period: ')
            inflation=input('enter the inflation rate: ')
            if t2=='now':
                t2=str(khayyam.JalaliDate.today())
            output=df_transaction[(df_transaction.time>=t1) & (df_transaction.time<=t2)]
            t1=t1.split('-')
            t2=t2.split('-')
            t1=datetime.date(int(t1[0]),int(t1[1]),int(t1[2]))
            t2=datetime.date(int(t2[0]),int(t2[1]),int(t2[2]))
            days=(t2-t1).days
            output=output['amount'].sum()
            output+=int(inflation)*output/100
            print('estimated charging cost is :')
            print(round(output*(days/365)/120))
            print()
    else:
        
        print('wrong command!\n')
        
        continue
    
    print('Done!\n') 
    

df_transaction.to_csv('transaction.csv')



