import pandas as pd

# Cargar el archivo CSV
df = pd.read_csv('INDUSTRIA DOWJONES2.csv')

# Convertir la columna de fecha a tipo datetime
df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%y')

# Eliminar el signo de dólar y las comas de la columna de valores y convertirlos a flotantes
df['Value'] = df['Value'].replace(r'[\$,]', '', regex=True).astype(float)

# Ordenar los datos por fecha
df.sort_values('Fecha', inplace=True)

# Calcular las medias móviles y la volatilidad
df['SMA_20'] = df['Value'].rolling(window=20).mean()
df['SMA_50'] = df['Value'].rolling(window=50).mean()
df['Volatilidad'] = df['Value'].rolling(window=20).std()

# Calcular la volatilidad promedio y máxima
df['Volatilidad_Promedio'] = df['Volatilidad'].rolling(window=50).mean()
volatilidad_maxima = df['Volatilidad'].max()

# Identificar las posibles fases de mercado
df['Acumulacion'] = (df['SMA_20'] < df['SMA_50']) & (df['Volatilidad'] < df['Volatilidad_Promedio'])
df['Participacion_Publica'] = (df['SMA_20'] > df['SMA_50'])
df['Distribucion'] = (df['SMA_20'] < df['SMA_50']) & (df['Volatilidad'] > df['Volatilidad_Promedio'])

# Seleccionar fechas para cada fase
fechas_acumulacion = df[df['Acumulacion']]['Fecha']
fechas_participacion = df[df['Participacion_Publica']]['Fecha']
fechas_distribucion = df[df['Distribucion']]['Fecha']

# Crear un DataFrame para las estadísticas de volatilidad
volatilidad_df = pd.DataFrame({
    'Estadistica': ['Promedio', 'Maxima'],
    'Volatilidad': [
        df['Volatilidad_Promedio'].iloc[-1],
        volatilidad_maxima
    ]
})

# Imprimir las fechas y las estadísticas de volatilidad
print("Fechas de Fases de Acumulación:")
print(fechas_acumulacion)
print("\nFechas de Fases de Participación Pública:")
print(fechas_participacion)
print("\nFechas de Fases de Distribución:")
print(fechas_distribucion)
print("\nEstadísticas de Volatilidad:")
print(volatilidad_df)



