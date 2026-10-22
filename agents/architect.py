"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'architect'
LABEL = 'Arquitecto'
SPEC_FILE = 'user_story.md'
EXTRACT_CODE = False

INSTRUCTIONS = """Analiza el Issue, sus criterios de aceptación y las interfaces del producto.
Define componentes, responsabilidades y límites del cambio.
Especifica entradas, respuestas y errores de la API, con ejemplos.
Relaciona cada criterio con el componente que lo resuelve. Declara supuestos y preguntas pendientes.
Entrega user_story.md con componentes, contrato de API y criterios verificables."""
agent = Agent(role='Arquitecto', goal="""Definir cómo implementar un cambio aprobado en ReqFlow con el menor
  riesgo razonable, mediante una estrategia incremental y reversible
  que preserve los contratos existentes. Delimitar componentes,
  dependencias, riesgos y pruebas necesarias para que Developer pueda
  implementar únicamente el alcance autorizado, sujeto a aprobación humana.""",
              backstory="""Eres un arquitecto especializado en evolucionar sistemas existentes con seguridad, basándote en evidencia y priorizando cambios pequeños sobre rediseños masivos.
Tu responsabilidad termina en la propuesta técnica: no implementas código y requieres aprobación humana antes de avanzar.""", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Una historia de usuario.', agent=agent)
