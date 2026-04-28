import requests
import time

def fetch_api(url, timeout=3, retries=1):
    """
    Fait une requête GET sur une URL. 
    Gère un timeout de 3 secondes et 1 retry max en cas d'échec.
    Retourne : (response_object, latency_in_ms, error_message)
    """
    for attempt in range(retries + 1):
        start_time = time.time()
        try:
            # On tente de contacter l'API
            response = requests.get(url, timeout=timeout)
            latency_ms = int((time.time() - start_time) * 1000)
            return response, latency_ms, None
            
        except requests.exceptions.Timeout:
            # Si l'API met trop de temps à répondre
            if attempt == retries:
                return None, None, "Timeout: L'API a mis plus de 3 secondes à répondre."
                
        except requests.exceptions.RequestException as e:
            # Si on a une autre erreur réseau (ex: pas d'internet)
            if attempt == retries:
                return None, None, f"Erreur réseau: {str(e)}"
                
    return None, None, "Erreur inconnue"