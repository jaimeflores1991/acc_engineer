# -*- coding: utf-8 -*-

# Mapa de recomendaciones ACC
# Formato: "texto amigable": {"path": ["nivel1", "nivel2", ...], "change": valor, "unit": unidad}

recomendacion_map = {
    # --- FRENOS ---
    "No se detiene a tiempo": {"path": ["basicSetup", "mechanicalBalance", "brakeTorque"], "change": "+1", "unit": "%"},
    "Se detiene muy pronto": {"path": ["basicSetup", "mechanicalBalance", "brakeTorque"], "change": "-1", "unit": "%"},
    "Patina cuando freno - delantero": {
        "path": ["basicSetup", "mechanicalBalance", "brakeBias"],
        "change": "-1",
        "unit": "%"
    },
    "Patina cuando freno - trasero": {
        "path": ["basicSetup", "mechanicalBalance", "brakeBias"],
        "change": "+1",
        "unit": "%"
    },

    # --- AERODINÁMICA ---
    "Voy muy lento en rectas": [
        {"path": ["advancedSetup", "aeroBalance", "rearWing"], "change": "-1", "unit": "mm"},
        {"path": ["advancedSetup", "aeroBalance", "splitter"], "change": "-1", "unit": "mm"}
    ],
    "Patino en curvas rápidas": {"path": ["advancedSetup", "aeroBalance", "rearWing"], "change": "+1", "unit": "mm"},
    "El auto no gira en curvas": [
        {"path": ["advancedSetup", "aeroBalance", "splitter"], "change": "+1", "unit": "mm"},
        {"path": ["advancedSetup", "aeroBalance", "rearWing"], "change": "-1", "unit": "mm"}
    ],

    # --- SUSPENSIÓN / AGARRE MECÁNICO ---
    "El auto no gira en curvas - entrada": [
        {"path": ["advancedSetup", "mechanicalBalance", "aRBFront"], "change": "+1", "unit": "pts"},
        {"path": ["advancedSetup", "aeroBalance", "rideHeight"], "change": "-1", "unit": "mm"}
    ],
    "El auto no gira en curvas - a lo largo": [
        {"path": ["advancedSetup", "mechanicalBalance", "aRBRear"], "change": "+1", "unit": "pts"}
    ],
    "El auto no gira en curvas - salida": [
        {"path": ["advancedSetup", "mechanicalBalance", "aRBRear"], "change": "+1", "unit": "pts"},
        {"path": ["advancedSetup", "aeroBalance", "rideHeight"], "change": "+1", "unit": "mm"}
    ],
    "El auto gira demasiado - entrada": [
        {"path": ["advancedSetup", "mechanicalBalance", "aRBFront"], "change": "+1", "unit": "pts"}
    ],
    "El auto gira demasiado - a lo largo": [
        {"path": ["advancedSetup", "mechanicalBalance", "aRBRear"], "change": "-1", "unit": "pts"}
    ],
    "Neumáticos se desgastan rápido": [
        {"path": ["advancedSetup", "mechanicalBalance", "aRBFront"], "change": "+1", "unit": "pts"},
        {"path": ["advancedSetup", "mechanicalBalance", "aRBRear"], "change": "+1", "unit": "pts"}
    ],

    # --- ELECTRÓNICA ---
    "TC demasiado alto": {"path": ["basicSetup", "electronics", "tC1"], "change": "-1", "unit": "pts"},
    "ABS se bloquea": {"path": ["basicSetup", "electronics", "abs"], "change": "-1", "unit": "pts"},

    # --- AMORTIGUADORES ---
    "Rebote demasiado": {"path": ["advancedSetup", "dampers", "reboundSlow"], "change": "-1", "unit": "pts"},
    "Compresión demasiado dura": {"path": ["advancedSetup", "dampers", "bumpFast"], "change": "-1", "unit": "pts"},

    # --- NEUMÁTICOS ---
    "PSI bajo": {"path": ["basicSetup", "tyres", "tyrePressure"], "change": "+1", "unit": "psi"},
    "PSI alto": {"path": ["basicSetup", "tyres", "tyrePressure"], "change": "-1", "unit": "psi"},
    "Caída incorrecta": {"path": ["basicSetup", "alignment", "camber"], "change": "+0.1", "unit": "°"}
}
