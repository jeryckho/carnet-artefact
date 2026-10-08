# Board — tableaux partagés avec Claude

Page HTML autonome, publiée comme artefact claude.ai, qui tient des tableaux de cartes
(Kanban, file de demandes, investigation, libre) partagés en direct entre un utilisateur
et Claude. Les cartes vivent dans la base de l'artefact (capacité `db`) : Claude y lit et
écrit depuis Claude Code avec l'outil `ArtifactData`, l'utilisateur depuis la page.

Un seul source, `board.html`, sert à autant d'instances que voulu (une par artefact).
Le fichier n'a **pas** de balise `<title>` : le nom de l'artefact est donné au moment
de publier. Ce qui diffère d'une instance à l'autre passe par la base (`settings/app`),
jamais par une divergence de code.

## Contenu du dépôt

| Fichier | Rôle |
|---|---|
| `board.html` | La page complète (CSS, HTML, JS), sans dépendance locale. Librairies `marked` et `DOMPurify` chargées depuis cdnjs. |
| `CHANGELOG.md` | Une ligne par version publiée. |
| `test/serve.py` | Banc de test local : la page branchée sur une base factice en mémoire, servie sur `http://127.0.0.1:8765/`. |

## Installer une nouvelle instance

Depuis une session Claude Code ouverte avec le compte claude.ai qui possédera l'artefact.

1. **Publier** `board.html` comme nouvel artefact, en passant :
   - `title` : le nom de l'instance (le fichier n'a pas de `<title>`) ;
   - `icon` : un mot générique, par exemple `board` ;
   - `capabilities` : `{"db": {}, "comments": {"composer_only": true}}`.
     Charger d'abord le skill `artifact-capabilities`, qui donne la syntaxe exacte.
     Capacités facultatives reconnues par la page : `user` (nom des auteurs au lieu
     de « Moi »), `downloads` (export CSV de la vue Semaine).
2. **Ouvrir** l'artefact. La page propose de créer les trois tableaux de départ
   (Kanban, File pour Claude, Investigation) ou un tableau vide.
3. **Régler l'instance** (facultatif) : document `settings/app` dans la base,
   écrit avec `ArtifactData` (`collection: settings`, `doc_id: app`) :
   `{"title": "Nom affiché", "sub": "sous-titre", "contacts": true}`.
   `contacts: true` active la vue Contacts et le champ Contact des cartes.
4. **Partager** depuis le menu Partager de la page si d'autres personnes doivent y accéder.
5. **Noter** l'URL de l'artefact et le titre dans la mémoire de la session Claude
   (pas dans ce dépôt, qui reste neutre).

## Mettre à jour une instance

1. Modifier `board.html`, tester en local (ci-dessous), publier sur l'instance de référence :
   `Artifact publish` avec `file_path=board.html`, `url=<artefact>`, `title=<nom>`.
   Depuis une session qui n'a pas encore touché l'artefact, l'outil exige d'abord
   `Artifact read` sur cette URL, en lisant le fichier sauvegardé jusqu'à la dernière ligne.
2. `git commit`, tag `vNN` où NN est le numéro de version que l'outil annonce à la
   publication, ligne dans `CHANGELOG.md`.
3. Pour chaque autre instance, depuis une session sur le compte qui la possède :
   `Artifact read` de son URL puis `Artifact publish` du même `board.html` avec son titre.
   Le suivi de quelle instance est à quelle version se tient hors dépôt.

Règle : une instance de référence reçoit les évolutions en premier, les autres suivent
à l'identique.

## Tester en local

```bash
python test/serve.py
```

Génère `test/index.html` (la page + une base factice qui simule `window.claude.use("db")`
avec quatre tableaux vides) et la sert sur `http://127.0.0.1:8765/`. Les écritures
s'inspectent dans la console : `window.__log` (liste des `update`), `window.__store`
(contenu), `window.__orders` (ordre des onglets à chaque redessin). Option
`--delay` pour retarder et échelonner les écritures, utile pour les effets de rendu
intermédiaire. `Ctrl+C` pour arrêter.

Le banc ne couvre pas les capacités `comments`, `user` et `downloads` : la page les
ignore quand elles manquent, comme en lecture hors claude.ai.

## Base de données

Collections `boards`, `items`, `contacts`, `settings`. Chaque écriture de Claude porte
`by: "claude"` et `updatedAt`, et la carte s'illumine dix minutes côté page. Le schéma
détaillé (champs des cartes, journal `activity`, historique `history`, renvois `#réf`,
archivage) est documenté dans les notes de l'utilisateur ; les presets de colonnes sont
en tête du script de `board.html` (`PRESETS`).
