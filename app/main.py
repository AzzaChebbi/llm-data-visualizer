import pandas as pd
import streamlit as st
import traceback
from llm_integration import call_llm_for_viz
import matplotlib.pyplot as plt
import seaborn as sns

def execute_viz_code(viz_responses, df):
    """
    Execute multiple visualization codes and display them with their interpretations in Streamlit.
    """
    try:
        exec_globals = {"df": df, "st": st, "plt": plt, "sns": sns, "__name__": "__main__"}

        if not viz_responses or not isinstance(viz_responses, list):
            st.error("⚠️ Erreur: Aucun code de visualisation valide reçu.")
            return

        for idx, viz_response in enumerate(viz_responses):
            if not isinstance(viz_response, dict) or "code" not in viz_response or "interpretation" not in viz_response:
                continue  # Ignore invalid responses
            
            viz_code = viz_response["code"]
            explanation = viz_response["interpretation"]

            st.subheader(f"📊 Visualisation {idx+1}")

            try:
                exec(viz_code, exec_globals)
                st.pyplot(plt)
                plt.clf()  # Nettoyer la figure après chaque visualisation
            
                # Afficher l'explication de la visualisation
                if explanation:
                    st.markdown(f"**🧐 Interprétation:** {explanation}")
            
            except Exception as e:
                st.error(f"⚠️ Erreur lors de l'exécution de la visualisation: {e}")
                st.text(traceback.format_exc())

    except Exception as e:
        st.error(f"⚠️ Erreur globale: {e}")
        st.text(traceback.format_exc())

def main():
    st.title("🔍 AI-Powered Data Visualization")

    # File uploader
    uploaded_file = st.file_uploader("📂 Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### 📄 Aperçu du dataset :", df.head())

        # User request
        user_request = st.text_input("📝 Décrivez votre requête de visualisation")

        if st.button("🚀 Générer des visualisations") and user_request:
            st.info("🔄 Génération en cours...")

            visualization_responses = call_llm_for_viz(df, user_request)

            # Exécuter et afficher les visualisations
            execute_viz_code(visualization_responses, df)

if __name__ == "__main__":
    main()
