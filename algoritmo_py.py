def homologo(texto_input):
    texto_output=''
    dfObj = pd.DataFrame(columns=['Nombre', 'value', 'simil'])

    for i in range(len(df_u)):
        xbase = df_u.iloc[i]['Nombre ']
        simil=0
        simil = 100*lev.similarity(xbase, texto_input)
        if (simil>=89):
            dfObj.loc[len(dfObj)] = [xbase, texto_input, simil]

    if (len(dfObj)>0):
        dt = dfObj.sort_values(by='simil', ascending=False).head(1)
        texto_output = dt.iloc[0]['Nombre']

    return texto_output
	
    
import pandas as pd
from hermetrics.levenshtein import Levenshtein
lev = Levenshtein()

df_ie= pd.read_csv("E:\\KROWDY\\instituciones_educativas.csv")
df_ie['value'] = df_ie['value'].astype('string')

df_u= pd.read_json("E:\\KROWDY\\universidades.json")

    
dfvalue_res = pd.DataFrame(columns=['value', 'value_homologo'])
dfvalue_res['value'] = dfvalue_res['value'].astype('string')
dfvalue_res['value_homologo'] = dfvalue_res['value_homologo'].astype('string')

df_value = df_ie.groupby(["value"], as_index=False).count()
df_value.rename(columns={'candidateId':'qtd'}, inplace=True)

for i in range(len(df_value)):
    xvalue = df_value.iloc[i]['value']
    xvalue_h = homologo(xvalue)
    dfvalue_res.loc[len(dfvalue_res)] = [xvalue, xvalue_h]
    
    
######################################################################################################
#CREA universidades_homologadas.csv
######################################################################################################
dfvalue_res = dfvalue_res.rename(columns={'value_homologo':'universidad homologada'})

dfvalue_res['value'] = dfvalue_res['value'].astype('string')
dfvalue_res['universidad homologada'] = dfvalue_res['universidad homologada'].astype('string')

df_h = df_ie.merge(dfvalue_res, on='value', how='left')
df_h

df_h.to_csv("E:\\KROWDY\\universidades_homologadas.csv", index=False)

    ######################################################################################################
#CREA sinonimo_universidades.json
######################################################################################################
import numpy as np
def f(df):
    keys, values = df.sort_values('sinonimos').values.T
    ukeys, index = np.unique(keys, True)
    arrays = np.split(values, index[1:])
    df2 = pd.DataFrame({'nombre_universidad':ukeys, 'sinonimos':[list(a) for a in arrays]})
    return df2
    
df_json = dfvalue_res[dfvalue_res['universidad homologada']!='']
dfx = df_json.rename(columns={'value':'sinonimos', 'universidad homologada':'nombre_universidad'})
dfr = f(dfx)

dfr.to_json(r"E:\\KROWDY\\sinonimo_universidades.json", orient='records')