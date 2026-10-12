from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def generate_dummy_samples(count: int, override_ax=None):
    """Funzione helper per generare payload di test rapidamente."""
    samples = []
    for i in range(count):
        samples.append({
            "timestamp": 1620000000 + i,
            "ax": override_ax if override_ax is not None else 0.1,
            "ay": 0.2,
            "az": 9.8,
            "gx": 0.0,
            "gy": 0.0,
            "gz": 0.0
        })
    return {"samples": samples}

def test_calibrate_imu_success():
    """Test 1: Happy Path. Esattamente 100 sample validi."""
    payload = generate_dummy_samples(100)
    response = client.post("/api/v1/calibrate", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert round(data["data"]["offset_ax"], 5) == 0.1 

def test_calibrate_imu_wrong_length():
    """Test 2: Drop di pacchetti. Il sensore invia solo 99 sample."""
    # 1. Genera un payload da 99 sample usando generate_dummy_samples
    payload = generate_dummy_samples(99)
    
    # 2. Invia una POST a "/api/v1/calibrate" con quel payload
    response = client.post("/api/v1/calibrate", json=payload)
    
    # 3. Fai un assert che response.status_code sia uguale a 422
    # Pydantic rifiuta il payload perché min_length=100 non è soddisfatto
    assert response.status_code == 422
    
    # Bonus: verifichiamo che il messaggio di errore sia chiaro
    data = response.json()
    assert "detail" in data
    assert any("samples" in str(err) for err in data["detail"])

def test_calibrate_imu_invalid_data_type():
    """Test 3: Dati corrotti. Il sensore invia una stringa invece di un numero."""
    # 1. Genera un payload da 100 sample passando override_ax="errore_sensore"
    payload = generate_dummy_samples(100, override_ax="errore_sensore")
    
    # 2. Invia una POST a "/api/v1/calibrate"
    response = client.post("/api/v1/calibrate", json=payload)
    
    # 3. Fai un assert che response.status_code sia uguale a 422
    # Pydantic non riesce a convertire "errore_sensore" in float
    assert response.status_code == 422
    
    # Bonus: verifichiamo che l'errore punti al campo corretto
    data = response.json()
    assert "detail" in data

def test_health_check():
    """Test 4: Verifica che l'endpoint di health check risponda correttamente."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "imu-calibration-engine"