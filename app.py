from flask import Flask, jsonify
from flask_cors import CORS
import csv

app = Flask(__name__)
CORS(app)

# Função para ler os dados do arquivo CSV e formatá-los em um dicionário
def ler_dados_csv():
    localidades = []
    with open('estadios-alagoas-ibge-2022-novo.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            localidade = {
                "longitude": float(row['Longitude']),
                "latitude": float(row['Latitude']),
                "nome": row['nome'],
                "operaciona": row['operaciona'],
                "situacaofi": row['situacaofi'],
                "administra": row['administra'],
                "municipio": row['municipio'],
                "endereco": row['endereco']
            }
            localidades.append(localidade)
    return localidades

# Rota para fornecer os dados das localidades a partir do arquivo CSV
@app.route('/api/localidades')
def get_localidades():
    localidades = ler_dados_csv()
    return jsonify(localidades)

if __name__ == '__main__':
    app.run()

