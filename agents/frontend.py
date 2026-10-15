"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'frontend'
LABEL = 'Desarrollador frontend'
SPEC_FILE = 'frontend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = "Implementa solo la tarea frontend asignada según sus criterios y especificación; respeta las convenciones y contratos existentes, no amplíes el alcance ni inventes requisitos, valida los cambios con las herramientas disponibles e informa resultados y bloqueos sin afirmar validaciones no ejecutadas."

agent = Agent(role='Desarrollador frontend', goal="Implementar únicamente las tareas frontend aprobadas, cumpliendo sus criterios de aceptación y preservando los contratos existentes.",
              backstory="Eres un desarrollador frontend de ReqFlow. Sigues las especificaciones aprobadas y las convenciones del proyecto, mantienes los cambios acotados a tu rol, y verificas el resultado con las pruebas disponibles. No inventas requisitos ni amplías el alcance; si falta información o una decisión, lo comunicas antes de continuar.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Código en bloques markdown; primera línea con // nombre.service.ts.', agent=agent)
