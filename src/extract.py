from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from datetime import date


def iniciar():
    driver = selenium_config()
    data = []
    product = input("Qual produto deseja fazer o scrapy: ").strip()
    base_url = f'https://www.amazon.com.br/s?k={product}'

    for page in range(1, 6):
        page_url = f'{base_url}&page={page}'
        print(f"Navegando para a página {page}")
        driver.get(page_url)
        time.sleep(10)
        try:
            page_data = scrapy(driver)
            data.extend(page_data)
        except Exception as e:
            print(f"Erro ao coletar dados da página {page}: {e}")

    gerar_csv(data)
    driver.quit()


def selenium_config():
    chrome_options = Options()
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver


def scrapy(driver):
    wait = WebDriverWait(driver, 30)
    try:
        products = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@data-component-type="s-search-result"]')))
    except Exception as e:
        print(f'Timeout ao tentar carregar os produtos: {e}')
        return []

    print(f'Quantidade de produtos: {len(products)}')
    data = []
    for product in products:
        try:
            name = product.find_element(By.XPATH, './/h2//span').text
        except Exception as e:
            print(f'Erro ao obter nome do produto: {e}')
            name = None
        try:
            price_symbol = product.find_element(
                By.XPATH, './/span[@class="a-price-symbol"]').text
            price_whole = product.find_element(
                By.XPATH, './/span[@class="a-price-whole"]').text
            price_fraction = product.find_element(
                By.XPATH, './/span[@class="a-price-fraction"]').text

            price_whole = price_whole.replace('.', '')
            price = f'R${price_whole},{price_fraction}'
        except Exception as e:
            print(f'Erro ao obter preço: {e}')
            price = None
        try:
            rating = product.find_element(
                By.XPATH, './/span[@class="a-size-base s-underline-text"]').text
        except Exception as e:
            print(f'Erro ao obter a quantidade de avaliações: {e}')
            rating = None
        try:
            mean_rating = product.find_element(
                By.CSS_SELECTOR, "span.a-icon-alt").get_attribute("textContent")
        except Exception as e:
            print(f'Erro ao obter média de avaliações: {e}')
            mean_rating = None
        try:
            link = product.find_element(
                By.XPATH, './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal" ]').get_attribute('href')
        except Exception as e:
            print(f'Erro ao obter link: {e}')
            link = None
        data.append({
            'name': name,
            'price': price,
            'rating': rating,
            'mean': mean_rating,
            'link': link
        })

    return data


def gerar_csv(data):
    if data:
        df = pd.DataFrame(data)
        df.to_csv('C:\\Users\\Arthur Coutinho\\Desktop\\Arthur Coutinho\\Python\\amazon-testeTécnico\\data\\amazon_notebooks.csv', index=False)
        print('Dados salvos')
    else:
        print('Nenhum dado salvo')


def leitura():
    df = pd.read_csv(
        'C:\\Users\\Arthur Coutinho\\Desktop\\Arthur Coutinho\\Python\\amazon-testeTécnico\\data\\amazon_notebooks.csv')
    return df


def mean_rating(df):
    df['mean'] = df['mean'].str.slice(0, 3)
    df['mean'] = df['mean'].str.replace(',', '.')
    df['mean'] = pd.to_numeric(df['mean'], errors='coerce')

    return df


def price_symbol(df):
    df['price'] = df['price'].str.replace('R$', '')
    df['price'] = df['price'].str.replace(',', '.')
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    return df


def integer_null(df):
    df = df.fillna(0)
    df['rating'] = df['rating'].astype(int)

    return df


def date_column(df):
    df['Date'] = date.today()
    return df


def conn_mysql(host, user, password, database):
    try:
        connection_url = f'mysql+pymysql://{user}:{password}@{host}/{database}'
        engine = create_engine(connection_url)
        print("Sucessfully connected to MySQL")
        return engine
    except Exception as e:
        print(f'Error: {e}')
        return None


def load_csv(df, engine):
    try:
        df.to_sql(name='products', con=engine,
                  if_exists='append', index=False)

        print('Data was sucessfully saved in products')
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    load_dotenv()
    iniciar()
    HOST = os.getenv('HOST')
    USER = os.getenv('USER')
    PASSWORD = os.getenv('PASSWORD')
    DATABASE = os.getenv('DB_NAME_PROD')

    engine = conn_mysql(HOST, USER, PASSWORD, DATABASE)
    df = leitura()
    df = mean_rating(df)
    df = price_symbol(df)
    df = integer_null(df)
    df = date_column(df)
    load_csv(df, engine)
