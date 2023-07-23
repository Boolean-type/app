from flask import Flask, render_template, request
from datetime import datetime
from flask import flash, redirect, url_for
import os
import pandas as pd
import plotly.graph_objs as go

app = Flask(__name__)

# Generar una clave secreta aleatoria
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')



@app.route('/mostrar_prediccion', methods=['POST'])
def mostrar_prediccion():
    fecha_inicio = request.form['fecha_inicio']
    fecha_fin = request.form['fecha_fin']

    # Verificar si las fechas están en el formato adecuado (YYYY-MM-DD)
    try:
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
    except ValueError:
        error_msg = 'Formato de fecha incorrecto. Utiliza el formato YYYY-MM-DD.'
        flash(error_msg)
        return redirect(url_for('servicios'))

    # Verificar si las fechas cumplen con las restricciones (entre 2018 y 2022)
    if fecha_inicio.year < 2018 or fecha_inicio.year > 2022 or fecha_fin.year < 2018 or fecha_fin.year > 2022:
        error_msg = 'Las fechas deben estar entre 2018 y 2022.'
        flash(error_msg)
        return redirect(url_for('servicios'))

    # Cóodigo generador del gráfico
   
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    # Carga los datos desde el archivo Excel 
    excel_file_path = os.path.join('data', 'marginal_price.xlsx')
    df_final = pd.read_excel(excel_file_path)

    # Filtra los datos en el DataFrame en base al rango de fechas 
    df_filtered = df_final[(df_final['date'] >= fecha_inicio) & (df_final['date'] <= fecha_fin)]

    # Código para generar el gráfico con Plotly 
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_filtered['date'], y=df_filtered['marginalES'], mode='lines+markers', name='Marginal ES'))
    fig.update_layout(title='Gráfico de Precios Marginales mercado español', xaxis_title='Fecha', yaxis_title='Precio €/MWh')
    
    # Convierte el gráfico en una representación JSON para pasarlo a la plantilla
    graph_json = fig.to_json()

    return render_template('servicios.html', graph_json=graph_json)





if __name__ == '__main__':
    app.run()
