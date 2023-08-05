import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
#from sklearn.linear_model import LinearRegression,Ridge,Lasso,RidgeCV,LassoCV,ElasticNet,ElasticNetCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np




class all_in_1:
    def __init__(self,dataset,out,visualize=False,standard=False,stats=False,future_sel=False,outlayer_removel=False,multicol=False,remove_null=False):
        self.dataset=dataset
        self.out=out
        self.v=visualize
        self.out=outlayer_removel
        self.m=multicol
        self.std=standard
        self.s=stats
        if self.std==True:
            self.standardtation(dataset,out)
        if self.v==True:
            self.visualize_data(dataset,out)
        if self.s==True:
            self.stats_data(dataset,out)
        if self.m==True:
            self.multi_col1(dataset,out)
            
        if self.out==True:
            self.find_outlayer(dataset)
        if remove_null==True:
            self.remove_nan_value(dataset,out)
    def stats_data(self,dataset,out):
        
        print('our dataset Stats Analysis :')
        try:
            
            
        
            print(dataset.describe())

            print('---'*20)
            
            print()
            print('dataset  croreation')
            print(dataset.corr())
            print('---'*20)
            print()
            
            print('---'*20)
            print()
            replace_i=[]
            replace_i1=[]
            try:
                import statsmodels.formula.api as sm
                col=dataset.columns
                s1=''
                replace_i=[]
                replace_i1=[]
                for i in col:
                    if i.startswith('Serial' or 'serial' or 'SERIAL'):
                        continue

                    new=i.replace(' ','_')

                    replace_i.append(new)
                for i in col:


                    new=i.replace(' ','_')

                    replace_i1.append(new)

                for i,j in enumerate(replace_i):
                    if i<len(replace_i)-1:
                        s1=s1+j+'+'
                    else:
                        s1=s1+j
                print(s1)
                out=out.replace(' ','_')
                new_d=np.asarray(dataset)
                new_d1=pd.DataFrame(new_d,columns=replace_i1)
                print(new_d1.columns)
                lm=sm.ols(formula=f'{out} ~ {s1}',data=new_d1).fit()
                print('stats table')
                print()
                print(lm.summary())
            except Exception as e:
                print('error ',e)
            print('calculate the multi colinearity ')
            self.multi_col1(dataset,out)
        

        except Exception as e:
                  print('erorr stats ',e)
        
              
            
    def remove_nan_value(self,dataset,out):
      
        li=[dataset._get_numeric_data().columns]
        print(li)

        try:

            for i in range(len(dataset.columns)):

                if dataset.columns[i] in li[0]:
                    if dataset[dataset.columns[i]].nunique()<6:
                        
                        dataset[dataset.columns[i]].fillna(dataset[dataset.columns[i]].mode()[0],inplace=True)
                    else:
                        
                        dataset[dataset.columns[i]].fillna(dataset[dataset.columns[i]].mean(),inplace=True)
                else:
                    
                    dataset[dataset.columns[i]].fillna(dataset[dataset.columns[i]].mode()[0],inplace=True)
            return dataset
        except Exception as e:
                  print('error ',e)
     
    def find_outlayer(self,dataset):
        
        """ 
        this function find and remove the outlayers in our dataset
        
        and return tha new_dataset
        
        """
        out_layer_list=[]
        col=dataset.columns
        ind=[ i for i,j in enumerate(dataset.dtypes) if j=='float64' or 'int64']
        col_name=dataset.columns[ind]
        for i in col_name:
            try:
                if dataset[i].isna().sum()<=0:
               
                    q1=np.percentile(dataset[i],25)
                    q3=np.percentile(dataset[i],75)
                    iq=q3-q1
                    upper=q3+(1.5*iq)
                    lower=q1-(1.5*iq)
                    print(i)
                    print(upper,lower)
                    for i1,j in enumerate(dataset[i]):
                        if j<upper and j>lower:
                            pass
                        else:
                            print(f'col of {i} index is {i1} val is {j} ')
                            out_layer_list.append(i1)
                else:
                    print('some val was null val so you first remove null values')
                    inp1=input('if you want remove outayer yes ---1 o no---0')
                    if inp1=='1':
                        self.remove_nan_value(dataset,out)
            except Exception as e:
                print('eror ',e)
        inp=input('if you want the emove the outlayersyes--1 or no---0')
        if inp=='1':


            a=(dataset.iloc[out_layer_list]).index
            dataset.drop(a,inplace=True)
            print('our new dataset shape :',dataset.shape)
   


    def visualize_data(self,d,o):
        
        """ 
        this function removivisualize in our dataset to better undestanding in our dataset
        
        """
        inp=input('if you want to save all the plots y---1 or n---0')
        try:
            if inp=='1':
                inp1=input('enter path')
                  
        except Exception as e:
                  print('enter 0 or 1 ')
        
        int_col,object_col=[],[]
        cat_col,num_col=[],[]

        df=d
        print(type(df))
        out_come=o
        col=d.columns
        col=d.columns
        for i in range(len(col)):

            if d[col[i]].nunique()<6:
                cat_col.append(col[i])
            else:
                 num_col.append(col[i])

        for i in range(len(num_col)):
            
            
            print(num_col)
            plt.scatter(x=num_col[i],y=o,data=d)
            plt.show()
            print('--'*20)
            try:
                
                plt.savefig(inp1+num_col[i]+'_vs_'+o+'.png')
            
            except Exception as e:
                print('please enter valid path ',e)
                            
        
        for i in range(len(cat_col)):
            
            
            print()
            sns.barplot(x=cat_col[i],y=o,data=d)
            plt.show()
            print('--'*20)
            try:
                plt.savefig(inp1+cat_col[i]+'_vs_'+o+'.png')
            except Exception as e:
                print('please enter valid path ',e)

        inp=input('you want hist yes--1  no--0')
        if inp=='1':
            for i in d.columns:
                plt.xlabel(i)
                plt.ylabel('count')

                plt.hist(x=d[i])
                plt.show()
                print('--'*20)
    def featue_selection(self,dataset,out):
        """
        this function find best feature to our dataset
        
        this function used in corelation compaison method used
        
        if our dataset feature < 35% to correlation in output data remove the that paticular feature
        
        return the new dataset
        """
        cor=dataset.corr()
        ind=np.where(cor[out]<0.35)
        a=cor.iloc[ind].index
        print('this columns lower contribute our out come ' ,a)
        inp=input('if you want to remove columns y--1 or n--0')
        if inp=='1':
            dataset.drop(columns=a,inplace=True)
            return dataset
    def multi_col1(self,dataset,out):
        """
        this function findind the multicolinearity feature in our datset
        
        this function used variance_inflation_factor method
        
        return new_dataset
        """
        from statsmodels.stats.outliers_influence import variance_inflation_factor
        li=dataset._get_numeric_data().columns
        try:
            print(out)
            #data=dataset.drop(out,axis=1)
            final_data=dataset[li]
            print(final_data)
            x=np.asarray(final_data)
            
            data_vif=[variance_inflation_factor(x,i)for i in range(x.shape[1])]
            print('our dataset vif val ',data_vif)
            print()
            inp=input('if you want to remove the mlti col feature y --- 1 or n----0 ')
            if inp=='1':
            
                col_ind=[ i for i,j in enumerate(data_vif) if j>10]
                print(col_ind)
                col_name=dataset.columns[col_ind]
                print(col_name)
                dataset.drop(col_name,axis=1,inplace=True)
                print('our final col in dataset ',dataset.columns)
                return dataset
        except Exception as e:
            print('error mul ',e)
        
        
    def standardtation(self,dataset,out):
        """
        this function standardtizeing in our dataset
        
        return standadtize dataset
        """
        data=dataset.drop(out,axis=1)
        li=data._get_numeric_data().columns
        from sklearn.preprocessing import StandardScaler
        scaler=StandardScaler()
        arr=scaler.fit_transform(dataset[li])
        final=pd.DataFrame(data=arr,columns=li)
        dataset[li]=final
        return dataset


