import logging
from fastapi import FastAPI, HTTPException
from models.schemas import IMUBatch
from services.analyzer import calculate_calibration_offsets

# 1. CONFIGURAZIONE LOGGING
# Un microservizio senza log è una scatola nera. Configuriamo un logger base.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("imu_engine")

app = FastAPI(title="IMU Calibration Engine")

# 2. HEALTH CHECK ENDPOINT
# Fondamentale per Docker, Kubernetes o i Load Balancer per sapere se il servizio è vivo.
@app.get("/health")
def health_check():
    logger.debug("Health check richiesto.")
    return {"status": "healthy", "service": "imu-calibration-engine"}

# 3. ENDPOINT DI CALIBRAZIONE CON GESTIONE ERRORI
@app.post("/api/v1/calibrate")
def calibrate_imu(payload: IMUBatch):
    logger.info(f"Ricevuta richiesta di calibrazione con {len(payload.samples)} sample.")
    
    try:
        # La logica di business è isolata nel service
        offsets = calculate_calibration_offsets(payload.samples)
        logger.info("Calibrazione completata con successo.")
        
        return {
            "status": "success", 
            "data": offsets
        }
    except Exception as e:
        # INGEGNERIA DEL FALLIMENTO: 
        # Se succede qualcosa di imprevisto (es. un bug matematico), 
        # NON facciamo crashare l'app. Logghiamo l'errore e restituiamo un 500 pulito.
        logger.error(f"Errore imprevisto durante la calibrazione: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail="Si è verificato un errore interno durante l'elaborazione dei dati IMU."
        )