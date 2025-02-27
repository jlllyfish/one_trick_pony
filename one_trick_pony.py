import streamlit as st
import pandas as pd
import base64
import re
from datetime import datetime

st.set_page_config(page_title="Gestion des groupes d'instructeurs", layout="wide")

# Fonction pour télécharger le fichier CSV
def get_csv_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Télécharger le fichier CSV</a>'
    return href

# Fonction pour valider un email avec regex
def is_valid_email(email):
    # Regex pour validation d'email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Titre de l'application
st.title("Gestion des groupes d'instructeurs")

# Sidebar pour l'importation du fichier
st.sidebar.header("Importation du fichier")

# Upload du fichier CSV
uploaded_file = st.sidebar.file_uploader("Importer le fichier CSV Démarches simplifiées (groupe instructeur)", type=['csv'])

# Section principale - Emails récurrents
st.header("1. Emails récurrents (pour tous les groupes)")

# Initialiser la zone de texte pour les emails récurrents si elle n'existe pas
if 'recurring_emails_text' not in st.session_state:
    st.session_state.recurring_emails_text = ""

# Créer un champ de texte pour les emails récurrents
recurring_emails_text = st.text_area(
    "Entrez les emails récurrents (un par ligne)",
    value=st.session_state.recurring_emails_text,
    height=200,
    placeholder="exemple@agriculture.gouv.fr\nautre.email@agriculture.gouv.fr"
)

# Mettre à jour la session state
st.session_state.recurring_emails_text = recurring_emails_text

# Extraire et valider les emails
emails_list = [email.strip() for email in recurring_emails_text.split('\n') if email.strip()]
invalid_emails = [email for email in emails_list if not is_valid_email(email)]

# Afficher les erreurs pour les emails invalides
if invalid_emails:
    st.error(f"Les emails suivants ne sont pas valides : {', '.join(invalid_emails)}")
    recurring_emails_valid = False
else:
    recurring_emails_valid = True

# Récupérer la liste des emails récurrents valides
recurring_emails_list = [email for email in emails_list if is_valid_email(email)]

# Afficher un résumé
st.write(f"Nombre d'emails récurrents valides : {len(recurring_emails_list)}")

# Ajouter un bloc d'aide sur l'utilisation de Ctrl+Enter
st.info("💡 Astuce : Utilisez Ctrl+Enter pour valider votre saisie dans ce champ.")

# Séparateur visuel
st.markdown("---")

# Section - Groupes et emails spécifiques
st.header("2. Groupes et emails spécifiques")

# Variable pour stocker les données du fichier
data = None
existing_group_emails = {}

# Traitement du fichier téléversé
if uploaded_file is not None:
    try:
        # Lire le fichier sans afficher son contenu
        uploaded_file.seek(0)
        
        # Essayer avec différentes options
        data = None
        for encoding in ['utf-8', 'latin1', 'cp1252']:
            for separator in [',', ';', '\t']:
                try:
                    uploaded_file.seek(0)  # Réinitialiser le curseur à chaque tentative
                    test_data = pd.read_csv(uploaded_file, encoding=encoding, sep=separator)
                    
                    if 'Groupe' in test_data.columns and 'Email' in test_data.columns:
                        data = test_data
                        st.sidebar.success(f"Fichier chargé avec succès (encodage: {encoding}, séparateur: '{separator}')")
                        
                        # Extraire les emails existants par groupe
                        existing_group_emails = data.groupby('Groupe')['Email'].apply(list).to_dict()
                        break
                except Exception:
                    continue
            if data is not None and 'Groupe' in data.columns and 'Email' in data.columns:
                break
        
        if data is None or 'Groupe' not in data.columns or 'Email' not in data.columns:
            st.error("Impossible de lire le fichier. Veuillez vérifier son format (il doit avoir des colonnes 'Groupe' et 'Email').")
            data = None
            
    except Exception as e:
        st.error(f"Erreur lors de l'importation: {e}")
        data = None

