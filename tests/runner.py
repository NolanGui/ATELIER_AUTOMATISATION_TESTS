import datetime
from tests.tests import run_all_tests

def calculate_percentile(data, percentile):
    """Calcule un percentile donné sur une liste de nombres."""
    if not data:
        return 0
    data.sort()
    index = int(len(data) * (percentile / 100.0))
    # On s'assure de ne pas déborder de la liste
    return data[min(index, len(data)-1)]

def execute_run():
    """
    Lance tous les tests, calcule les statistiques QoS et 
    génère le rapport de fin d'exécution.
    """
    # 1. On lance les tests
    tests_results = run_all_tests()
    
    # 2. On calcule les métriques de réussite
    passed = sum(1 for t in tests_results if t["status"] == "PASS")
    failed = sum(1 for t in tests_results if t["status"] == "FAIL")
    total = len(tests_results)
    error_rate = round(failed / total, 3) if total > 0 else 0
    
    # 3. On calcule la QoS (Latences)
    # On ne prend que les latences supérieures à 0 pour être précis
    latencies = [t["latency_ms"] for t in tests_results if t["latency_ms"] > 0]
    
    avg_latency = int(sum(latencies) / len(latencies)) if latencies else 0
    p95_latency = int(calculate_percentile(latencies, 95))
    
    # 4. On génère le Timestamp au format ISO (ex: 2026-04-28T10:00:00+00:00)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # 5. On construit le dictionnaire final (comme demandé dans les consignes)
    run_data = {
        "api": "Frankfurter",
        "timestamp": now,
        "summary": {
            "passed": passed,
            "failed": failed,
            "error_rate": error_rate,
            "latency_ms_avg": avg_latency,
            "latency_ms_p95": p95_latency
        },
        "tests": tests_results
    }
    
    return run_data

# Petit bloc pour tester le script tout seul sur ton ordi
if __name__ == "__main__":
    import json
    resultat = execute_run()
    print(json.dumps(resultat, indent=2))