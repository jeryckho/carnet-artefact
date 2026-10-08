# Établi / Carnet — source commun

Un seul fichier, `board.html`, sert aux deux artefacts claude.ai :

| Artefact | Compte | URL | Titre à passer |
|---|---|---|---|
| Établi | nrco (vault `C:\Prj\teletravail`) | https://claude.ai/artifact/V5NZb2Xo8NdtgSuQBWTBzw | `Établi` |
| Le Carnet | perso (vault UE5) | https://claude.ai/artifact/1NjcWMkxaW7F1tJE8tHEZu | `Le Carnet` |

Le fichier n'a **pas** de balise `<title>` : le titre est donné au moment de publier
(paramètre `title` de l'outil Artifact). Le nom affiché dans la page vient de
`settings/app` dans la base de chaque artefact.

## Flux

1. Développer et tester sur l'Établi (session sur le vault teletravail).
2. Publier l'Établi : `Artifact publish file_path=board.html url=<Établi> title="Établi"`.
3. `git commit` + tag `vNN` (NN = numéro de version de l'artefact Établi), ligne dans `CHANGELOG.md`.
4. Dans une session sur le vault UE5 : relire l'artefact Carnet (`Artifact read url=<Carnet>`),
   puis publier le même `board.html` avec `title="Le Carnet"`. Cocher la colonne Carnet du changelog.

Règle : l'Établi est le maître, le Carnet suit. Un comportement propre à une instance passe
par `settings/app`, jamais par une divergence de code.

## Données

Les cartes vivent dans la base de chaque artefact (capacité `db`), pas ici.
Schéma et pièges : note vault `Établi - Board partagé avec Claude.md` (vault UE5, dossier `IA/`).
