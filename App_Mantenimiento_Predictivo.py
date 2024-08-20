# Importamos las bibliotecas necesarias
import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Configuramos la página de Streamlit
st.set_page_config(page_title="App de predicción de mantenimiento de maquinas",
                   page_icon="assets/ahorra-energia.png",
                   layout="centered",
                   initial_sidebar_state="auto")

# Definimos el título y la descripción de la aplicación
st.title("App de predicción de mantenimiento en maquinas industriales")
st.markdown("""Esta aplicación predice si puede que ocurra una falla en la maquina basándose en tus datos ingresados. Esto indicara que si hay falla, deberia realizarse mantenimiento""")


st.title("Integrantes")


st.write("""
Ing. Alpaca Rendón, Jesús A.\n
Ing. Vargas Franco, Mauricio S.\n
Ing. Del Carpio Maraza Heberth E.\n
""")

from PIL import Image
image = Image.open("assets/mantenimiento.jpeg")
st.image(image, caption="App Mantenimiento Predictivo", use_column_width=True)

# Cargamos y mostramos un logo en la barra lateral
logo = "assets/logo.jpg"
st.sidebar.image(logo, width=150)
# Añadimos un encabezado para la sección de datos del usuario en la barra lateral
st.sidebar.header('Datos ingresados por el usuario')

# # Permitimos al usuario cargar un archivo CSV o ingresar datos manualmente
# uploaded_file = st.sidebar.file_uploader("Cargue su archivo CSV", type=["csv"])

# if uploaded_file is not None:
#     input_df = pd.read_csv(uploaded_file)
# else:
machine_options = np.array(["4","5","6","8","10","11","15","16","17","20","21","22","23","25"])
error_options = np.array(['0','1','2'])
error1_options = np.array(['0','1'])
models_options = np.array(['0','1'])
error2_options = np.array(['1','2'])
failure_options = np.array(['none','PART01','PART02','PART03','PART04'])
def user_input_features():
    # Creamos controles deslizantes y cuadros de selección para que el usuario ingrese datos
    #machine = st.sidebar.selectbox(label='Nro de Maquina', options=machine_options,placeholder='Seleccione una maquina')
    #fecha = st.sidebar.date_input(label='Fecha del Registro',value=datetime.date(2021, 7, 6), min_value=datetime.date(2021,1,3), max_value=datetime.date(2021,12,30))
    voltmean_3h = st.sidebar.slider('Voltage Prom 3h', 142.0, 221.0, 160.75)
    rotatemean_3h = st.sidebar.slider('Rotacion Prom 3h', 326.0, 541.0, 426.15)
    pressuremean_3h = st.sidebar.slider('Presion Prom 3h', 80.0, 136.0, 118.45)
    vibrationmean_3h = st.sidebar.slider('Vibracion Prom 3h', 42.0,65.0,57.49)
    voltsd_3h = st.sidebar.slider('Voltage SD 3h', 1.0, 50.0, 31.78)
    rotatesd_3h	= st.sidebar.slider('Rotacion SD 3h', 3.0, 145.0, 46.75)
    pressuresd_3h = st.sidebar.slider('Presion SD 3h', 0.1, 27.99, 15.41)	
    vibrationsd_3h = st.sidebar.slider('Vibracion SD 3h', 0.05, 15.99, 9.12)
    
    voltmean_24h = st.sidebar.slider('Voltage Prom 24h', 160.0, 206.0, 194.75)
    rotatemean_24h = st.sidebar.slider('Rotacion Prom 24h', 357.0, 479.0, 411.12)
    pressuremean_24h = st.sidebar.slider('Presion Prom 24h', 94.0, 126.0, 110.43)
    vibrationmean_24h = st.sidebar.slider('Vibracion Prom 24h', 47.0,61.0,49.67)
    voltsd_24h = st.sidebar.slider('Voltage SD 24h', 9.0, 21.0, 16.48)
    rotatesd_24h	= st.sidebar.slider('Rotacion SD 24h', 28.0, 73.0, 46.75)
    pressuresd_24h = st.sidebar.slider('Presion SD 24h', 5.8, 18.87, 11.40)	
    vibrationsd_24h = st.sidebar.slider('Vibracion SD 24h', 2.9, 8.1, 5.46)
        
    error1_count = st.sidebar.selectbox('Error Count 1',options=error_options)
    error2_count = st.sidebar.selectbox('Error Count 2',options=error1_options)
    error3_count = st.sidebar.selectbox('Error Count 3',options=error1_options)
    error4_count = st.sidebar.selectbox('Error Count 4',options=error1_options)
    error5_count = st.sidebar.selectbox('Error Count 5',options=error_options)
    model_part_1 = st.sidebar.slider('Part 1', 0.125, 233.0, 110.85)
    model_part_2 = st.sidebar.slider('Part 2', 0.125, 308.25, 267.15)
    model_part_3 = st.sidebar.slider('Part 3', 0.125, 289.0, 216.97)
    model_part_4 = st.sidebar.slider('Part 4', 0.125, 394.0, 297.61)
    age = st.sidebar.slider('Edad', 14, 20, 16)
    model_ALPHA_560_UNIVERSAL = st.sidebar.selectbox('model_ALPHA 560 UNIVERSAL',options=models_options)
    model_JACQUARD_TF = st.sidebar.selectbox('model_JACQUARD TF',options=models_options)
    model_NOVA_62 = st.sidebar.selectbox('model_NOVA 62',options=models_options)
    model_NOVA_6HS = st.sidebar.selectbox('model_NOVA 6HS',options=models_options)
    # failure = st.sidebar.selectbox('Fallo?',options=models_options)
    
    # Creamos un diccionario con los datos ingresados por el usuario
    data = {
            # 'Maquina': machine,
            # 'Fecha': fecha,
            'voltmean_3h': voltmean_3h,
            'rotatemean_3h': rotatemean_3h,
            'pressuremean_3h': pressuremean_3h,
            'vibrationmean_3h': vibrationmean_3h,
            'voltsd_3h': voltsd_3h,
            'rotatesd_3h': rotatesd_3h,
            'pressuresd_3h': pressuresd_3h,
            'vibrationsd_3h': vibrationsd_3h,
            'voltmean_24h': voltmean_24h,
            'rotatemean_24h': rotatemean_24h,
            'pressuremean_24h': pressuremean_24h,
            'vibrationmean_24h': vibrationmean_24h,
            'voltsd_24h': voltsd_24h,
            'rotatesd_24h': rotatesd_24h,
            'pressuresd_24h': pressuresd_24h,
            'vibrationsd_24h': vibrationsd_24h,
            'error1_count': error1_count,
            'error2_count': error2_count,
            'error3_count': error3_count,
            'error4_count': error4_count,
            'error5_count': error5_count,
            'Part_1': model_part_1,
            'Part_2': model_part_2,
            'Part_3': model_part_3,
            'Part_4': model_part_4,
            'age': age,
            'model_ALPHA 560 UNIVERSAL': model_ALPHA_560_UNIVERSAL,
            'model_JACQUARD TF': model_JACQUARD_TF,
            'model_NOVA 62': model_NOVA_62,
            'model_NOVA 6HS': model_NOVA_6HS
            # 'Fallo el componente?': failure
            }
    # Convertimos el diccionario en un DataFrame
    features = pd.DataFrame(data, index=[0], dtype=float)
    return features

