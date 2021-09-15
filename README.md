# Frietlijst by Ivo
Dit is een applicatie die de recente antwoorden op het bestelformulier weergeeft, 
zodat de informatie inzichtelijker is dan op Google Sheets.

De applicatie is te benaderen via: https://europe-west1-friet-azg.cloudfunctions.net/frietlijst

## Lokaal draaien
Eenmalig:
- Download de service account credentials als `token.json`
- Installeer de requirements.txt
- `pip install functions-framework`

Telkens:
- `bash run-locally.sh`

## Deployen
Eenmalig
- Download de service account credentials als `token.json`

Telkens
- `bash pack.sh`
- Upload `deployable.zip` via https://console.cloud.google.com/functions/details/europe-west1/frietlijst?project=friet-azg