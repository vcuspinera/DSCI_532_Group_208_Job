import numpy as np
import pandas as pd
data = pd.read_json('https://raw.githubusercontent.com/vega/vega-datasets/master/data/jobs.json')
data = pd.DataFrame(data)
data['job'] = data['job'].str.replace('Professor.*', 'Professor', regex=True)
mini_sd = data.groupby(['job']).std().sort_values(by=['perc'], 
                                                    ascending=[True]).reset_index().iloc[:10]
        
mini_sd = mini_sd.rename(columns = {'perc':'std'})
all1 = pd.merge(data, mini_sd, how="inner", on="job")
first = all1.query('sex == "men"')
second = all1.query('sex == "women"')
first = first.reset_index()
first['together'] = pd.Series(np.asarray(first['perc']) + np.asarray(second['perc']))
first = first.replace({'together' : 0}, value = np.nan)
first = first.interpolate()
first = first.sort_values(by=['std'], 
                        ascending=[True])
first = first.reset_index()

first2 = data.query('sex == "men"')
second2 = data.query('sex == "women"')
first2 = first2.reset_index()
first2['together'] = pd.Series(np.asarray(first2['perc']) + np.asarray(second2['perc']))
first2 = first2.replace({'together' : 0}, value = np.nan)
first2 = first2.interpolate()
first2 = first2.sort_values(by=['perc'], 
                        ascending=[True])
first2 = first2.reset_index()

first2['job'] = first2['job'].str.replace('Professor.*', 'Professor', regex=True)
first3 = first2[first2['year'].isin(['2000'])]
first3 = first3.sort_values(by=['perc'], ascending=[False]).iloc[:10]

all2 = pd.merge(first2, first3, how="inner", on="job")
