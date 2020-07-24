import pandas as pd
from influxdb import DataFrameClient

def fetch_data():
  url = 'https://raw.githubusercontent.com/opendataddorf/od-resources/master/COVID_Duesseldorf.csv'
  return pd.read_csv(url, engine='python')

def prepare_data(data):
  df = data.copy()
  df.columns = df.columns.str.replace(' ', '')
  df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y')
  df = df.set_index("Datum")
  df = df.drop(columns=['DateiUhrzeit', 'Dateivom'])
  return df

def write_data_to_influxdb(data):
  influxClient = DataFrameClient("localhost", 8087, "admin", "admin", "corona_data")
  influxClient.drop_measurement("dus")
  influxClient.write_points(data, "dus")
  influxClient.close()

if __name__ == '__main__':
  data = fetch_data()
  prepared_data = prepare_data(data)
  write_data_to_influxdb(prepared_data)
  print("done")