input_df = user_input_features()

# Seleccionamos solo la primera fila
input_df = input_df[:1]
# print(input_df.head())

st.subheader('Datos ingresados por el usuario')
# Mostramos los datos ingresados por el usuario en la página principal

# st.write('A la espera de que se cargue el archivo CSV. Actualmente usando parámetros de entrada de ejemplo (que se muestran a continuación).')
st.write(input_df)

# Cargamos el modelo de clasificación previamente entrenado
load_clf = pickle.load(open('assets/predictive_maintenance.pkl', 'rb'))

# Aplicamos el modelo para realizar predicciones en base a los datos ingresados
prediction = load_clf.predict(input_df)
msg = 'No se detecto pronto mantenimiento de la Maquina'
if prediction == 0:
    msg = 'Se requiere mantenimiento en la Parte 1 de la maquina'
elif prediction == 1:
    msg = 'Se requiere mantenimiento en la Parte 2 de la maquina'
elif prediction == 2:
    msg = 'Se requiere mantenimiento en la Parte 3 de la maquina'
elif prediction == 3:
    msg = 'Se requiere mantenimiento en la Parte 4 de la maquina'
else:
    print(msg)
    
# prediction_proba = load_clf.predict_proba(input_df)
print('Prediction: ' + str(prediction))
col1, col2 = st.columns(2)

with col1:
    st.subheader('Predicción')
    st.write('NO REQUIERE MANTENIMIENTO' if prediction==4 else 'REQUIERE MANTENIMIENTO')

# with col2:
#     st.subheader('Probabilidad de predicción')
#     st.write(prediction_proba)

st.subheader(msg)
st.markdown('---')