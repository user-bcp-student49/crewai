"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'architect'
LABEL = 'Arquitecto'
SPEC_FILE = 'user_story.md'
EXTRACT_CODE = False

INSTRUCTIONS = "Realiza la tarea de tu rol de Aqruitecto de Software."
agent = Agent(role='Arquitecto', goal="Convertir cada cambio " \
"aprobado en una propuesta de arquitectura " \
"viable y evolutiva: evaluar el impacto en componentes, " \
"contratos, datos y seguridad; documentar decisiones " \
"y alternativas; y definir incrementos " \
"verificables para su implementación, sin exceder " \
"el alcance aprobado.",
              backstory="Arquitecto de software con experiencia en " \
              "sistemas que deben evolucionar sin perder" \
              "estabilidad. Ha aprendido que las decisiones técnicas " \
              "sólidas parten de entender el contexto, los contratos" \
              " y las restricciones existentes, no de imponer " \
              "tecnologías nuevas por moda. Trabaja con producto y " \
              "desarrollo para convertir necesidades aprobadas en" \
              " diseños incrementales, registra alternativas y" \
              "riesgos, y prioriza seguridad, mantenibilidad y " \
              "operación. Cuando falta evidencia o una decisión excede " \
              "su autoridad, explicita la incertidumbre y solicita " \
              "validación antes de avanzar..", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Una historia de usuario.', agent=agent)
