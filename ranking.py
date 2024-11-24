# JOC DE PROVES PER FER RANQUINGS

import pandas as pd
import streamlit as st

def pantalla_inici():
    st.title("Creació de Rànquing")
    st.session_state.nom_ranquing = st.text_input("Introdueix el nom del rànquing:")
    st.session_state.df = pd.DataFrame(columns=["elements"])
    st.session_state.uploaded = False   
    if st.button("Comença"):
        st.session_state.page = "elements"



def pantalla_elements():
    
    st.title(st.session_state.nom_ranquing)
    
    st.subheader(":violet[Pots importar una llista ja feta, modificant el que vulguis!]")
    uploaded_file = st.file_uploader("Tria un document CSV", type=['csv'])

    if uploaded_file is not None and not st.session_state.uploaded:
        try:
            # Llegir el fitxer CSV i carregar-lo com un dataframe
            df_upload = pd.read_csv(uploaded_file)
            st.session_state.df = pd.concat(
                [st.session_state.df, df_upload], ignore_index=True
            )
            st.session_state.uploaded = True
            if 'pesos' in st.session_state.df['elements'].values:
            # Guardar la fila com a diccionari dins de st.session_state.pesos
                fila_pesos = st.session_state.df[st.session_state.df['elements'] == 'pesos']
                st.session_state.pesos = fila_pesos.iloc[0].to_dict()
                st.session_state.df = st.session_state.df[st.session_state.df["elements"] != "pesos"]
            st.rerun()

            # Mostra una vista prèvia del dataframe
            
        except Exception as e:
            st.error(f"Error en llegir el fitxer: {e}")
    
    st.header(":red[Llista d'elements:]")
    st.dataframe(st.session_state.df)
    
    st.header(":blue[Afegeix un element]")
    with st.form("add_row_form"):
        # Generar inputs dinàmicament segons les columnes del DataFrame
        inputs = {
            "elements": st.text_input("Afegeix un element")
        }
        submitted = st.form_submit_button("Afegeix")

        if submitted:
            # Crear una nova fila amb els valors introduïts
            for i in st.session_state.df.columns:
                if i == "elements": continue
                inputs[i] = 5
            new_row = pd.DataFrame([inputs])

            # Afegir la nova fila al dataframe
            st.session_state.df = pd.concat(
                [st.session_state.df, new_row], ignore_index=True
            )

            st.success("Element afegit!")
            st.rerun()
            
            
        
    row_to_delete = st.selectbox(
        "Esborrar un element:",
        options=[col for col in st.session_state.df['elements']]
        )

        # Botó per esborrar la columna seleccionada
    if st.button("Esborrar element"):
        st.session_state.df = st.session_state.df[st.session_state.df["elements"] != row_to_delete]
        st.session_state.df = st.session_state.df.reset_index(drop=True)
        st.rerun()
        
    st.subheader(":blue[Canviar nom del rànquing]")
    with st.form("nomranquing"):
        # Generar inputs dinàmicament segons les columnes del DataFrame
        inp = st.text_input("Nom del rànquing")
        sub = st.form_submit_button("Canvia")

        if sub:     
            st.session_state.nom_ranquing = inp
            st.rerun()
    
    if st.button("Afegir metriques",type="primary"):
        st.session_state.page ="metriques"
    
    
    if st.button("Reinicia rànquing"):
        st.session_state.page = "inici"

def pantalla_metriques():
        
        # Mostra el dataframe actual
    st.title(st.session_state.nom_ranquing)
    st.header(":red[Taula actual:]")
    st.dataframe(st.session_state.df)
    st.session_state.new_col_values = [5] * len(st.session_state.df)
    # EDITAR ELEMENTS
    if st.button("Editar elements"):
        st.session_state.page ="elements"
        
    st.subheader(":violet[Pots afegir, editar i eliminar les mètriques de la taula!]")
        
    # AFEGIR COLUMNA
    # Introdueix el nom de la nova columna
    st.session_state.new_col_name = st.text_input(
        "Afegir la columna:",
        value=st.session_state.new_col_name
    )                        
    # Si s'ha proporcionat el nom, crea sliders per a cada fila
    if st.session_state.new_col_name:
        st.write(f"Defineix els valors per a la nova columna: {st.session_state.new_col_name}")

        for idx, row in st.session_state.df.iterrows():
            st.session_state.new_col_values[idx] = st.slider(
                label=f"Valor per a {row['elements']}",
                min_value=0,
                max_value=10,
                value=5,
                key=f"sliderc_{idx}"
            )

        # Afegeix la columna al dataframe quan es premi el botó
        if st.button("Afegir columna"):
            st.session_state.df[st.session_state.new_col_name] = st.session_state.new_col_values
            st.success(f"Columna '{st.session_state.new_col_name}' afegida amb èxit!")
            # Reinicia els valors per a una nova entrada
            st.session_state.new_col_name = ""
