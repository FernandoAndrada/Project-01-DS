import pandas as pd
import datetime as dt
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual
import numpy as np






df = pd.read_csv ("D:\pycharm\PyCharm Community Edition 2022.1.3\house_sale_king\kc_house_data.csv")

# Supress Scientific Notation
np.set_printoptions(suppress=True)
pd.set_option('display.float_format', '{:.2f}'.format)

# Ajeitando data 'date'

df['date'] = pd.to_datetime(df['date']). dt.strftime( '%Y-%m-%d')

# -*H1: Imóveis que possuem vista para água, são 30% mais
# caros, na média.

# ---> ['price_m2'] = Transformar sqft_lot em m2 => 1 pés = 0.3048 m
#     ---> ['Year'] ==> ordenar a coluna em ordem crescente
#     ---> ['price_inc_perc_year'] ===> percentual 'price'em 'Year' = x 'price' em 'Year'+ 1 = y -> x-y/x = percent

df['month_year']=pd.to_datetime(df['date'] ). dt.strftime( '%m')
df['Year'] = pd.to_datetime(df['date']).dt.strftime('%Y')
df['price_m2'] = (df['price'] / (df['sqft_lot']* 0.3048)).round()
df['price_inc_perc_year'] = 'perc'

#     Criar novo df = df_buy_now com as seguintes colunas:

df_buy_now = df


# df = data.loc[data['yr_renovated'] > 1930, ['price', 'yr_renovated']].groupby( 'yr_renovated' ).mean().reset_index()
#- criar dataframe df_wf_view com 'price','zipcode','waterfront','price_m2' 


cols = ['id', 'date', 'bedrooms', 'sqft_living',
       'sqft_lot', 'floors', 'view', 'condition', 'grade',
       'sqft_above', 'sqft_basement', 'yr_built', 'yr_renovated',
       'lat', 'long', 'sqft_living15', 'sqft_lot15', 'Year',
       'price_inc_perc_year']

df_wf_view = df_buy_now.drop(cols, axis=1)



df_wf = df_wf_view.loc[df_wf_view['waterfront'] == 1, ['zipcode','price_m2']].groupby('zipcode').mean()


mean_water = df_wf['price_m2'].mean()


df_no_wf = df_wf_view.loc[df_wf_view['waterfront'] == 0, ['zipcode','price_m2']].groupby('zipcode').mean()

mean_no_water = df_no_wf['price_m2'].mean()

perc_water_yn = ((mean_water-mean_no_water)/mean_water)*100

print(f'A variação de preço entre os imóveis é de {perc_water_yn:.2f} % maior para os com vista para água.')


waterfront_bar = widgets.RadioButtons( 
    options=['Water View','No Water View'],
   # value= False, 
    description='Water View', 
    disable=False
    )

def waterfront ( df_wf, waterfront_bar):
    if waterfront_bar == 'Water View':
        print(df_wf)
    else:
        print(df_no_wf)


widgets.interactive(waterfront, df_wf = fixed (df_wf), waterfront_bar=waterfront_bar)



# jupyter continua não imprimindo resultado widgets

# -*H2: Imóveis com data de construção menor que 1955, são 50% mais baratos, na média.

df_yr_bt55 = df_buy_now.loc[df_buy_now['yr_built'] == 1955, ['zipcode','price_m2']].groupby('zipcode').mean()


md_yr_55 = df_yr_bt55['price_m2'].mean()


df_no_wfb55 = df_buy_now.loc[df_buy_now['yr_built'] != 1955, ['zipcode','price_m2']].groupby('zipcode').mean()

mean_no_1955 = df_no_wfb55['price_m2'].mean()

per_yr_bt55 = (((md_yr_55-mean_no_1955)/md_yr_55)*100)*-1

print(f'A variação de preço entre os imóveis é de {per_yr_bt55:.2f} % maior para os construidos após 1955.')

# filtro iterativo RadioButtons

yr_built_but = widgets.RadioButtons( 
    options=['Year 1955','Year after 1955'],
   # value= False, 
    description='Year 1955', 
    disable=False
    )

def yr_1955 ( df_buy_now, yr_built_but):
    if yr_built_but == 'Year 1955':
        print(df_yr_bt55)
    else:
        print(df_no_wfb55)