# Gestion des groupes si les données sont chargées
if data is not None:
    # Afficher les groupes disponibles
    unique_groups = data['Groupe'].unique().tolist()
    
    # Initialiser le dictionnaire pour stocker les emails spécifiques
    if 'specific_emails' not in st.session_state:
        st.session_state.specific_emails = {}
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Pour chaque groupe, créer un champ pour les emails spécifiques
        selected_group = st.selectbox("Sélectionner un groupe", 
                                  options=unique_groups if unique_groups else [""])
    
    if selected_group:
        # Gestion des emails existants et ajoutés pour le groupe
        existing_emails = existing_group_emails.get(selected_group, [])
        added_emails = st.session_state.specific_emails.get(selected_group, [])
        
        # Combiner les emails existants et ajoutés
        all_emails = existing_emails + added_emails
        
        # Section pour afficher les emails du groupe
        st.subheader(f"Emails pour le groupe '{selected_group}'")
        
        # Créer un formulaire pour gérer les emails
        with st.form(key=f'email_form_{selected_group}'):
            # Zone de texte modifiable avec tous les emails
            email_text = st.text_area(
                "Emails (un par ligne)", 
                value="\n".join(all_emails), 
                height=200
            )
            
            # Bouton de soumission
            submit_button = st.form_submit_button("Mettre à jour les emails")
            
            if submit_button:
                # Nettoyer et valider les emails
                updated_emails = [email.strip() for email in email_text.split('\n') if email.strip()]
                
                # Vérifier la validité des emails
                invalid_emails = [email for email in updated_emails if not is_valid_email(email)]
                
                if invalid_emails:
                    st.error(f"Les emails suivants ne sont pas valides : {', '.join(invalid_emails)}")
                else:
                    # Séparer les emails existants et ajoutés
                    new_added_emails = [email for email in updated_emails if email not in existing_emails]
                    
                    # Mettre à jour les emails spécifiques
                    st.session_state.specific_emails[selected_group] = new_added_emails
                    
                    st.success(f"Emails du groupe '{selected_group}' mis à jour.")
        
        # Ajouter un bloc d'aide sur l'utilisation de Ctrl+Enter
        st.info("💡 Astuce : Utilisez Ctrl+Enter pour valider votre saisie.")
    
    # Section récapitulative des emails par groupe
    st.subheader("Récapitulatif des emails par groupe")
    
    # Préparer un dictionnaire combinant emails existants et ajoutés
    all_groups_emails = {}
    for group in unique_groups:
        existing_emails = existing_group_emails.get(group, [])
        specific_emails = st.session_state.specific_emails.get(group, [])
        all_groups_emails[group] = list(set(existing_emails + specific_emails))
    
    if all_groups_emails:
        for group, emails in all_groups_emails.items():
            if emails:
                with st.expander(f"Groupe: {group} ({len(emails)} emails)"):
                    st.text_area(f"Emails du groupe {group}", 
                                 value="\n".join(emails), 
                                 height=150, 
                                 key=f"group_emails_{group}")
    else:
        st.info("Aucun email spécifique n'a été ajouté pour le moment.")
else:
    st.info("Veuillez importer le fichier CSV Démarches Simplifiées (groupe instructeur : Exporter le csv) pour gérer les emails spécifiques aux groupes.")

# Séparateur visuel
st.markdown("---")

# Bouton pour générer le fichier final
st.header("3. Génération du fichier final")

if st.button("Générer le fichier CSV"):
    if uploaded_file is None:
        st.error("Veuillez d'abord importer un fichier CSV.")
    elif not recurring_emails_valid:
        st.error("Veuillez corriger tous les emails récurrents invalides avant de générer le fichier.")
    elif data is None:
        st.error("Impossible de lire le fichier CSV. Veuillez vérifier son format.")
    else:
        try:
            # Utiliser les données déjà chargées
            processed_data = data.copy()
            
            # Création d'une nouvelle structure avec les e-mails ajoutés
            expanded_data = []
            
            # Récupérer tous les groupes
            all_groups = set(processed_data['Groupe'].unique())
            
            # Ajouter les emails récurrents à tous les groupes
            for group in all_groups:
                # Emails récurrents
                for email in recurring_emails_list:
                    if email not in existing_group_emails.get(group, []):
                        expanded_data.append({
                            'Groupe': group,
                            'Email': email
                        })
                
                # Emails spécifiques ajoutés
                if 'specific_emails' in st.session_state and group in st.session_state.specific_emails:
                    for email in st.session_state.specific_emails[group]:
                        if email not in existing_group_emails.get(group, []):
                            expanded_data.append({
                                'Groupe': group,
                                'Email': email
                            })
            
            # Ajouter les emails existants
            for group, emails in existing_group_emails.items():
                for email in emails:
                    if email not in [row['Email'] for row in expanded_data if row['Groupe'] == group]:
                        expanded_data.append({
                            'Groupe': group,
                            'Email': email
                        })
            
            # Conversion en DataFrame
            expanded_df = pd.DataFrame(expanded_data)
            
            # Trier par groupe et email
            expanded_df = expanded_df.sort_values(['Groupe', 'Email'])
            
            # Afficher un aperçu du fichier final
            st.subheader("Aperçu du fichier final")
            st.write(f"Nombre total d'entrées: {len(expanded_df)}")
            
            # Afficher le DataFrame avec une hauteur plus importante
            st.dataframe(expanded_df, height=400, use_container_width=True)
            
            # Lien de téléchargement
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"groupe_instructeurs_onetrickpony_{now}.csv"
            st.markdown(get_csv_download_link(expanded_df, filename), unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Erreur lors de la génération du fichier: {e}")
