# JOC DE PROVES PER FER RANQUINGS

import pandas as pd
import streamlit as st

def pantalla_inici():
    st.title("Creació de Rànquing")
        
    st.session_state.df = pd.DataFrame(columns=["elements"])
    st.session_state.uploaded = False  
    st.markdown("""
    <style>
    div.stButton > button {
        font-size: 40px !important;
        height: 180px;
        width: 100%;
        background-color: #28948c;
        color: white;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    div.stButton > button:active {
        transform: translateY(0px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    if st.button(r"$\textsf{Crear rànquing}$",
        use_container_width=True, icon=":material/star:"): 
        st.session_state.nou_r = "Importar llista d'elements"
        st.session_state.page = "nom"
    
    if st.button(r"$\textsf{Importar rànquing}$",use_container_width=True,icon=":material/restart_alt:"):
        st.session_state.nou_r = "Importar rànquing"
        st.session_state.page = "elements"
        
def pantalla_nom_ranquing():
    st.title("Nom del Rànquing")
    st.session_state.nom_ranquing = st.text_input("Introdueix el nom del rànquing:")
    if st.button("Comença"):
        st.session_state.page = "elements"
        
    if st.button("Tornar"):
        st.session_state.page = "inici"

def pantalla_elements():
    
    #st.title(st.session_state.nom_ranquing)
    st.markdown(f"<h1 style='text-align: center; color: black;'>{st.session_state.nom_ranquing}</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2,gap='medium')
    with col1:
        st.subheader(f":blue[{st.session_state.nou_r}]")
        uploaded_file = st.file_uploader("Tria un document CSV", type=['csv'])

        if uploaded_file is not None and not st.session_state.uploaded:
            try:
                # Llegir el fitxer CSV i carregar-lo com un dataframe
                if st.session_state.nou_r != "Importar llista d'elements":
                    st.session_state.nom_ranquing = uploaded_file.name[:-4]
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
        
        
        st.subheader(":blue[Afegir elements]")
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
    with col2:                
        st.subheader(":blue[Llista d'elements:]")
        st.dataframe(st.session_state.df)
        
        # ESBORRAR ELEMENTS 
        row_to_delete = st.selectbox(
            "Esborrar un element:",
            options=[col for col in st.session_state.df['elements']]
            )

            # Botó per esborrar la metrica seleccionada
        if st.button("Esborrar element"):
            st.session_state.df = st.session_state.df[st.session_state.df["elements"] != row_to_delete]
            st.session_state.df = st.session_state.df.reset_index(drop=True)
            st.rerun()
        
    
    if st.button("Següent",type="primary"):
        st.session_state.page ="metriques"
    
    if st.button("Canviar el nom del rànquing"):
        st.session_state.page = "nom"
    
    if st.button("Tornar a pantalla d'inici"):
        st.session_state.page = "inici"

def pantalla_metriques():
        
        # Mostra el dataframe actual
    st.markdown(f"<h1 style='text-align: center; color: black;'>{st.session_state.nom_ranquing}</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap='large')
    st.session_state.new_col_values = [5 for _ in st.session_state.df.iterrows()]
    
    with col1:
        st.header(":blue[Editar les mètriques]")

        # AFEGIR metrica
        # Introdueix el nom de la nova metrica
        st.session_state.new_col_name = st.text_input(
            "Afegir la mètrica:",
            value=st.session_state.new_col_name
        )                        
        # Si s'ha proporcionat el nom, crea sliders per a cada fila
        if st.session_state.new_col_name:
            st.write(f"Defineix els valors per a la nova metrica: {st.session_state.new_col_name}")

            for idx, row in st.session_state.df.iterrows():
                
                st.session_state.new_col_values[idx-1] = st.slider(
                    label=f"Valor per a {row['elements']}",
                    min_value=0,
                    max_value=10,
                    value=5,
                    key=f"sliderc_{idx}"
                )

            # Afegeix la metrica al dataframe quan es premi el botó
            if st.button("Afegir mètrica"):
                st.session_state.df[st.session_state.new_col_name] = st.session_state.new_col_values
                st.success(f"Mètrica '{st.session_state.new_col_name}' afegida amb èxit!")
                # Reinicia els valors per a una nova entrada
                st.session_state.new_col_name = ""
    #                    st.session_state.new_col_values = [0] * len(st.session_state.df)
                st.rerun()
                
        # EDITAR metrica
        if not st.session_state.editing_column:
            st.session_state.column_to_edit = st.selectbox(
            "Editar una mètrica:",
            options=[col for col in st.session_state.df.columns if col != "elements"]
            )
            if st.button("Editar mètrica"):
                st.session_state.editing_column = True
                st.rerun()
        else:  
            st.write(f"Defineix els nous valors per a la mètrica: {st.session_state.new_col_name}")
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
            if st.button("Editar mètrica"):
                st.session_state.df[st.session_state.column_to_edit] = st.session_state.new_col_values
                st.success(f"Mètrica '{st.session_state.column_to_edit}' editada amb èxit!")
                st.session_state.editing_column = False
                st.rerun()
        
        # ESBORRAR metrica
        column_to_delete = st.selectbox(
        "Esborrar una mètrica:",
        options=[col for col in st.session_state.df.columns if col != "elements"]
        )

        # Botó per esborrar la metrica seleccionada
        if st.button("Esborrar mètrica"):
                st.session_state.df.drop(columns=[column_to_delete], inplace=True)
                st.success(f"La mètrica '{column_to_delete}' s'ha esborrat correctament!")
                st.rerun()
    
    #st.subheader(":blue[Editar els pesos de les mètriques]")
    
        # EDITAR PESOS
        if not st.session_state.editing_pesos:
            # Mostra el vector actual
            st.header(":blue[Pesos:]")
            for k, v in st.session_state.pesos.items():
                try:
                    if k == "Posicio ranquing" or k  == "Puntuacio" or k=="elements": continue
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

    with col2:
        st.header(":blue[Taula actual:]")
        st.dataframe(st.session_state.df)
        # EDITAR ELEMENTS
        if st.button("Editar elements"):
            st.session_state.page ="elements"
    with col1:
    # CALCULAR RANQUINGS
        if st.button("Calcular rànquing",type="primary"):
            # st.header(":red[Puntuacions]") # mostrar puntuacions juntament amb ranquing o no
            with col2:
                r = {}
                for i, row in st.session_state.df.iterrows():
                    v = 0
                    for k,j in enumerate(st.session_state.df.columns):
                        if k == 0 or j == "Posicio ranquing" or j == "Puntuacio": continue
                        v += st.session_state.pesos[j]*row[j]
                    r[st.session_state.df['elements'][i]] = v
                
                st.header(":blue[Rànquing]",divider="gray")
                r2 = {}
                p = 1
                for key in sorted(r, key=r.get, reverse=True):
                    r2[key] = p
                    p+=1
                    st.subheader(f'**{p-1}: {key}** ({round(r[key],1)})',divider="blue")

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
    if st.button("Canviar el nom del rànquing"):
        st.session_state.page = "nom"
    if st.button("Tornar a pantalla d'inici"):
        st.session_state.page = "inici"
    

def main():
    st.set_page_config(layout="wide")

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
    
    elif st.session_state.page == "nom":
        pantalla_nom_ranquing()

    # Segona pantalla: Afegir elements i mètrica
    elif st.session_state.page == "elements":
        pantalla_elements()
    
    elif st.session_state.page == "metriques":
        pantalla_metriques()
if __name__ == "__main__":
    main()