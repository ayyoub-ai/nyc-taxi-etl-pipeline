import pandas as pd
from sqlalchemy import create_engine
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    
    # Le nom du fichier CSV téléchargé
    csv_name = 'output.csv.gz'

    # 1. Télécharger le fichier (si tu es en local, sinon on peut lire directement l'URL)
    # Pour simplifier dans Codespaces, on va lire directement depuis l'URL
    print(f"Connecting to database at {host}:{port}...")
    
    # 2. Créer le moteur SQLAlchemy
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()
    print("Connection established successfully!")

    # 3. Lire les données par chunks
    df_iter = pd.read_csv(url, iterator=True, chunksize=100000)

    # Récupérer le premier chunk pour créer la table
    df = next(df_iter)
    
    # Convertir les colonnes de date en format datetime
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # Créer la table dans PostgreSQL (écrase si elle existe déjà)
    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')
    print(f"Table '{table_name}' created.")

    # Insérer le premier chunk
    df.to_sql(name=table_name, con=engine, if_exists='append')
    print("First chunk inserted.")

    # 4. Boucle pour insérer les chunks suivants
    for df in df_iter:
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        
        df.to_sql(name=table_name, con=engine, if_exists='append')
        print("Inserted another chunk...")

    print("Data ingestion completed!")

if __name__ == '__main__':
    # Configuration des arguments en ligne de commande
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='username for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()
    main(args)