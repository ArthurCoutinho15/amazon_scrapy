import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()


def conn_mysql(host, user, password, database):
    try:
        connection_url = f'mysql+pymysql://{user}:{password}@{host}/{database}'
        engine = create_engine(connection_url)
        print("Sucessfully connected to MySQL")
        return engine
    except Exception as e:
        print(f'Error: {e}')
        return None


def get_data(engine):
    query = """ SELECT * FROM amazon.products"""
    df = pd.read_sql(query, engine)
    return df


def kpi(df):
    st.title('Análise de Notebooks')

    st.header('Dados de Notebooks')
    st.dataframe(df)

    st.sidebar.header('Filtros')

    price_min = st.sidebar.number_input(
        'Preço mínimo', min_value=0.0, value=float(df['price'].min()))
    price_max = st.sidebar.number_input(
        'Preço máximo', min_value=0.0, value=float(df['price'].max()))

    rating_min = st.sidebar.slider(
        'Avaliação mínima', min_value=0.0, max_value=5.0, value=0.0)
    rating_max = st.sidebar.slider(
        'Avaliação máxima', min_value=0.0, max_value=5.0, value=5.0)

    filtered_df = df[
        (df['price'] >= price_min) & (df['price'] <= price_max) &
        (df['mean'] >= rating_min) & (df['mean'] <= rating_max)
    ]

    st.header('Dados Filtrados')
    st.dataframe(filtered_df)

    st.header('Análise Gráfica')

    st.subheader('Distribuição de Preços')
    st.bar_chart(filtered_df['price'])

    st.subheader('Distribuição de Avaliações')
    st.bar_chart(filtered_df['mean'])

    st.write('Aplicação desenvolvida para análise de notebooks raspados da Amazon.')


if __name__ == '__main__':
    HOST = os.getenv('HOST')
    USER = os.getenv('USER')
    PASSWORD = os.getenv('PASSWORD')
    DATABASE = os.getenv('DB_NAME_PROD')

    engine = conn_mysql(HOST, USER, PASSWORD, DATABASE)
    df = get_data(engine)
    kpi(df)
