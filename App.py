import streamlit as st
import pandas as pd
import plotly.express as px

# Configurazione Pagina
st.set_page_config(page_title="Filiera Puglia - Gestione Interna", layout="wide")

# --- SIMULAZIONE DATABASE (In produzione useresti un database reale come Supabase) ---
if 'data_approv' not in st.session_state:
    st.session_state.data_approv = pd.DataFrame(columns=["Azienda", "Data", "Tipo", "Risorsa", "Quantità"])
if 'data_pulizie' not in st.session_state:
    st.session_state.data_pulizie = pd.DataFrame(columns=["Azienda", "Data", "Area", "Operatore", "Stato"])

# --- SISTEMA DI LOGIN SEMPLICE ---
st.sidebar.title("🌿 Filiera Puglia Login")
user_role = st.sidebar.selectbox("Accedi come:", ["Capo Filiera (Admin)", "Azienda Agricola"])
access_code = st.sidebar.text_input("Codice Accesso", type="password")

# --- LOGICA APPLICAZIONE ---
if access_code == "123": # Codice di test
    
    if user_role == "Capo Filiera (Admin)":
        st.title("📊 Dashboard Capo Filiera")
        st.write("Benvenuto. Qui 
        hai il controllo totale su tutte le aziende.")
        
        # KPI Rapidi
        col1, col2, col3 = st.columns(3)
        col1.metric("Aziende Attive", "5")
        col2.metric("Approvvigionamenti Totali", f"{st.session_state.data_approv['Quantità'].sum()} kg")
        col3.metric("Alert Pulizie", "1", delta="-2", delta_color="inverse")

        # Grafico Approvvigionamenti
        if not st.session_state.data_approv.empty:
            st.subheader("Analisi Risorse per Azienda")
            fig = px.bar(st.session_state.data_approv, x="Azienda", y="Quantità", color="Risorsa")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nessun dato di approvvigionamento ancora caricato.")

    else:
        st.title("🚜 Area Azienda Agricola")
        azienda_nome = st.selectbox("Seleziona la tua Azienda:", ["Tenuta Coratina", "Masseria Gargano", "Orti di Polignano"])
        
        tab1, tab2, tab3 = st.tabs(["Approvvigionamento", "Pulizie", "Formazione"])
        
        with tab1:
            st.subheader("Carica Dati Approvvigionamento")
            with st.form("form_approv"):
                tipo = st.radio("Fonte", ["Auto-approvvigionamento", "Esterno"])
                risorsa = st.selectbox("Risorsa", ["Sementi", "Concimi", "Acqua", "Carburante"])
                qta = st.number_input("Quantità (kg/litri)", min_value=0)
                submit = st.form_submit_button("Salva Dato")
                if submit:
                    new_data = pd.DataFrame([[azienda_nome, pd.Timestamp.now(), tipo, risorsa, qta]], 
                                            columns=["Azienda", "Data", "Tipo", "Risorsa", "Quantità"])
                    st.session_state.data_approv = pd.concat([st.session_state.data_approv, new_data], ignore_index=True)
                    st.success("Dato salvato con successo!")

        with tab2:
            st.subheader("Registro Pulizie")
            area = st.text_input("Area Intervento (es. Magazzino)")
            operatore = st.text_input("Nome Operatore")
            if st.button("Conferma Pulizia Effettuata"):
                st.success(f"Pulizia registrata per {area} da {operatore}")

        with tab3:
            st.subheader("Stato Formazione")
            st.info("I tuoi prossimi corsi in scadenza: Sicurezza sul lavoro (Giugno 2026)")

else:
    st.warning("Inserisci il codice di accesso '123' nella barra laterale per entrare.")
