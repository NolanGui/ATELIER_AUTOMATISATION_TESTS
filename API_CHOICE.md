# API Choice

- Étudiant : Nolan Guiziou
- API choisie : Frankfurter
- URL base : https://api.frankfurter.app
- Documentation officielle / README : https://www.frankfurter.app/docs/
- Auth : None
- Endpoints testés :
  - GET /latest (Derniers taux de change)
  - GET /currencies (Liste des devises supportées)
- Hypothèses de contrat (champs attendus, types, codes) : Le format de retour doit être du JSON. Le statut HTTP doit être 200. Pour /latest, on attend un champ amount (float), un champ base (string), un champ date (string) et un dictionnaire rates.
- Limites / rate limiting connu : Pas de limite stricte documentée, mais on va se limiter à quelques requêtes par run.
- Risques (instabilité, downtime, CORS, etc.) : Downtime du service, timeout si l'API est surchargée.