widgets.interactive(yr_1955, df_buy_now = fixed (df_buy_now), yr_built_but = yr_built_but)

# -*H3: Imóveis sem porão possuem sqrt_lot, são 50%  maiores do que com porão. 'sqft_lot' 'sqft_basement'

#separando dfs

df_lot_basement = df_buy_now.loc[df_buy_now['sqft_basement'] != 0, ['id','sqft_lot']].groupby('id').max()
df_basement_mean = df_lot_basement['sqft_lot'].mean()

df_lot_no_basement = df_buy_now.loc[df_buy_now['sqft_basement'] == 0, ['id','sqft_lot']].groupby('id').max()
df_no_basement_mean = df_lot_no_basement['sqft_lot'].mean()

perc_lot_basement = (((df_lot_no_basement-df_no_basement_mean)/df_lot_no_basement)*100)*-1

print(f'A variação de tamanho de lotes em pés entre os imóveis com ou sem porão é de {perc_yr_built1955:.2f} % maior para os sem porão.')


# filtro iterativo RadioButtons

basement_but = widgets.RadioButtons( 
    options=['Basement','No basement'],
   # value= False, 
    description='Basement', 
    disable=False
    )

def basement ( df_buy_now, basement_but):
    if basement_but == 'Basement':
        print(df_lot_basement)
    else:
        print(df_lot_no_basement)


widgets.interactive(basement, df_buy_now = fixed (df_buy_now), basement_but = basement_but)



# -*H4: O crescimento do preço dos imóveis YoY ( Year over
# Year ) é de 10%
#Ordenar 'yr_built'

df_yr_built = df_buy_now[['id','price','Year','month_year','bathrooms','price_m2','price_inc_perc_year','zipcode','yr_built']].sort_values( 'yr_built', ascending=False ).reset_index()

#crescimento proporcional entre linhas ['price_inc_perc_year'] price_m2.pct_change()

df_yr_built['price_inc_perc_year'] = (df_yr_built.price_m2.pct_change())*100


data = df_yr_built

def increment_Y (data):

    
    filtro = (data['price_inc_perc_year']<=100)#&(data['price_inc_perc_year']>0)
    data = data[filtro]
    price_std = data['price_inc_perc_year'].mean()

    print(f'O crescimento do preço dos imóveis ano a ano é de {price_std:.2f} % e não de 10%.''Obs: Selecionados os imóveis com crescimento menor igual a 100%, que representa - 67,93 % df.')
    
print(increment_Y(data))

zipcode_slider = widgets.IntSlider(
    value= 98001,
    min=98001,
    max=98199,
    step=1,
    description='Zipcode:',
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d'
)

def zipcode ( df_yr_built, limit ):
    
    dfzip = df_yr_built.loc[df_yr_built['zipcode'] == limit, ['zipcode','price_m2','price_inc_perc_year','yr_built']].groupby( 'price_inc_perc_year').mean().reset_index()
    
    print (dfzip)
    

widgets.interactive(zipcode, df_yr_built = fixed (df_yr_built), limit = zipcode_slider)


# -*H5: Imóveis com 3 banheiros tem um crescimento MoM
# ( Month over Month ) de 15%
# no parametro 'bathrooms'=3
#     ver mediana entre os anos ['price_inc_perc_year']
#     Encontrar o percentual de aumento entre eles

df_yr_built['price_inc_perc_month'] = (df_yr_built.price_m2.pct_change())*100
df_inc_bathrooms = df_yr_built.loc[(df_yr_built['bathrooms']==3),['id','bathrooms','price_m2','price_inc_perc_month','month_year']].groupby('month_year').median()
df_inc_month = df_inc_bathrooms['price_inc_perc_month'].mean()

print(f'O cresimento mês a mês dos imóveis com 3 banheiros é de {df_inc_month:.2f}% ao mês nos anos de 2014 e 2015.')
    


df_zipcode = df_yr_built.loc[(df_yr_built['zipcode']>98000),['id','price_m2','price','zipcode','Year']].groupby('zipcode').median().sort_values( 'price', ascending=False ).reset_index()
df_zipcode.head()


# - H7 valorização do zipcode por ano a ano

#     groupby ['price_inc_perc_year'],['zipcode']
#     criar df_price_zipcode
    