#                    st.session_state.new_col_values = [0] * len(st.session_state.df)
            st.rerun()
            
    # EDITAR COLUMNA
    if not st.session_state.editing_column:
        st.session_state.column_to_edit = st.selectbox(
        "Editar una columna:",
        options=[col for col in st.session_state.df.columns if col != "elements"]
        )
        if st.button("Editar columna"):
            st.session_state.editing_column = True
            st.rerun()
    else:  
        st.write(f"Defineix els nous valors per a la columna: {st.session_state.new_col_name}")
        #st.session_state.new_col_values = st.session_state.df[st.session_state.column_to_edit]
        
        values_prev = st.session_state.df[st.session_state.column_to_edit]
        
        for idx, row in st.session_state.df.iterrows():
            try:
                st.session_state.new_col_values[idx] = st.slider(
                    label=f"Valor per a {row['elements']}",
                    min_value=0,
                    max_value=10,
                    step=1,
                    value=int(values_prev[idx]),
                    key=f"slidere_{idx}"
                )
            except:
                    st.session_state.new_col_values[idx] = st.slider(
                    label=f"Valor per a {row['elements']}",
                    min_value=0,
                    max_value=10,
                    step=1,
                    value=5,
                    key=f"slidere_{idx}"
                )
        if st.button("Editar columna"):
            st.session_state.df[st.session_state.column_to_edit] = st.session_state.new_col_values
            st.success(f"Columna '{st.session_state.column_to_edit}' editada amb èxit!")
            st.session_state.editing_column = False
            st.rerun()
    
    # ESBORRAR COLUMNA
    column_to_delete = st.selectbox(
    "Esborrar una columna:",
    options=[col for col in st.session_state.df.columns if col != "elements"]
    )

    # Botó per esborrar la columna seleccionada
    if st.button("Esborrar columna"):
            st.session_state.df.drop(columns=[column_to_delete], inplace=True)
            st.success(f"La columna '{column_to_delete}' s'ha esborrat correctament!")
            st.rerun()
    
    st.subheader(":violet[Assigna un valor pels pesos de cada mètrica abans de calcular el rànquing!]")
    
    # EDITAR PESOS
    if not st.session_state.editing_pesos:
        # Mostra el vector actual
        st.header(":blue[Pesos:]")
        for k, v in st.session_state.pesos.items():
            try:
                if k == "Posicio ranquing" or k  == "Puntuacio": continue
                st.write(k, ":", v)
            except:
                continue

        # Botó per començar a editar
        if st.button("Editar pesos"):
            st.session_state.editing_pesos = True
            st.rerun()
    else:
        # Mostra sliders per editar els valors del vector
        st.session_state.newpesos = {col : 0.0 for col in st.session_state.df.columns}
        st.write("Modifica els valors amb els sliders:")
        for i, col in enumerate(st.session_state.df.keys()):
            if i == 0 or col == "Posicio ranquing" or col == "Puntuacio": continue
            try:
                st.session_state.newpesos[col] = st.slider(
                    f"Pes de {col}",
                    min_value=-1.0,
                    max_value=1.0,
                    step=0.05,
                    value=st.session_state.pesos[col],
                    key=f"slider_{i}"
                )
            except:
                st.session_state.newpesos[col] = st.slider(
                    f"Pes de {col}",
                    min_value=-1.0,
                    max_value=1.0,
                    step=0.05,
                    value=0.0,
                    key=f"slider_{i}"
                )
        # Botó per guardar els canvis i tornar a la vista inicial
        if st.button("Guardar pesos"):
            st.session_state.editing_pesos = False
            st.session_state.pesos = st.session_state.newpesos
            st.rerun()


    # CALCULAR RANQUINGS
    if st.button("Calcular ranquing",type="primary"):
        # st.header(":red[Puntuacions]") # mostrar puntuacions juntament amb ranquing o no
        r = {}
        for i, row in st.session_state.df.iterrows():
            v = 0
            for k,j in enumerate(st.session_state.df.columns):
                if k == 0 or j == "Posicio ranquing" or j == "Puntuacio": continue
                v += st.session_state.pesos[j]*row[j]
            r[st.session_state.df['elements'][i]] = v
            # st.subheader(f"{st.session_state.df['elements'][i]} : {round(v,1)}",divider=True) # idem
        st.header(":red[Rànquing]")
        r2 = {}
        p = 1
        for key in sorted(r, key=r.get, reverse=True):
            r2[key] = p
            p+=1
            st.subheader(f'{p-1}: {key} ({round(r[key],1)})',divider=True)

        st.session_state.pesos['elements'] = 'pesos'
        nova_fila = pd.DataFrame([st.session_state.pesos])       
        st.session_state.df['Puntuacio'] = r.values()
        st.session_state.df["Posicio ranquing"] = st.session_state.df['elements'].map(r2)
        df2_csv = pd.concat([nova_fila, st.session_state.df], ignore_index=True)
        
        
        csv = df2_csv.to_csv(index=False)

        # Crea un botó de descàrrega
        st.download_button(
            label="Descarrega el CSV",
            data=csv,
            file_name=f'{st.session_state.nom_ranquing}.csv',
            mime='text/csv'
        )
        
    if st.button("Reinicia rànquing"):
        st.session_state.page = "inici"
    

def main():

    if "page" not in st.session_state:
        st.session_state.page = "inici"
    if "nom_ranquing" not in st.session_state:
        st.session_state.nom_ranquing = "Rànquing"
    if "noms" not in st.session_state:
        st.session_state.noms = []
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=["elements"])

    if "pesos" not in st.session_state:
        st.session_state.pesos = {}
    if "new_col_name" not in st.session_state:
        st.session_state.new_col_name = ""
    if "editing_pesos" not in st.session_state:
        st.session_state.editing_pesos = False
    if "editing_column" not in st.session_state:
        st.session_state.editing_column = False   
      
    
    # Primera pantalla: Nom del rànquing i nombre d'elements
    if st.session_state.page == "inici":
        pantalla_inici()

    # Segona pantalla: Afegir elements i mètrica
    elif st.session_state.page == "elements":
        pantalla_elements()
    
    elif st.session_state.page == "metriques":
        pantalla_metriques()
if __name__ == "__main__":
    main()