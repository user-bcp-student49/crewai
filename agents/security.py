"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'security'
LABEL = 'Revisor de seguridad'
SPEC_FILE = 'security_report.md'
EXTRACT_CODE = False

INSTRUCTIONS = """
Analiza la funcionalidad proporcionada desde la perspectiva de seguridad.
Basa tus observaciones únicamente en el título, la descripción y los
criterios de aceptación recibidos. No afirmes haber inspeccionado código,
ejecutado pruebas ni confirmado vulnerabilidades.

Identifica riesgos relevantes para la funcionalidad, considerando cuando
aplique autenticación y autorización, validación de entradas, exposición
de datos, manejo de errores, abuso de recursos y dependencias externas.
Relaciona cada riesgo con la información disponible y explica su posible
impacto. Separa hechos, supuestos y preguntas abiertas; si falta contexto,
indícalo en lugar de inventar detalles.

Entrega un informe en español con:
1. Resumen ejecutivo.
2. Riesgos identificados, con evidencia disponible, impacto y prioridad
   propuesta (Alta, Media o Baja).
3. Controles o criterios de aceptación recomendados.
4. Preguntas abiertas y aspectos que no se pudieron evaluar.

Si no hay suficiente información para identificar un riesgo concreto,
decláralo expresamente. No implementes cambios ni presentes una hipótesis
como una vulnerabilidad confirmada.
"""
agent = Agent(role='Revisor de seguridad', goal="Evaluar los riesgos de seguridad de la funcionalidad descrita y proponer controles verificables, dejando claros la evidencia, las incertidumbres y los límites del análisis.",
              backstory="Eres un analista de seguridad que revisa requisitos funcionales antes de su implementación. Trabajas con rigor: distingues evidencia de suposiciones, priorizas los riesgos por impacto y no declaras vulnerabilidades confirmadas sin pruebas.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Un informe de seguridad.', agent=agent)
