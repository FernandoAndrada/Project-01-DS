
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

@st.cache( allow_output_mutation=True )
def get_data( path ):
    df = pd.read_csv( path )

    return df

def view_data (df):
    st.title('Houses in Houses')
    st.markdown('Bem vindo(a)')

    st.header('Imóveis')

    return None

def set_feature ( df ):
    np.set_printoptions(suppress=True)
    pd.set_option('display.float_format', '{:.2f}'.format)

    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

    df['month_year'] = pd.to_datetime(df['date']).dt.strftime('%m')
    df['Year'] = pd.to_datetime(df['date']).dt.strftime('%Y')
    df['price_m2'] = (df['price'] / (df['sqft_lot'] * 0.3048)).round()
    df['price_inc_perc_year'] = 'perc'

    # Criar novo df = df_buy_now com as seguintes colunas:

    df_buy_now = df
    st.write(df_buy_now.head(5))

    cols = ['id', 'date', 'bedrooms', 'sqft_living',
            'sqft_lot', 'floors', 'view', 'condition', 'grade',
            'sqft_above', 'sqft_basement', 'yr_built', 'yr_renovated',
            'sqft_living15', 'sqft_lot15', 'Year',
            'price_inc_perc_year']

    df_wf_view = df_buy_now.drop(cols, axis=1)

    df_wf = df_wf_view.loc[df_wf_view['waterfront'] == 1, ['zipcode', 'price_m2']].groupby('zipcode').mean()

    mean_water = df_wf['price_m2'].mean()

    df_no_wf = df_wf_view.loc[df_wf_view['waterfront'] == 0, ['zipcode', 'price_m2']].groupby('zipcode').mean()

    mean_no_water = df_no_wf['price_m2'].mean()

    perc_water_yn = ((mean_water - mean_no_water) / mean_water) * 100

    # Respondendo Hipóteses

    st.header('Hipóteses')

    st.subheader('Hipótese 1:')
    st.write(' Imóveis que possuem vista para água, '
             'são 30% mais caros, na média.')

    st.subheader('Resp H1: ')
    st.write(f'A variação de preço entre os imóveis '
             f'é  {perc_water_yn:.2f} % maior para '
             f'os com vista para água.')
    st.write('')
    st.caption('Preços')

    # interactive butons

    waterfront_bar = st.sidebar.radio(
        "H1 - Preços dos imóveis:",
        ('Com vista para água;', 'Sem vista para água.'))

    if waterfront_bar == 'Com vista para água;':
        st.write((df_wf).round(0))

    else:
        st.write((df_no_wf).round(0))

    # Respondendo Hipóteses

    st.subheader('Hipótese 2:')
    st.write('Imóveis com data de construção menor que 1955, são 50% mais baratos, na média. ')

    st.subheader('Resp H2: ')

    df_yr_bt55 = df_buy_now.loc[df_buy_now['yr_built'] == 1955, ['zipcode', 'price_m2']].groupby('zipcode').mean()

    md_yr_55 = df_yr_bt55['price_m2'].mean()

    df_no_wfb55 = df_buy_now.loc[df_buy_now['yr_built'] != 1955, ['zipcode', 'price_m2']].groupby('zipcode').mean()

    mean_no_1955 = df_no_wfb55['price_m2'].mean()

    per_yr_bt55 = (((md_yr_55 - mean_no_1955) / md_yr_55) * 100) * -1

    st.write(f'A variação de preço entre os imóveis é {per_yr_bt55:.2f} % maior para os construidos após 1955.')
    st.write('')
    st.caption('Preços m2')

    # # filtro iterativo RadioButtons

    yr_built_but = st.sidebar.radio(
        "H2 - Ano dos imóveis:",
        ('Ano de 1955;', 'Depois de 1955.'))

    if yr_built_but == 'Ano de 1955;':
        st.write((df_yr_bt55).round(0))

    else:
        st.write((df_no_wfb55).round(0))

    # Respondendo Hipóteses

    st.subheader('Hipótese 3:')
    st.write('Imóveis sem porão possuem sqrt_lot, são 50%  maiores do que com porão.')
    st.subheader('Resp H3: ')

    df_lot_basement = df_buy_now.loc[df_buy_now['sqft_basement'] != 0, ['id', 'sqft_lot']].groupby('id').max()
    df_basement_mean = df_lot_basement['sqft_lot'].mean()

    df_lot_no_basement = df_buy_now.loc[df_buy_now['sqft_basement'] == 0, ['id', 'sqft_lot']].groupby('id').max()
    df_no_basement_mean = df_lot_no_basement['sqft_lot'].mean()

    perc_lot_basement = (((df_no_basement_mean - df_basement_mean) / df_no_basement_mean) * 100)

    st.write(
        f'A variação de tamanho de lotes em pés entre os imóveis com ou sem porão é de {perc_lot_basement:.2f} % maior para os sem porão.')

    # # filtro iterativo RadioButtons

    basement_but = st.sidebar.radio(
        "H3 - Imóveis com ou sem porão:",
        ('Com porão;', 'Sem porão.'))

    if basement_but == 'Com porão;':
        st.write((df_lot_basement).round(0))

    else:
        st.write((df_lot_no_basement).round(0))

    # Respondendo Hipóteses

    st.subheader('Hipótese 4:')
    st.write('O crescimento do preço dos imóveis YoY ( Year over Year ) é de 10%')
    st.subheader('Resp H4: ')



    df_yr_built = df_buy_now[
        ['id', 'price', 'Year', 'month_year', 'bathrooms', 'price_m2', 'price_inc_perc_year', 'zipcode',
         'yr_built', 'lat', 'long']].sort_values('yr_built', ascending=False).reset_index()

    # crescimento proporcional entre linhas ['price_inc_perc_year'] price_m2.pct_change()

    df_yr_built['price_inc_perc_year'] = (df_yr_built.price_m2.pct_change()) * 100

    data = df_yr_built

    # def increment_Y(data):
    filtro = (data['price_inc_perc_year'] <= 100)  # &(data['price_inc_perc_year']>0)
    data = data[filtro]
    price_std = data['price_inc_perc_year'].mean()
    st.write(f'O crescimento do preço dos imóveis ano a ano é de {price_std:.2f} % e não de 10%.')
    st.write('Obs: Selecionados os imóveis com crescimento menor igual a 100%, que representa 67,93 % do Data Frame.')

    # # filtro iterativo

    zipcode_slider = st.sidebar.slider('H4 - Escolha o zipcode', 98001, 98199)
    dfzip = df_yr_built.loc[
        df_yr_built['zipcode'] == zipcode_slider, ['zipcode', 'price_m2', 'price_inc_perc_year']].groupby(
        'price_inc_perc_year').mean().reset_index()
    st.write(dfzip)

    # Respondendo Hipóteses

    st.subheader('Hipótese 5:')
    st.write('Imóveis com 3 banheiros tem um crescimento MoM Month over Month ) de 15%.')
    st.subheader('Resp H5: ')

    df_yr_built['price_inc_perc_month'] = (df_yr_built.price_m2.pct_change()) * 100
    df_inc_bathrooms = df_yr_built.loc[
        (df_yr_built['bathrooms'] == 3), ['id', 'bathrooms', 'price_m2', 'price_inc_perc_month', 'month_year']].groupby(
        'month_year').median()
    df_inc_month = df_inc_bathrooms['price_inc_perc_month'].mean()

    st.write(
        f'O cresimento mês a mês dos imóveis com 3 banheiros é de {df_inc_month:.2f}% ao mês nos anos de 2014 e 2015.')

    # filtro iterativo RadioButtons

    yr_built_but = st.sidebar.radio(
        "H5 - Ano dos imóveis:",
        ('Ano de 2014;', 'Ano de 2015.'))
    df_inc_bathrooms = df_yr_built.loc[
        df_yr_built['bathrooms'] == 3, ['id', 'bathrooms', 'price_m2', 'price_inc_perc_month', 'month_year',
                                        'Year']].groupby('Year').median()
    df_no_inc_bathrooms = df_yr_built.loc[
        df_yr_built['bathrooms'] == 3, ['id', 'bathrooms', 'price_m2', 'price_inc_perc_month', 'month_year',
                                        'Year']].groupby('Year').median().sort_values('Year', ascending=False)

    if yr_built_but == 'Ano de 2014;':
        st.write(df_inc_bathrooms)

    else:
        st.write(df_no_inc_bathrooms)

    # Respondendo Hipóteses

    st.subheader('Hipótese 6:')
    st.write('Valores dos imóveis por zipcode e m2')
    st.subheader('Resp H6: ')

    # filtro iterativo

    zip_slider = st.sidebar.slider('H6 - Escolha o zipcode', 98001, 98199)
    df_zip = df_yr_built.loc[(df_yr_built['zipcode'] == zip_slider), ['price_m2', 'price', 'zipcode', 'Year']].groupby(
        'zipcode').median().sort_values('price', ascending=False).reset_index()
    st.write(df_zip)

    # plot map
    st.title('House Rocket Map')
    is_check = st.checkbox('Display Map')

    # filters
    # ordena data por zipcode

    zip = data.sort_values(by='zipcode')

    # widgetes selectbox

    price_slider = st.selectbox('Enter zipcode',
                                zip['zipcode'].unique()
                                )

    if is_check:
        # select rows
        houses = data[data['zipcode'] == price_slider][['id', 'lat', 'long',
                                                        'price', 'zipcode']]

        # draw map
        fig = px.scatter_mapbox(
            houses,
            lat="lat",
            lon="long",
            color="price",
            size="zipcode",
            color_continuous_scale=px.colors.cyclical.IceFire,
            size_max=15,
            zoom=10)

        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(height=600, margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.plotly_chart(fig)

    # Respondendo Hipóteses

    st.subheader('Hipótese 7:')
    st.write('Qual a valorização do zipcode por ano?')
    st.subheader('Resp H7: ')

    # - H7 valorização do zipcode por ano a ano


    zip_year_slider = st.sidebar.slider('H7 - Escolha o zipcode', 98001, 98199)
    df_zipcode = df_yr_built.loc[
        (df_yr_built['zipcode'] == zip_year_slider), ['price_m2', 'price', 'zipcode', 'price_inc_perc_year',
                                                      'Year']].groupby(
        ['zipcode', 'Year']).median().sort_values('Year', ascending=False).reset_index()

    st.write(df_zipcode)

    # Respondendo Hipóteses

    st.subheader('Hipótese 8:')
    st.write('Qual zipcode está com tendência de alta?')
    st.subheader('Resp H8: ')

    df_zipcode = df_yr_built.loc[
        (df_yr_built['zipcode'] == 98039), ['id', 'price_m2', 'price', 'zipcode', 'Year']].groupby(
        ['price_m2']).mean().sort_values('price_m2', ascending=False).reset_index()

    cols = ['bedrooms', 'bathrooms', 'sqft_living', 'waterfront',
            'sqft_lot', 'floors', 'sqft_above', 'sqft_basement', 'sqft_living15', 'sqft_lot15', 'month_year', 'Year']

    df_md_price = df_buy_now.drop(cols, axis=1)

    df_md_price.loc[(df['price_m2'] < 367) & (df['zipcode'] == 98039), :'price_m2']
    #
    st.write(
        'o zipcode com maior alta é o 98039 e os imóveis com maior potencial de ganho foram baseados na vista e nas condições do imóvel.')
    st.write(df_md_price)

    # Respondendo Hipóteses

    st.subheader('Hipótese 9:')
    st.write('Qual zipcode está com tendência de baixa?')
    st.subheader('Resp H9: ')

    # - H9 qual zipcode está com tendência de baixa e listar imóveis para venda imediata


    df_zipco = df_yr_built.loc[
        (df_yr_built['zipcode'] > 98000), ['id', 'price_m2', 'price', 'zipcode', 'price_inc_perc_year',
                                           'Year']].groupby(
        ['zipcode', 'Year']).median().sort_values('price', ascending=True).reset_index()


    # Qual o zipcode para venda imediata

    zipco = df_yr_built.loc[
            (df_yr_built['price_m2'] < 367) & (df_yr_built['zipcode'] == 98168) & (
                        df_yr_built['price_inc_perc_year'] < 0) & (
                    df_yr_built['price_inc_perc_year'] < -90), :'yr_built'].sort_values('price_inc_perc_year',
                                                                                        ascending=True)

    st.write('O zipcode é o 98168 com os imóveis com perda de quase 100 %')
    st.write(df_zipco)

    # Respondendo Hipóteses

    st.subheader('Hipótese 10:')
    st.write('Verificar se no zipcode com maior alta tem imóveis em mal estado e preço baixo que valha pena a compra.')
    st.subheader('Resp H10: ')

    compra_df = df_md_price.loc[(df['price_m2'] < 367) & (df['zipcode'] == 98039) & (df['condition'] <= 3),
                :'price_m2']
    st.write(compra_df)

    # Resposta 2 Construir uma tabela com recomendações de compra ou não compra.
    st.header('2 - Tabela com recomendações de compra:')

    cols = ['Year', 'month_year', 'bathrooms', 'price_inc_perc_month', 'price_inc_perc_year']
    df_buy = df_yr_built.drop(cols, axis=1)
    df_buy['buy'] = 'yes'
    buy_median = df_buy['price_m2'].median()

    df_buy['buy'] = df_buy['price_m2'].apply(lambda x: 'Yes' if x < buy_median else 'No')

    st.write(df_buy)

    st.header('3 - Tabela com recomendações de venda com acréscimo de 10 ou 30%.')
    # 3 Construir uma tabela com recomendações de venda com acréscimo de 10 ou 30%.

    df_recom = df_buy[df_buy['buy'] == 'Yes'].copy()



    buy_median = df_recom['price_m2'].median()

    df_recom.loc[(df_recom['price_m2'] < buy_median), 'sell'] = 'Add 30%'
    df_recom.loc[(df_recom['price_m2'] > buy_median), 'sell'] = 'Add 10%'

    st.write(df_recom)

    return None


if __name__=='__main__':


    df = get_data('kc_house_data.csv')


    view_data(df)

    df = set_feature ( df )
