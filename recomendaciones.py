# recomendaciones.py
# Mapa extenso y profesional de recomendaciones para "Ingeniero de Pista ACC"
# Pensado para competición en simracing: síntomas -> lista de acciones concretas
# Cada acción contiene:
# - accion: texto amigable
# - change: valor a aplicar (puede ser relativo: "+1", "-0.1", etc.)
# - unit: unidad a mostrar (psi, mm, %, deg, pts, Nm, N/m)
# - path: ruta al parámetro en el JSON del setup (lista). Si es un índice en una lista, incluir entero.
# - desc: descripción detallada (opcional)
#
# Notas:
# - Las rutas siguen la estructura de setups ACC tal como usamos antes (basicSetup / advancedSetup).
# - Las acciones están pensadas para ser interpretadas y aplicadas por el script principal.
# - Ajusta valores según tu experiencia o el coche específico; estos son valores iniciales recomendados.

RECOMENDACIONES = {
    "Frenos": {
        "No se detiene a tiempo": [
            {
                "accion": "Aumentar presión de frenos delanteros",
                "change": "+3",
                "unit": "psi",
                "path": ["basicSetup", "mechanicalBalance", "brakeTorque"],  # ejemplo, puede variar por setup
                "desc": "Incrementar la fuerza de frenado aumentando presión/calibración de los frenos delanteros."
            },
            {
                "accion": "Avanzar reparto de frenada (más adelante)",
                "change": "+1",
                "unit": "%",
                "path": ["basicSetup", "mechanicalBalance", "brakeBias"],
                "desc": "Mover el reparto hacia el eje delantero para aumentar eficacia en frenadas largas."
            },
            {
                "accion": "Aumentar refrigeración de frenos",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "aeroBalance", "brakeDuct"],
                "desc": "Abrir conductos de freno para evitar fading en stints largos."
            }
        ],
        "Se detiene muy pronto": [
            {
                "accion": "Disminuir presión de frenos delanteros",
                "change": "-3",
                "unit": "psi",
                "path": ["basicSetup", "mechanicalBalance", "brakeTorque"],
                "desc": "Reducir presión si el coche frena demasiado en distancias cortas (evita bloquear o perder ritmo)."
            },
            {
                "accion": "Retrasar reparto de frenada (más atrás)",
                "change": "-1",
                "unit": "%",
                "path": ["basicSetup", "mechanicalBalance", "brakeBias"],
                "desc": "Mover reparto hacia atrás para reducir la frenada delantera excesiva."
            }
        ],
        "Patina cuando freno - delantero": [
            {
                "accion": "Reducir presión freno delantero",
                "change": "-2",
                "unit": "psi",
                "path": ["basicSetup", "mechanicalBalance", "brakeTorque"],
                "desc": "Disminuir presión para evitar bloqueo y pérdida de agarre delantero."
            },
            {
                "accion": "Retrasar reparto de frenada",
                "change": "-1",
                "unit": "%",
                "path": ["basicSetup", "mechanicalBalance", "brakeBias"],
                "desc": "Mover reparto hacia atrás cuando las ruedas delanteras bloquean con facilidad."
            },
            {
                "accion": "Aumentar ABS (suavizar) si está disponible",
                "change": "+1",
                "unit": "pts",
                "path": ["basicSetup", "electronics", "abs"],
                "desc": "Subir nivel de ABS para reducir bloqueo bajo frenada."
            }
        ],
        "Patina cuando freno - trasero": [
            {
                "accion": "Reducir presión freno trasero",
                "change": "-2",
                "unit": "psi",
                "path": ["basicSetup", "mechanicalBalance", "brakeTorque"],
                "desc": "Disminuir presión de freno trasero (o ajustar por eje si el setup lo permite)."
            },
            {
                "accion": "Avanzar reparto de frenada",
                "change": "+1",
                "unit": "%",
                "path": ["basicSetup", "mechanicalBalance", "brakeBias"],
                "desc": "Mover reparto hacia adelante para prevenir bloqueo trasero durante frenadas fuertes."
            },
            {
                "accion": "Aumentar TC (si patina salida de curva al frenar)",
                "change": "+1",
                "unit": "pts",
                "path": ["basicSetup", "electronics", "tC1"],
                "desc": "Incrementar control de tracción para ayudar a controlar patinadas traseras."
            }
        ],
        "Frena bien pero bloquea esporádicamente": [
            {
                "accion": "Reducir presión de frenos en 1-2 PSI",
                "change": "-1",
                "unit": "psi",
                "path": ["basicSetup", "mechanicalBalance", "brakeTorque"],
                "desc": "Ajuste fino para evitar picos de bloqueo sin perder mucho rendimiento."
            },
            {
                "accion": "Incrementar ABS 1 punto",
                "change": "+1",
                "unit": "pts",
                "path": ["basicSetup", "electronics", "abs"],
                "desc": "Incrementar ABS para evitar bloqueo intermitente."
            }
        ]
    },

    "Aerodinámica": {
        "Voy muy lento en rectas": [
            {
                "accion": "Reducir alerón trasero",
                "change": "-1",
                "unit": "mm",
                "path": ["advancedSetup", "aeroBalance", "rearWing"],
                "desc": "Disminuir carga trasera para reducir drag y ganar velocidad punta."
            },
            {
                "accion": "Reducir alerón delantero / splitter",
                "change": "-1",
                "unit": "mm",
                "path": ["advancedSetup", "aeroBalance", "splitter"],
                "desc": "Reducir carga delantera si el coche pierde mucha velocidad en recta."
            },
            {
                "accion": "Ajustar altura trasera (bajar)",
                "change": "-1",
                "unit": "mm",
                "path": ["advancedSetup", "aeroBalance", "rideHeight", 1],
                "desc": "Bajar la parte trasera puede reducir drag en algunos coches."
            }
        ],
        "Patino en curvas rápidas": [
            {
                "accion": "Aumentar alerón trasero",
                "change": "+2",
                "unit": "mm",
                "path": ["advancedSetup", "aeroBalance", "rearWing"],
                "desc": "Más carga en la parte trasera para mejorar estabilidad en curvas rápidas."
            },
            {
                "accion": "Aumentar splitter/aleta delantera",
                "change": "+1",
                "unit": "mm",
                "path": ["advancedSetup", "aeroBalance", "splitter"],
                "desc": "Aumentar carga delantera ayuda al giro en curvas rápidas."
            }
        ],
        "El auto no gira en curvas (subviraje)": [
            {
                "accion": "Aumentar carga delantera",
                "change": "+1",
                "unit": "mm",
                "path": ["advancedSetup", "aeroBalance", "splitter"],
                "desc": "Incrementar 'splitter' o carga delantera para ayudar a que gire."
            },
            {
                "accion": "Reducir alerón trasero 1 punto",
                "change": "-1",
                "unit": "mm",
                "path": ["advancedSetup", "aeroBalance", "rearWing"],
                "desc": "Reducir carga trasera puede reducir subviraje."
            }
        ],
        "Oscilaciones a alta velocidad (flutter)": [
            {
                "accion": "Aumentar alerón trasero 1 punto",
                "change": "+1",
                "unit": "mm",
                "path": ["advancedSetup", "aeroBalance", "rearWing"],
                "desc": "Ajustes para estabilizar el coche a velocidad alta; revisar también rigidez y amortiguadores."
            },
            {
                "accion": "Subir altura delantera 1 mm",
                "change": "+1",
                "unit": "mm",
                "path": ["advancedSetup", "aeroBalance", "rideHeight", 0],
                "desc": "Pequeños cambios en altura pueden suavizar la respuesta aerodinámica."
            }
        ]
    },

    "Suspensión / Agarre Mecánico": {
        "El auto no gira en curvas - entrada": [
            {
                "accion": "Aumentar rigidez delantera (ARB Front)",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "mechanicalBalance", "aRBFront"],
                "desc": "Mayor rigidez frontal para mejorar respuesta de giro en entrada."
            },
            {
                "accion": "Bajar altura delantera",
                "change": "-1",
                "unit": "mm",
                "path": ["advancedSetup", "aeroBalance", "rideHeight", 0],
                "desc": "Bajar ligeramente la suspensión delantera para aumentar agarre."
            }
        ],
        "El auto no gira en curvas - a lo largo": [
            {
                "accion": "Aumentar rigidez trasera (ARB Rear)",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "mechanicalBalance", "aRBRear"],
                "desc": "Refuerza la parte trasera para mantener el coche estable durante la curva."
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
                "desc": "Elevar ligeramente la parte trasera para más tracción en salida."
            }
        ],
        "El auto gira demasiado (sobreviraje)": [
            {
                "accion": "Reforzar barra estabilizadora delantera (más stiff)",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "mechanicalBalance", "aRBFront"],
                "desc": "Aumentar rigidez frontal para reducir sobreviraje."
            },
            {
                "accion": "Reducir rigidez trasera",
                "change": "-1",
                "unit": "pts",
                "path": ["advancedSetup", "mechanicalBalance", "aRBRear"],
                "desc": "Suavizar trasera para más agarre y menos giro excesivo."
            }
        ],
        "Neumáticos se desgastan rápido / se sobrecalientan": [
            {
                "accion": "Reducir rigidez delantera",
                "change": "-1",
                "unit": "pts",
                "path": ["advancedSetup", "mechanicalBalance", "aRBFront"],
                "desc": "Menos rigidez frontal puede equilibrar el desgaste en pistas con muchas curvas."
            },
            {
                "accion": "Aumentar presión de neumáticos 0.5 psi (si necesario)",
                "change": "+0.5",
                "unit": "psi",
                "path": ["basicSetup", "tyres", "tyrePressure"],
                "desc": "Ajuste de presión para controlar la temperatura y el desgaste."
            }
        ],
        "Dirección lenta o con mucha relación (steer ratio)": [
            {
                "accion": "Reducir relación de giro (más directo)",
                "change": "-1",
                "unit": "pts",
                "path": ["basicSetup", "alignment", "steerRatio"],
                "desc": "Reducir el ratio para una dirección más rápida y directa."
            }
        ]
    },

    "Amortiguadores": {
        "Rebote / bouncy (rebotan al salir de curva)": [
            {
                "accion": "Aumentar rebound slow (reboundSlow) trasero",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "dampers", "reboundSlow", 2],  # ejemplo índice
                "desc": "Aumentar la extensión lenta para controlar el rebote en salidas."
            },
            {
                "accion": "Aumentar bump slow (bumpSlow) delantero",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "dampers", "bumpSlow", 0],
                "desc": "Controlar compresión lenta para estabilizar asentamiento del coche."
            }
        ],
        "Amortiguación demasiado dura en compresión rápida": [
            {
                "accion": "Disminuir bump fast",
                "change": "-1",
                "unit": "pts",
                "path": ["advancedSetup", "dampers", "bumpFast", 0],
                "desc": "Suavizar compresión rápida para mayor tracción en baches y kerbs."
            }
        ],
        "Carro demasiado blando en frenada (nose dive)": [
            {
                "accion": "Aumentar compresión delantera",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "dampers", "bumpSlow", 0],
                "desc": "Más compresión delantera disminuye hundimiento en frenadas."
            }
        ]
    },

    "Electrónica": {
        "Acelera muy despacio (perdida tracción en salida)": [
            {
                "accion": "Reducir nivel de TC (si es demasiado intrusivo)",
                "change": "-1",
                "unit": "pts",
                "path": ["basicSetup", "electronics", "tC1"],
                "desc": "Bajar TC permite más potencia entregada, pero requiere control del piloto."
            },
            {
                "accion": "Aumentar TC en caso de pérdida de tracción constante",
                "change": "+1",
                "unit": "pts",
                "path": ["basicSetup", "electronics", "tC1"],
                "desc": "Si el coche patina, subir TC ayuda a mantener tracción."
            }
        ],
        "Frenada inestable con ABS": [
            {
                "accion": "Reducir ABS 1 punto",
                "change": "-1",
                "unit": "pts",
                "path": ["basicSetup", "electronics", "abs"],
                "desc": "Ajuste fino del ABS para que no intervenga de forma irregular."
            }
        ],
        "Mapa motor / aceleración inconsistente": [
            {
                "accion": "Probar otro mapa ECU",
                "change": "+1",
                "unit": "pts",
                "path": ["basicSetup", "electronics", "eCUMap"],
                "desc": "Cambiar map de ECU para ajustar respuesta del motor."
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
        "PSI traseros bajo/alto": [
            {
                "accion": "Aumentar PSI trasero 0.5 psi",
                "change": "+0.5",
                "unit": "psi",
                "path": ["basicSetup", "tyres", "tyrePressure", 2],
                "desc": "Ajuste fino trasero izquierdo."
            },
            {
                "accion": "Aumentar PSI trasero 0.5 psi (derecho)",
                "change": "+0.5",
                "unit": "psi",
                "path": ["basicSetup", "tyres", "tyrePressure", 3],
                "desc": "Ajuste fino trasero derecho."
            }
        ],
        "Desgaste exterior en delantero (carcasa caliente)": [
            {
                "accion": "Incrementar camber (menos negativo) 0.1°",
                "change": "+0.1",
                "unit": "deg",
                "path": ["basicSetup", "alignment", "staticCamber", 0],
                "desc": "Reducir extremo de caída para minimizar desgaste exterior."
            },
            {
                "accion": "Reducir presión 0.3 psi",
                "change": "-0.3",
                "unit": "psi",
                "path": ["basicSetup", "tyres", "tyrePressure", 0],
                "desc": "Ajuste fino de presión para equilibrar la huella."
            }
        ],
        "Desgaste interior (exceso de camber negativo)": [
            {
                "accion": "Hacer camber menos negativo 0.1°",
                "change": "+0.1",
                "unit": "deg",
                "path": ["basicSetup", "alignment", "staticCamber", 0],
                "desc": "Menos caída negativa reduce desgaste interior."
            }
        ],
        "Desgaste desigual entre ejes": [
            {
                "accion": "Ajustar toe en el eje correspondiente 0.05°",
                "change": "+0.05",
                "unit": "deg",
                "path": ["basicSetup", "alignment", "toe", 0],
                "desc": "Pequeños ajustes de toe para equilibrar la huella."
            }
        ]
    },

    # Opciones avanzadas / misc
    "Avanzado / Drivetrain": {
        "Diferencial patina en salida": [
            {
                "accion": "Aumentar preload diferencial",
                "change": "+10",
                "unit": "Nm",
                "path": ["advancedSetup", "drivetrain", "preload"],
                "desc": "Mayor preload para reducir giro diferencial y mejorar salida."
            }
        ],
        "El coche vibra en baches a baja velocidad": [
            {
                "accion": "Aumentar tope de suspensión (bump stop rate up) trasero",
                "change": "+1",
                "unit": "pts",
                "path": ["advancedSetup", "mechanicalBalance", "bumpStopRateUp", 2],
                "desc": "Evitar que la suspensión vaya al fondo en baches fuertes."
            }
        ]
    }
}

# Export-friendly alias
# (mantener RECOMENDACIONES como la fuente principal)