#     streamlit  botão slide 'zipcode'
df_zipcode = df_yr_built.loc[(df_yr_built['zipcode']>98000),['id','price_m2','price','zipcode','price_inc_perc_year','Year']].groupby(['zipcode','Year']).median().sort_values( 'price', ascending=False ).reset_index()
df_zipcode.head()

# - H8 qual zipcode está com tendência de alta, listar zipcode com potencial valorização  e qual percentual de ganho 

#     Com base no df_price_zipcode 
#     Qual o zipcode com a maior média de valorização 
#     qual zipcode está em alta e qual o potencial ganho
df_zipcode = df_yr_built.loc[(df_yr_built['zipcode']==98039),['id','price_m2','price','zipcode','Year']].groupby(['price_m2']).mean().sort_values('price_m2', ascending=False ).reset_index()
df_zipcode.head()

#     qual zipcode está em alta e qual o potencial ganho = maior que a mediana 'price_m2'= 367


cols = [ 'bedrooms', 'bathrooms', 'sqft_living','waterfront',
       'sqft_lot', 'floors','sqft_above', 'sqft_basement','sqft_living15', 'sqft_lot15', 'month_year', 'Year']
     
df_md_price = df_buy_now.drop(cols, axis=1) 

df_md_price.loc[(df['price_m2']<367)&(df['zipcode']==98039),:'price_m2']

# o zipcode com maior alta é o 98039 e os imóveis com maior potencial de ganho foram baseados na vista e nas condições do imóvel.


# - H9 qual zipcode está com tendência de baixa e listar imóveis para venda imediata

#     Com base no df_price_zipcode
#     qual zipcode está em baixa e qual a potencial perda
#     Qual o zipcode para venda imediata

df_zipcode = df_yr_built.loc[(df_yr_built['zipcode']>98000),['id','price_m2','price','zipcode','price_inc_perc_year','Year']].groupby(['zipcode','Year']).median().sort_values( 'price', ascending=True ).reset_index()
df_zipcode.head()

#     Qual o zipcode para venda imediata

df_yr_built.loc[(df_yr_built['price_m2']<367)&(df_yr_built['zipcode']==98168)&(df_yr_built['price_inc_perc_year']<0)&(df_yr_built['price_inc_perc_year']<-90),:'yr_built'].sort_values( 'price_inc_perc_year', ascending=True )

O zipcode é o 98168 com os imóveis com perda de quase 100%

# - H10 verificar se no zipcode com maior alta tem imóveis em mal estado e preço baixo que valha pena a compra

#     No maior zipcode com alta, procurar casas em mal estado 'condition' == 1 ! 2 e com preço baixo calcular potencial ganho ['perc_gain']compra reforma e venda.
#     verificar se cabe botões


df_md_price.loc[(df['price_m2']<367)&(df['zipcode']==98039)&(df['condition']<=3),:'price_m2']

### Resposta 2 Construir uma tabela com recomendações de compra ou não compra.

# Com base na analise dos zipcodes fazer um dataframe com 'id', 'price','buy','waterfront','zipcode','lat','long'
# df_buy = ['buy'] = 'yes' ! 'no'

# streamlit = marcação 'yes' 'no' = slide 'zipcode'
# [fazer mapa com os imóveis selecionados] não pede na tarefa

# Selecionados pelo valor da mediana do 'price_m2', abaixo 'Yes', acima 'No'

cols = ['Year', 'month_year', 'bathrooms','price_inc_perc_month','price_inc_perc_year']
df_buy = df_yr_built.drop(cols, axis=1)
df_buy['buy'] = 'yes'
buy_median = df_buy['price_m2'].median()

df_buy['buy'] = df_buy ['price_m2']. apply (lambda x: 'Yes' if x < buy_median else 'No')


df_buy
     

### 3 Construir uma tabela com recomendações de venda com acréscimo de 10 ou 30%.

df_recom = df_buy[df_buy['buy'] == 'Yes'].copy()

#df_recom['purchase'] = '0'

buy_median = df_recom['price_m2'].median()

df_recom.loc[(df_recom['price_m2'] <  buy_median ) , 'sell'] = 'Add 30%'
df_recom.loc[(df_recom['price_m2'] >  buy_median ) , 'sell'] = 'Add 10%'


#df_recom['purchase'] = df_recom['price_m2'].apply (lambda x: 'Yes' if x < buy_median else 'No')


df_recom