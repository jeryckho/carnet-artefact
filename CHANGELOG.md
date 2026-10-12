# Changelog

Version = numéro annoncé par l'outil Artifact à la publication sur l'instance de référence.

| Version | Date | Changement |
|---|---|---|
| v47 | 2026-10-12 | Vues enregistrées : bouton « Vues » dans la barre d'outils, collection `views` (`boardId`, `name`, `state`, `order`) partagée ; une vue = Colonnes/Liste + recherche, personne, en retard, et en Liste filtres colonne/priorité/archivées + tri ; appliquer, enregistrer (nom proposé), supprimer avec Annuler ; vue courante reconnue par comparaison, nom affiché dans le badge de filtre. Banc de test : jeu de démonstration chargé à chaque ouverture (cartes, étiquettes, limite, vues). |
| v46 | 2026-10-12 | Transformer une ligne à cocher en carte : bouton « → carte » au survol de chaque ligne dans l'aperçu du détail (carte ouverte). Nouvelle carte dans la même colonne après la source (titre = texte de la ligne, personne et étiquettes reprises), la ligne devient `- [ ] #réf texte`, historique croisé. On reste sur la source. |
| v45 | 2026-10-12 | Dupliquer une carte : bouton dans la carte ouverte, copie juste après l'original dans sa colonne (titre « (copie) », cases décochées, étiquettes, liens, priorité, personne ; sans journal, historique, échéance ni contact), historique croisé « Dupliquée de / en #réf », copie ouverte aussitôt avec le titre sélectionné. |
| v44 | 2026-10-12 | Étiquettes colorées : teinte dérivée du nom (même nom, même couleur partout, cartes, Liste, Agenda), surcharge par document `tags/{slug}` (`hue` 0-360 ou `"none"`), choisie depuis la carte ouverte (pastilles sous le champ Étiquettes, clic = sélecteur Auto / Gris / dix teintes). Banc de test : collection `tags` ajoutée au store factice. |
| v43 | 2026-10-12 | Limite de cartes : pastille « max N » à part du compteur (grise, orange quand la colonne déborde), le compteur garde son seul sens (`affichées/total` sous filtre). Corrige la v42 où la même case portait deux lectures. |
| v42 | 2026-10-12 | Limite de cartes par colonne : champ facultatif `limit` sur chaque colonne, saisi en 3e segment des réglages (`En cours | active | 3`, ou `En cours | 3`) ; affichage `total/limite` dans le compteur, orange quand dépassé, sans blocage. |
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
