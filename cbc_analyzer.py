import streamlit as st
import pandas as pd

def convert_hdl(hdl_mg_dl):
    return hdl_mg_dl / 38.67

def calculate_indices(neut, lymph, mono, platelets, rdw, hdl_mg_dl):
    hdl = convert_hdl(hdl_mg_dl)
    nlr = neut / lymph
    plr = platelets / lymph
    sii = (neut * platelets) / lymph
    siri = (neut * mono) / lymph
    aisi = (neut * platelets * mono) / lymph
    mhr = mono / hdl if hdl > 0 else float('inf')

    interpretations = {
        'NLR': interpret_nlr(nlr),
        'PLR': interpret_plr(plr),
        'SII': interpret_sii(sii),
        'SIRI': interpret_siri(siri),
        'AISI': interpret_aisi(aisi),
        'RDW': interpret_rdw(rdw),
        'MHR': interpret_mhr(mhr)
    }

    data = {
        'Index': ['NLR', 'PLR', 'SII', 'SIRI', 'AISI', 'RDW', 'MHR'],
        'Value': [round(nlr, 2), round(plr, 2), round(sii, 2), round(siri, 2), round(aisi), f"{rdw}%", round(mhr, 2)],
        'Interpretation': [interpretations[key] for key in ['NLR', 'PLR', 'SII', 'SIRI', 'AISI', 'RDW', 'MHR']]
    }

    return pd.DataFrame(data)

def interpret_nlr(value):
    if value < 2.0:
        return 'Normal'
    elif value <= 3.5:
        return 'Mild–Moderate inflammation'
    else:
        return 'Significant inflammation'

def interpret_plr(value):
    if value < 100:
        return 'Normal'
    elif value <= 150:
        return 'Mild elevation'
    else:
        return 'Significant inflammation / thrombosis risk'

def interpret_sii(value):
    if value < 300:
        return 'Normal'
    elif value <= 600:
        return 'Moderate inflammation'
    else:
        return 'Severe systemic inflammation'

def interpret_siri(value):
    if value < 0.8:
        return 'Normal'
    elif value <= 1.5:
        return 'Moderate inflammation'
    else:
        return 'High inflammation'

def interpret_aisi(value):
    if value < 300000:
        return 'Normal'
    elif value <= 600000:
        return 'Moderate inflammation'
    else:
        return 'Severe inflammation'

def interpret_rdw(value):
    if value < 13.5:
        return 'Normal'
    elif value <= 15:
        return 'Mild elevation'
    else:
        return 'High inflammation or poor prognosis'

def interpret_mhr(value):
    if value < 8:
        return 'Normal'
    elif value <= 15:
        return 'Moderate cardiometabolic risk'
    else:
        return 'High systemic inflammation / atherosclerosis risk'

# Streamlit UI
st.title("CBC-Derived Inflammation Index Analyzer")

with st.form("cbc_form"):
    st.write("### Enter CBC and HDL values")
    neut = st.number_input("Neutrophils (×10³/µL)", min_value=0.0, step=0.1)
    lymph = st.number_input("Lymphocytes (×10³/µL)", min_value=0.1, step=0.1)
    mono = st.number_input("Monocytes (×10³/µL)", min_value=0.0, step=0.1)
    platelets = st.number_input("Platelets (×10³/µL)", min_value=0.0, step=1.0)
    rdw = st.number_input("RDW (%)", min_value=0.0, step=0.1)
    hdl_mg_dl = st.number_input("HDL (mg/dL)", min_value=0.0, step=0.1)

    submitted = st.form_submit_button("Analyze")

if submitted:
    result_df = calculate_indices(neut, lymph, mono, platelets, rdw, hdl_mg_dl)
    st.write("### Results")
    st.dataframe(result_df, use_container_width=True)
    st.write("📝 **Summary:**")
    st.write("CBC-derived indices suggest systemic inflammation based on NLR, PLR, SII, and SIRI. Interpretation should be correlated with clinical context.")
