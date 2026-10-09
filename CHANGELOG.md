# Changelog

Version = numéro annoncé par l'outil Artifact à la publication sur l'instance de référence.

| Version | Date | Changement |
|---|---|---|
| v41 | 2026-10-09 | Filtre actif visible : champ de recherche en évidence (ambre) et badge « N cartes · critères » avec bouton « Tout afficher » dans la barre d'outils (recherche, personne, en retard, filtres de la vue Liste). |
| v40 | 2026-10-08 | Diagrammes Mermaid dans le markdown (détail, carte ouverte, journal, Agenda) : librairie chargée à la demande depuis cdnjs, SVG assaini par DOMPurify, thème suivi, bloc invalide signalé sans dessin d'erreur. Règle `[hidden]` reprise de l'enveloppe d'artefact dans la page ; banc de test avec la même enveloppe. |
| v39 | 2026-10-08 | Réglages du tableau : champ « jours » d'archivage à largeur fixe, explication sous le champ (le champ était écrasé). |
| v38 | 2026-10-08 | Réglages de l'instance : écran « Réglages » (nom, sous-titre, vues proposées, vue par défaut ordinateur / téléphone) qui écrit `settings/app` (`views`, `defaults`) ; sélecteur de vue filtré, vue interdite rabattue sur Colonnes ; surcharge `views` par tableau dans ses réglages ; bouton réservé aux éditeurs quand la capacité `user` répond. |
| v37 | 2026-10-08 | Raccourcis clavier : `N` nouvelle carte, `/` filtre, `L` Liste, `C` Colonnes (inactifs dans un champ, une fenêtre ouverte ou avec modificateur). |
| v36 | 2026-10-08 | Archiver un tableau (`archivedAt` sur le tableau, cartes actives archivées avec lui `archivedBy: "board"`, désarchivage symétrique, onglets archivés masqués avec compteur, bandeau). Réglage `autoArchiveDays` + bouton d'archivage des cartes terminées anciennes (`archivedBy: "auto"`). |
| v35 | 2026-10-08 | Vue (Colonnes / Liste / Agenda / Semaine) mémorisée par tableau (`view.<boardId>`), ancienne clé globale reprise comme valeur de départ ; Contacts jamais mémorisée ; ancre `#tableau.vue` inchangée. |
| v33-34 | 2026-10-08 | Republication sans changement de code (titre rétabli). |
| v32 | 2026-10-08 | Source commun sans `<title>` (titre passé à la publication). Aucun changement fonctionnel. |
| v31 | 2026-10-08 | Onglets déplaçables : écritures en parallèle, ordre optimiste conservé pendant les écritures (plus d'avancée cran par cran). |
| v30 | 2026-10-08 | Correctif : écouteurs du conteneur d'onglets posés une seule fois. |
| v29 | 2026-10-08 | Déplacer un onglet par glisser-déposer (`wireTabDnD`, `moveBoard`, renumérotation de `order`). |
| v28 | 2026-10-08 | Code commun entre instances : vues Agenda / Semaine / Contacts, `settings/app`. |
