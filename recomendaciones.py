# recomendaciones.py
# Recomendaciones para "Ingeniero de Pista ACC" simplificadas a 4 grupos principales
# Cada acción tiene: accion, change, unit, path, desc
# Para usar directamente en la app de setup

RECOMENDACIONES = {
    "Frenos y Electrónica": {
        "No se detiene a tiempo": [
            {
                "accion": "Aumentar presión de frenos delanteros",
                "change": "+3",
                "unit": "%",
                "path": ["basicSetup", "mechanicalBalance", "brakeTorque"],
                "desc": "Incrementa la fuerza de frenado en el eje delantero para detener el coche antes."
            },
            {
                "accion": "Avanzar reparto de frenada",
                "change": "+1",
                "unit": "%",
                "path": ["basicSetup", "mechanicalBalance", "brakeBias"],
                "desc": "Mueve el reparto hacia adelante, aumentando eficacia de frenadas largas."
            },
            {
                "accion": "Incrementar TC si patina al frenar",
                "change": "+1",
                "unit": "pts",
                "path": ["basicSetup", "electronics", "tC1"],
                "desc": "El control de tracción ayuda a mantener las ruedas traseras pegadas al suelo."
            }
        ],
        "Se detiene muy pronto": [
            {
                "accion": "Reducir presión de frenos delanteros",
                "change": "-3",
                "unit": "%",
                "path": ["basicSetup", "mechanicalBalance", "brakeTorque"],
                "desc": "Reduce la fuerza de frenado para evitar bloquear o perder ritmo."
            },
            {
                "accion": "Retrasar reparto de frenada",
                "change": "-1",
                "unit": "%",
                "path": ["basicSetup", "mechanicalBalance", "brakeBias"],
                "desc": "Mover el reparto hacia atrás para frenar más suavemente."
            }
        ],
        "Patina cuando freno - delantero": [
            {
                "accion": "Reducir presión freno delantero",
                "change": "-2",
                "unit": "%",
                "path": ["basicSetup", "mechanicalBalance", "brakeTorque"],
                "desc": "Disminuye presión para evitar bloqueo del eje delantero."
            },
            {
                "accion": "Incrementar ABS",
                "change": "+1",
                "unit": "pts",
                "path": ["basicSetup", "electronics", "abs"],
                "desc": "Mayor ABS reduce patinadas frontales al frenar."
            }
        ],
        "Patina cuando freno - trasero": [
            {
                "accion": "Reducir presión freno trasero",
                "change": "-2",
                "unit": "%",
                "path": ["basicSetup", "mechanicalBalance", "brakeTorque"],
                "desc": "Disminuye presión trasera para evitar bloqueos en frenadas fuertes."
            },
            {
                "accion": "Avanzar reparto de frenada",
                "change": "+1",
                "unit": "%",
                "path": ["basicSetup", "mechanicalBalance", "brakeBias"],
                "desc": "Mueve reparto hacia adelante para mejorar estabilidad trasera."
            }
        ],
        "Frena bien pero bloquea esporádicamente": [
            {
                "accion": "Reducir presión de frenos ligeramente",
                "change": "-1",
                "unit": "%",
                "path": ["basicSetup", "mechanicalBalance", "brakeTorque"],
                "desc": "Ajuste fino para evitar picos de bloqueo."
            },
            {
                "accion": "Incrementar ABS en 1 punto",
                "change": "+1",
                "unit": "pts",
                "path": ["basicSetup", "electronics", "abs"],
                "desc": "Evita bloqueo intermitente sin comprometer frenada."
            }
        ],
        "Acelera muy despacio (pérdida de tracción en salida)": [
            {
                "accion": "Reducir TC",
                "change": "-1",
                "unit": "pts",
                "path": ["basicSetup", "electronics", "tC1"],
                "desc": "Permite más potencia en salida, pero requiere control del piloto."
            }
        ],
        "Frenada inestable con ABS": [
            {
                "accion": "Reducir ABS 1 punto",
                "change": "-1",
                "unit": "pts",
                "path": ["basicSetup", "electronics", "abs"],
                "desc": "Evita intervención irregular de ABS."
            }
        ],
        "Mapa motor / aceleración inconsistente": [
            {
                "accion": "Probar otro mapa ECU",
                "change": "+1",
                "unit": "pts",
                "path": ["basicSetup", "electronics", "eCUMap"],
                "desc": "Ajusta respuesta del motor para mayor consistencia."
            }
        ]
    },

    "Aerodinámica y Altura": {
        "Voy muy lento en rectas": [
            {
                "accion": "Reducir alerón trasero",
                "change": "-1",
                "unit": "pts",
                "path": ["advancedSetup", "aeroBalance", "rearWing"],
                "desc": "Disminuye drag para ganar velocidad punta."
            },
            {
                "accion": "Reducir alerón delantero / splitter",
                "change": "-1",
                "unit": "pts",
                "path": ["advancedSetup", "aeroBalance", "splitter"],
                "desc": "Reducción de carga frontal para mejorar recta."
            }
        ],
        "Patino en curvas rápidas": [
            {
                "accion": "Aumentar alerón trasero",
                "change": "+2",
                "unit": "pts",
                "path": ["advancedSetup", "aeroBalance", "rearWing"],
                "desc": "Más carga trasera mejora estabilidad."
            },
            {
                "accion": "Aumentar splitter / alerón delantero",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "aeroBalance", "splitter"],
                "desc": "Mayor carga delantera ayuda al giro rápido."
            }
        ],
        "El auto no gira en curvas (subviraje)": [
            {
                "accion": "Aumentar carga delantera",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "aeroBalance", "splitter"],
                "desc": "Mejora el giro en curvas reduciendo subviraje."
            },
            {
                "accion": "Reducir alerón trasero",
                "change": "-1",
                "unit": "pts",
                "path": ["advancedSetup", "aeroBalance", "rearWing"],
                "desc": "Menos carga trasera ayuda a girar mejor."
            }
        ],
        "Oscilaciones a alta velocidad (flutter)": [
            {
                "accion": "Aumentar alerón trasero 1 punto",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "aeroBalance", "rearWing"],
                "desc": "Estabiliza el coche a alta velocidad."
            },
            {
                "accion": "Subir altura delantera 1 mm",
                "change": "+1",
                "unit": "mm",
                "path": ["advancedSetup", "aeroBalance", "rideHeight", 0],
                "desc": "Pequeños cambios en altura suavizan respuesta aerodinámica."
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
                "desc": "Más rigidez frontal mejora la entrada de curva."
            }
        ],
        "El auto no gira en curvas - a lo largo": [
            {
                "accion": "Aumentar rigidez trasera (ARB Rear)",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "mechanicalBalance", "aRBRear"],
                "desc": "Mantiene estabilidad en curvas largas."
            }
        ],
        "El auto no gira en curvas - salida": [
            {
                "accion": "Aumentar rigidez trasera",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "mechanicalBalance", "aRBRear"],
                "desc": "Mejora la estabilidad al salir de curva."
            }
        ],
        "El auto gira demasiado (sobreviraje)": [
            {
                "accion": "Reforzar barra estabilizadora delantera",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "mechanicalBalance", "aRBFront"],
                "desc": "Reduce sobreviraje incrementando rigidez frontal."
            }
        ],
        "Neumáticos se desgastan rápido / se sobrecalientan": [
            {
                "accion": "Reducir rigidez delantera",
                "change": "-1",
                "unit": "pts",
                "path": ["advancedSetup", "mechanicalBalance", "aRBFront"],
                "desc": "Equilibra desgaste en curvas y pistas exigentes."
            },
            {
                "accion": "Ajustar presión de neumáticos",
                "change": "+0.5",
                "unit": "psi",
                "path": ["basicSetup", "tyres", "tyrePressure"],
                "desc": "Controla temperatura y desgaste."
            }
        ],
        "Dirección lenta o con mucha relación (steer ratio)": [
            {
                "accion": "Reducir relación de giro",
                "change": "-1",
                "unit": "pts",
                "path": ["basicSetup", "alignment", "steerRatio"],
                "desc": "Dirección más rápida y directa."
            }
        ],
        "Rebote / bouncy (rebotan al salir de curva)": [
            {
                "accion": "Aumentar rebound slow trasero",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "dampers", "reboundSlow", 2],
                "desc": "Controla el rebote trasero al salir de curva."
            }
        ],
        "Amortiguación demasiado dura en compresión rápida": [
            {
                "accion": "Disminuir bump fast delantero",
                "change": "-1",
                "unit": "pts",
                "path": ["advancedSetup", "dampers", "bumpFast", 0],
                "desc": "Suaviza compresión rápida, mejora agarre en baches."
            }
        ],
        "Carro demasiado blando en frenada (nose dive)": [
            {
                "accion": "Aumentar compresión delantera",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "dampers", "bumpSlow", 0],
                "desc": "Reduce hundimiento frontal al frenar."
            }
        ]
    },

    "Neumáticos y Diferencial": {
        "PSI bajo al inicio o calienta rápido": [
            {
                "accion": "Aumentar PSI delanteros izquierdo",
                "change": "+0.5",
                "unit": "psi",
                "path": ["basicSetup", "tyres", "tyrePressure", 0],
                "desc": "Ajuste fino para inicio de carrera."
            },
            {
                "accion": "Aumentar PSI delanteros derecho",
                "change": "+0.5",
                "unit": "psi",
                "path": ["basicSetup", "tyres", "tyrePressure", 1],
                "desc": "Equilibrio de presión frontal."
            }
        ],
        "PSI traseros bajo/alto": [
            {
                "accion": "Aumentar PSI trasero izquierdo",
                "change": "+0.5",
                "unit": "psi",
                "path": ["basicSetup", "tyres", "tyrePressure", 2],
                "desc": "Ajuste fino trasero izquierdo."
            },
            {
                "accion": "Aumentar PSI trasero derecho",
                "change": "+0.5",
                "unit": "psi",
                "path": ["basicSetup", "tyres", "tyrePressure", 3],
                "desc": "Ajuste fino trasero derecho."
            }
        ],
        "Desgaste exterior en delantero (carcasa caliente)": [
            {
                "accion": "Incrementar camber delantero",
                "change": "+0.1",
                "unit": "deg",
                "path": ["basicSetup", "alignment", "staticCamber", 0],
                "desc": "Reduce desgaste exterior de neumático."
            }
        ],
        "Desgaste interior (exceso de camber negativo)": [
            {
                "accion": "Hacer camber menos negativo",
                "change": "+0.1",
                "unit": "deg",
                "path": ["basicSetup", "alignment", "staticCamber", 0],
                "desc": "Reduce desgaste interior de neumático."
            }
        ],
        "Desgaste desigual entre ejes": [
            {
                "accion": "Ajustar toe en eje correspondiente",
                "change": "+0.05",
                "unit": "deg",
                "path": ["basicSetup", "alignment", "toe", 0],
                "desc": "Equilibra huella entre ejes."
            }
        ],
        "Diferencial patina en salida": [
            {
                "accion": "Aumentar preload diferencial",
                "change": "+10",
                "unit": "Nm",
                "path": ["advancedSetup", "drivetrain", "preload"],
                "desc": "Mejora tracción y salida de curva."
            }
        ],
        "El coche vibra en baches a baja velocidad": [
            {
                "accion": "Aumentar tope suspensión trasero",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "dampers", "bumpStopRear"],
                "desc": "Reduce vibraciones al pasar baches."
            }
        ]
    }
}
