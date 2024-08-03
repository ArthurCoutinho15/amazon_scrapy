<h1>Web Scraping Notebooks Amazon</h1>
<h2>Descrição</h2>
<p>Este projeto realiza a coleta de dados de notebooks do site Amazon, transforma, e carrega esses dados em um banco MySQL.     
Em seguida, gera um dashboard interativo utilizando Streamlit para visualização da distribuilção de preços e avaliações.</p>
<h2>Configuração</h2>
<ol>
    <li>Clone esse repositório</li>
    <pre><code>https://github.com/ArthurCoutinho15/amazon_scrapy</code></pre>
    Instale as dependências necessárias:
    pip install -r requirements.txt

    Crie um arquivo .env na raiz do projeto com as seguintes variáveis:
    HOST=your_mysql_host
    USER=your_mysql_user
    PASSWORD=your_mysql_password
    DB_NAME_PROD=your_database_name
</ol>
<h2>Bibliotecas Utilizadas</h2>
<ul>
    <li>Selenium</li>
    <li>Pandas</li>
    <li>SQLAlchemy</li>
    <li>dotenv</li>
    <li>Streamlit</li>
</ul>
<h2>Execução</h2>
<li>Crie um banco de dados amazon e a seguinte tabela</li>
<pre><code>
    USE amazon;
    CREATE TABLE products(
    name varchar (150),
    price float, 
    rating int,
    mean_rating float,
    link varchar (200)
    );
</code></pre>
<h2>Utilização do Streamlit</h2>
<p>
    O Streamlit é utilizado para criar um dashboard interativo que mostra os dados de tênis vendidos no mercado livre e seus KPI's.
</p>

<h3>Execução do Streamlit</h3>
<ol>
    <li>Certifique-se de que o ambiente virtual está ativado.</li>
    <li>Execute o comando para iniciar o Streamlit:
        <pre>
streamlit run script.py
        </pre>
        <p>Substitua <code>script.py</code> pelo nome do arquivo Python que contém o código acima.</p>
    </li>
    <li>Abra o navegador e acesse <a href="http://localhost:8501">http://localhost:8501</a> para visualizar o dashboard.</li>
</ol>
