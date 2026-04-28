from tests.client import fetch_api

def run_all_tests():
    """
    Exécute une suite de 6 tests sur l'API Frankfurter.
    Retourne une liste de résultats.
    """
    results = []
    base_url = "https://api.frankfurter.app/latest"
    
    # On fait l'appel principal pour les tests 1 à 4
    response, latency, error = fetch_api(base_url)
    
    # Test 1 : HTTP 200 attendu
    test_name = "1. Code HTTP 200"
    if error:
        results.append({"name": test_name, "status": "FAIL", "latency_ms": 0, "details": error})
    elif response.status_code == 200:
        results.append({"name": test_name, "status": "PASS", "latency_ms": latency, "details": ""})
    else:
        results.append({"name": test_name, "status": "FAIL", "latency_ms": latency, "details": f"Code HTTP {response.status_code}"})

    # Si l'appel a réussi, on fait les tests liés au contenu (Tests 2, 3 et 4)
    if response and response.status_code == 200:
        data = response.json() # On transforme le texte en dictionnaire Python
        
        # Test 2 : Content-Type JSON
        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            results.append({"name": "2. Format JSON", "status": "PASS", "latency_ms": latency, "details": ""})
        else:
            results.append({"name": "2. Format JSON", "status": "FAIL", "latency_ms": latency, "details": f"Mauvais type: {content_type}"})

        # Test 3 : Champs obligatoires présents (amount, base, date, rates)
        required_keys = ["amount", "base", "date", "rates"]
        missing_keys = [key for key in required_keys if key not in data]
        if not missing_keys:
            results.append({"name": "3. Champs obligatoires", "status": "PASS", "latency_ms": latency, "details": ""})
        else:
            results.append({"name": "3. Champs obligatoires", "status": "FAIL", "latency_ms": latency, "details": f"Manque: {missing_keys}"})

        # Test 4 : Types des données (ex: rates doit être un objet/dictionnaire)
        if "rates" in data and isinstance(data["rates"], dict):
            results.append({"name": "4. Type de 'rates' (dict)", "status": "PASS", "latency_ms": latency, "details": ""})
        else:
            results.append({"name": "4. Type de 'rates' (dict)", "status": "FAIL", "latency_ms": latency, "details": "'rates' n'est pas un dictionnaire"})
    else:
        # Si la requête a échoué, les tests 2, 3 et 4 échouent par défaut
        for name in ["2. Format JSON", "3. Champs obligatoires", "4. Type de données"]:
            results.append({"name": name, "status": "FAIL", "latency_ms": latency or 0, "details": "Impossible de vérifier (pas de réponse)"})

    # Test 5 : Cas d'erreur attendu (Demander une devise qui n'existe pas -> doit renvoyer 404)
    bad_url = "https://api.frankfurter.app/latest?from=MONNAIE_INCONNUE"
    bad_response, bad_latency, bad_error = fetch_api(bad_url)
    if bad_response and bad_response.status_code == 404:
        results.append({"name": "5. Gestion erreur 404 (Entrée invalide)", "status": "PASS", "latency_ms": bad_latency, "details": ""})
    else:
        results.append({"name": "5. Gestion erreur 404", "status": "FAIL", "latency_ms": bad_latency or 0, "details": "N'a pas renvoyé 404 comme prévu"})

    # Test 6 : Temps de réponse acceptable (Robustesse)
    if latency and latency < 1500: # On considère que moins de 1,5s c'est correct
        results.append({"name": "6. Latence acceptable (<1500ms)", "status": "PASS", "latency_ms": latency, "details": ""})
    else:
        results.append({"name": "6. Latence acceptable (<1500ms)", "status": "FAIL", "latency_ms": latency or 0, "details": f"Trop lent: {latency}ms"})

    return results