import requests
import websockets

from src.config import Config as cfg

# Caricamento configurazione
configObj = cfg.load_from_env()

