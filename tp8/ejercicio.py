import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def mostrar_informacion_alumno():
    with st.container():
        st.markdown('**Legajo:** 58761')
        st.markdown('**Nombre:** Lautaro Juarez')
        st.markdown('**Comisión:** C5')

def cargar_datos(file):
    try:
        df = pd.read_csv(file)
        df['Año-Mes'] = pd.to_datetime(df['Año'].astype(str) + '-' + df['Mes'].astype(str))
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return None

def calcular_estadisticas(df, sucursal_seleccionada):
    if sucursal_seleccionada != 'Todas':
        df = df[df['Sucursal'] == sucursal_seleccionada]
    
    estadisticas = df.groupby('Producto').agg({
        'Ingreso_total': 'sum',
        'Unidades_vendidas': 'sum',
        'Costo_total': 'sum'
    }).reset_index()
    
    estadisticas['Precio Promedio'] = estadisticas['Ingreso_total'] / estadisticas['Unidades_vendidas']
    estadisticas['Margen Promedio'] = (estadisticas['Ingreso_total'] - estadisticas['Costo_total']) / estadisticas['Ingreso_total']
    estadisticas['Unidades Vendidas'] = estadisticas['Unidades_vendidas']
    
    # Agregar cambios simulados
    estadisticas['Cambio Precio'] = np.random.uniform(-30, 30, size=len(estadisticas))
    estadisticas['Cambio Margen'] = np.random.uniform(-5, 5, size=len(estadisticas))
    estadisticas['Cambio Unidades'] = np.random.uniform(-10, 10, size=len(estadisticas))

    return estadisticas


def graficar_evolucion(df, producto):
    df_producto = df[df['Producto'] == producto].sort_values('Año-Mes')
    x = np.arange(len(df_producto))
    y = df_producto['Unidades_vendidas'].values

    tendencia = np.poly1d(np.polyfit(x, y, 1))(x)
    
    plt.figure(figsize=(10, 6))  
    plt.plot(df_producto['Año-Mes'], y, label=producto, color='#3b87bb', linewidth=2)  # Línea principal
    plt.plot(df_producto['Año-Mes'], tendencia, label='Tendencia', color='red', linestyle='--', linewidth=2)  # Línea de tendencia
    
    plt.xlabel("Año-Mes", fontsize=12)
    plt.ylabel("Unidades Vendidas", fontsize=12)
    plt.title("Evolución de Ventas Mensual", fontsize=14, fontweight="bold")
    plt.legend(fontsize=10)
    
    y_min = int(np.floor(y.min() / 1000) * 1000)
    y_max = int(np.ceil(y.max() / 1000) * 1000)   
    y_ticks = np.arange(y_min, y_max + 1000, 1000)  
    plt.yticks(y_ticks, [f"{int(tick):,}" for tick in y_ticks], fontsize=10)  
    
    x_ticks = pd.date_range(start=df_producto['Año-Mes'].min(), 
                            end=df_producto['Año-Mes'].max(), 
                            freq='YS')  
    x_lines = pd.date_range(start=df_producto['Año-Mes'].min(), 
                            end=df_producto['Año-Mes'].max(), 
                            freq='MS')  
    
    plt.xticks(x_ticks, [date.strftime("%Y") for date in x_ticks], rotation=0, fontsize=10)

    plt.grid(visible=True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
    for date in x_lines:
        plt.axvline(date, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)  # Líneas verticales mensuales
    
    plt.tight_layout()  

    st.pyplot(plt)  



def main():
    st.title("Análisis de Ventas")
    mostrar_informacion_alumno()
    
    file = st.sidebar.file_uploader("Subir archivo CSV", type=["csv"])
    sucursal_seleccionada = st.sidebar.selectbox(
        "Seleccionar Sucursal",
        options=['Todas', 'Sucursal Norte', 'Sucursal Centro', 'Sucursal Sur']
    )
    
    if file:
        df = cargar_datos(file)
        if df is not None:
            st.header(f"Datos de {'Todas las Sucursales' if sucursal_seleccionada == 'Todas' else sucursal_seleccionada}")
            
            estadisticas = calcular_estadisticas(df, sucursal_seleccionada)
            
            for _, row in estadisticas.iterrows():
                producto = row['Producto']
                
                df_producto_filtrado = df[df['Producto'] == producto]
                if sucursal_seleccionada != 'Todas':
                    df_producto_filtrado = df_producto_filtrado[df_producto_filtrado['Sucursal'] == sucursal_seleccionada]

                st.markdown(f"### {producto}")

                col1, col2 = st.columns([1, 2])  

                with col1:
                    st.metric(
                        "Precio Promedio",
                        f"${row['Precio Promedio']:.2f}",
                        f"{row['Cambio Precio']:.2f}%"
                    )
                    st.metric(
                        "Margen Promedio",
                        f"{row['Margen Promedio']:.2%}",
                        f"{row['Cambio Margen']:.2f}%"
                    )
                    st.metric(
                        "Unidades Vendidas",
                        f"{int(row['Unidades Vendidas']):,}",
                        f"{row['Cambio Unidades']:.2f}%"
                    )

                with col2:
                    graficar_evolucion(df_producto_filtrado, producto)

if __name__ == "__main__":
    main()
