# Gestion des Groupes d'Instructeurs

## 🚀 Description de l'Application

Cette application Streamlit permet de gérer et de consolider les emails pour différents groupes d'instructeurs à partir d'un fichier CSV exporté de Démarches Simplifiées.
Pour lancer l'appli en local : streamlit one_trick_pony.py

## 📋 Fonctionnalités Principales

### 1. Emails Récurrents
- Ajoutez des emails qui seront communs à tous les groupes
- Validation en temps réel des adresses email
- Affichage du nombre total d'emails existant et ajoutés par groupe

### 2. Groupes et Emails Spécifiques
- Importez un fichier CSV contenant les informations des groupes
- Visualisez les emails existants pour chaque groupe
- Ajoutez de nouveaux emails spécifiques à un groupe
- Modifiez facilement les listes d'emails

### 3. Génération du Fichier Final
- Créez un nouveau fichier CSV consolidé
- Incluez :
  - Emails récurrents
  - Emails spécifiques ajoutés manuellement
  - Emails existants du fichier original

## 🛠️ Prérequis

- Python 3.7+
- Bibliothèques :
  - streamlit
  - pandas
  - base64

## 🔧 Installation

1. Clonez le dépôt
```bash
git clone https://github.com/votre-repo/gestion-groupes-instructeurs.git
cd gestion-groupes-instructeurs
```

2. Installez les dépendances
```bash
pip install streamlit pandas
```

## 💻 Utilisation

Lancez l'application avec :
```bash
streamlit run gestion_groupes_instructeurs.py
```

### Étapes d'Utilisation

1. **Importer le Fichier CSV**
   - Format attendu : Colonnes 'Groupe' et 'Email'
   - Exporté depuis Démarches Simplifiées

2. **Emails Récurrents**
   - Saisissez les emails à ajouter à tous les groupes
   - Vérification automatique de la validité des emails

3. **Emails Spécifiques**
   - Sélectionnez un groupe
   - Visualisez/modifiez les emails existants
   - Ajoutez de nouveaux emails

4. **Générer le Fichier Final**
   - Cliquez sur "Générer le fichier CSV"
   - Téléchargez le fichier consolidé

## 🚨 Validation des Emails

- Vérification du format email
- Détection et signalement des emails invalides
- Prévention des doublons

## 📝 Notes Importantes

- Le fichier CSV doit contenir les colonnes 'Groupe' et 'Email'
- Les emails sont uniques par groupe
- Possibilité de modifier/supprimer des emails individuellement
