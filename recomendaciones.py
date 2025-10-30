# recomendaciones.py
# Recomendaciones para "Ingeniero de Pista ACC" organizadas por categorías optimizadas
# Cada acción tiene: accion, change, unit, path y desc

RECOMENDACIONES = {
    "Frenos": {
        "No se detiene a tiempo": [
            {
                "accion": "Aumentar presión de frenos delanteros",
                "change": "+3",
                "unit": "%",
                "path": ["basicSetup", "mechanicalBalance", "brakeTorque"],
                "desc": "Incrementa la fuerza de frenado ajustando la presión/calibración de los frenos delanteros."
            },
            {
                "accion": "Avanzar reparto de frenada",
                "change": "+1",
                "unit": "%",
                "path": ["basicSetup", "mechanicalBalance", "brakeBias"],
                "desc": "Mover el reparto hacia el eje delantero para aumentar eficacia en frenadas largas."
            }
        ],
        "Se detiene muy pronto": [
            {
                "accion": "Disminuir presión de frenos delanteros",
                "change": "-3",
                "unit": "%",
                "path": ["basicSetup", "mechanicalBalance", "brakeTorque"],
                "desc": "Reduce presión si el coche frena demasiado pronto."
            },
            {
                "accion": "Retrasar reparto de frenada",
                "change": "-1",
                "unit": "%",
                "path": ["basicSetup", "mechanicalBalance", "brakeBias"],
                "desc": "Mover reparto hacia atrás para disminuir frenada delantera."
            }
        ]
    },

    "Aerodinámica": {
        "Voy muy lento en rectas": [
            {
                "accion": "Reducir alerón trasero",
                "change": "-1",
                "unit": "pts",
                "path": ["advancedSetup", "aeroBalance", "rearWing"],
                "desc": "Disminuir carga trasera para ganar velocidad punta."
            },
            {
                "accion": "Reducir alerón delantero / splitter",
                "change": "-1",
                "unit": "pts",
                "path": ["advancedSetup", "aeroBalance", "splitter"],
                "desc": "Reducir carga delantera para menos resistencia en rectas."
            }
        ],
        "Patino en curvas rápidas": [
            {
                "accion": "Aumentar alerón trasero",
                "change": "+2",
                "unit": "pts",
                "path": ["advancedSetup", "aeroBalance", "rearWing"],
                "desc": "Más carga en la parte trasera para mejorar estabilidad en curvas rápidas."
            },
            {
                "accion": "Aumentar splitter/aleta delantera",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "aeroBalance", "splitter"],
                "desc": "Aumenta carga delantera para mejor agarre en curvas rápidas."
            }
        ]
    },

    "Suspensión y Amortiguadores": {
        "El auto no gira en curvas - entrada": [
            {
                "accion": "Aumentar rigidez delantera (ARB Front)",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "mechanicalBalance", "aRBFront"],
                "desc": "Mayor rigidez frontal mejora la respuesta de giro en entrada."
            },
            {
                "accion": "Bajar altura delantera",
                "change": "-1",
                "unit": "mm",
                "path": ["advancedSetup", "aeroBalance", "rideHeight", 0],
                "desc": "Bajar ligeramente la suspensión delantera para más agarre."
            }
        ],
        "El auto no gira en curvas - salida": [
            {
                "accion": "Aumentar rigidez trasera",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "mechanicalBalance", "aRBRear"],
                "desc": "Ayuda a mantener la estabilidad en salida de curva."
            },
            {
                "accion": "Subir altura trasera",
                "change": "+1",
                "unit": "mm",
                "path": ["advancedSetup", "aeroBalance", "rideHeight", 1],
                "desc": "Elevar ligeramente la parte trasera para más tracción."
            }
        ],
        "Rebote / bouncy (rebotan al salir de curva)": [
            {
                "accion": "Aumentar rebound slow trasero",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "dampers", "reboundSlow", 2],
                "desc": "Controlar extensión lenta para mejorar el rebote en salidas."
            },
            {
                "accion": "Aumentar bump slow delantero",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "dampers", "bumpSlow", 0],
                "desc": "Control compresión lenta para estabilizar el coche."
            }
        ]
    },

    "Electrónica": {
        "Acelera muy despacio": [
            {
                "accion": "Reducir TC",
                "change": "-1",
                "unit": "pts",
                "path": ["basicSetup", "electronics", "tC1"],
                "desc": "Permite más potencia entregada, requiere control del piloto."
            },
            {
                "accion": "Aumentar TC",
                "change": "+1",
                "unit": "pts",
                "path": ["basicSetup", "electronics", "tC1"],
                "desc": "Subir TC ayuda a mantener tracción si patina."
            }
        ],
        "Frenada inestable con ABS": [
            {
                "accion": "Reducir ABS 1 punto",
                "change": "-1",
                "unit": "pts",
                "path": ["basicSetup", "electronics", "abs"],
                "desc": "Ajuste fino del ABS para evitar intervenciones irregulares."
            }
        ]
    },

    "Neumáticos": {
        "PSI bajo al inicio o calienta rápido": [
            {
                "accion": "Aumentar PSI delanteros 0.5 psi",
                "change": "+0.5",
                "unit": "psi",
                "path": ["basicSetup", "tyres", "tyrePressure", 0],
                "desc": "Ajuste fino delantero izquierdo."
            },
            {
                "accion": "Aumentar PSI delanteros 0.5 psi (derecho)",
                "change": "+0.5",
                "unit": "psi",
                "path": ["basicSetup", "tyres", "tyrePressure", 1],
                "desc": "Ajuste fino delantero derecho."
            }
        ],
        "Desgaste desigual / calienta demasiado": [
            {
                "accion": "Ajustar camber delantero",
                "change": "+0.1",
                "unit": "deg",
                "path": ["basicSetup", "alignment", "staticCamber", 0],
                "desc": "Reducir desgaste exterior e interior."
            },
            {
                "accion": "Ajustar presión según eje",
                "change": "+/-0.3",
                "unit": "psi",
                "path": ["basicSetup", "tyres", "tyrePressure"],
                "desc": "Equilibrar temperatura y desgaste de neumáticos."
            }
        ]
    },

    "Avanzado / Drivetrain": {
        "Diferencial patina en salida": [
            {
                "accion": "Aumentar preload diferencial",
                "change": "+10",
                "unit": "Nm",
                "path": ["advancedSetup", "drivetrain", "preload"],
                "desc": "Mayor preload reduce giro diferencial y mejora salida."
            }
        ],
        "El coche vibra en baches": [
            {
                "accion": "Aumentar bump stop rate trasero",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "mechanicalBalance", "bumpStopRateUp", 2],
                "desc": "Evita que la suspensión llegue al fondo en baches fuertes."
            }
        ]
    }
}

# Alias export-friendly
# RECOMENDACIONES sigue siendo la fuente principal
