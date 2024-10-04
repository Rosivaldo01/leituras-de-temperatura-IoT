import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
import json

# Configurações do Supabase
SUPABASE_URL = "https://ogxcebxdhuehtecigwcl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9neGNlYnhkaHVlaHRlY2lnd2NsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc3NDQyODgsImV4cCI6MjA0MzMyMDI4OH0.y-MSE38nJ-9Ll7kaazpC4j-a42BzW0vbqKMxe3VVLrI"

TABLE_NAME = "temperature_reading"  # Nome da tabela no Supabase


# Função para conectar ao Supabase
@st.cache_resource
def get_supabase_client():
  return create_client(SUPABASE_URL, SUPABASE_KEY)


# Função para carregar dados do Supabase
def load_data(supabase):
  response = supabase.table(TABLE_NAME).select("data_line").execute()
  data = response.data
  if not data:
    st.error("Nenhum dado encontrado.")
    return pd.DataFrame()

  # Extrai a coluna 'data_line' sem precisar de json.loads(), já que 'data_line' é um dicionário
  data_lines = [item['data_line'] for item in data]
  return pd.DataFrame(data_lines)


# Função para criar visualizações
def create_views(df):

  # View 1: Média de Temperaturas por Quarto
  st.subheader("Média de Temperaturas por Quarto")

  fig_avg_temp = px.bar(df,
                        x='room_id/id',
                        y='temp',
                        title='Média de Temperaturas por Quarto')
  st.plotly_chart(fig_avg_temp)

  # View 2: Contagem de Entradas e Saídas
  st.subheader("Contagem de Entradas e Saídas")

  fig_count_in_out = px.pie(df,
                            names='out/in',
                            values='temp',
                            title='Contagem de Entradas e Saídas')
  st.plotly_chart(fig_count_in_out)

  # View 3: Temperaturas Registradas por Data
  st.header("Temperaturas Registradas por Data")

  fig_temp_by_date = px.line(df, x='noted_date', y='temp', title='Temperaturas Registradas por Data')
  st.plotly_chart(fig_temp_by_date)
  

# Função principal
def main():

  st.title("Análise de Temperaturas")

  # Conectando ao banco de dados
  supabase = get_supabase_client()

  # Carregar os dados da coluna 'data_line'
  df = load_data(supabase)

  if not df.empty:
    # Converta a coluna 'Date/Time' para o formato datetime
    # df["Date/Time"] = pd.to_datetime(df["Date/Time"], format="%m/%d/%Y %H:%M")

    # Converta a coluna 'Date/Time' para o formato datetime
    df["noted_date"] = pd.to_datetime(df["noted_date"], format="%d-%m-%Y %H:%M")
    
    # Crie as visualizações
    create_views(df)
  else:
    st.write("Nenhum dado disponível para visualização.")


if __name__ == "__main__":
  main()
