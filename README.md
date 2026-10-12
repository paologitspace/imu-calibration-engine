# 🛰️ IMU Calibration & Fusion Engine

Un microservizio robusto, containerizzato e testato per la validazione e la calibrazione di dati grezzi provenienti da sensori IMU (Accelerometro e Giroscopio).

> **



biettivo del progetto**: Dimostrare competenze di Ingegneria del Software orientate alla produzione, trasformando una logica di calcolo da un semplice script a un'API REST affidabile, con validazione rigorosa, gestione degli errori, test automatizzati e CI/CD.

---

## ️ Tech Stack

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-V2-orange.svg)](https://docs.pydantic.dev/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![CI](https://github.com/paologitspace/imu-calibration-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/paologitspace/imu-calibration-engine/actions/workflows/ci.yml)

---

## 💡 Why I Built This (Trade-offs & Design Choices)

Questo progetto nasce per risolvere un problema reale: i microcontrollori inviano buffer di letture grezze via Wi-Fi. Per risparmiare cicli di clock a bordo, l'elaborazione viene delegata a questo motore centrale.

Le scelte architetturali chiave:
1. **Validazione Rigida (Pydantic)**: L'endpoint rifiuta *a priori* payload con lunghezza errata (es. 99 invece di 100 sample, simulando un drop di pacchetti Wi-Fi) o tipi di dato errati, restituendo un `422 Unprocessable Entity` invece di far crashare il server.
2. **Separazione delle Responsabilità**: La logica di business (`services/analyzer.py`) è completamente disaccoppiata dal layer di routing (`main.py`), rendendo il codice facilmente testabile e manutenibile.
3. **Ingegneria del Fallimento**: Implementazione di un global exception handler e logging strutturato per garantire che l'API non vada mai in crash silenzioso (restituendo sempre `500` controllati in caso di errori imprevisti).
4. **Sicurezza Docker**: Il container viene eseguito con un utente non-root (`appuser`) e un'immagine base `slim` per minimizzare la superficie di attacco e la dimensione dell'immagine.

---

## 🚀 Quickstart

Il modo più veloce per eseguire il servizio è tramite Docker.

### 1. Clona il repository
```bash
git clone https://github.com/paologitspace/imu-calibration-engine.git
cd imu-calibration-engine

