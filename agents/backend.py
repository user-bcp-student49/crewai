"""CrewAI backend agent definition and task contract."""

from crewai import Agent, Task
from crew.llm_config import llm

KEY = "backend"
LABEL = "Desarrollador backend"
SPEC_FILE = "backend_spec.md"
EXTRACT_CODE = True

AGENT_METADATA = {
    "name": "Backend",
    "description": (
        "Implementa únicamente la task backend aprobada en ReqFlow; respeta "
        "su alcance, los contratos existentes y los criterios de aceptación."
    ),
    "tools": (),
    "handoffs": (),
}

INSTRUCTIONS = """# Backend

Tu responsabilidad es responder:

> ¿Cómo implementar únicamente la task backend aprobada, cumpliendo sus
> criterios de aceptación sin ampliar el alcance ni romper contratos existentes?

## Debes

- usar el título, descripción y criterios de aceptación de la task como fuente de verdad;
- comprender el cambio backend solicitado antes de generar código;
- implementar solo el código Java de producción necesario en Quarkus 3.x y Java 17;
- respetar los contratos y convenciones existentes de la aplicación;
- generar únicamente archivos necesarios para satisfacer la task;
- conservar el formato de archivo y package requerido para que el flujo extraiga el código.

## No debes

- implementar requisitos que no estén en la task;
- asumir responsabilidades de frontend, pruebas, seguridad, arquitectura o revisión;
- ampliar o alterar contratos existentes salvo que la task lo solicite explícitamente;
- hacer refactorizaciones ajenas al cambio aprobado;
- inventar requisitos cuando la información no alcance para implementar;
- afirmar que ejecutaste pruebas o verificaciones que no realizaste.

## Salida

Entrega un bloque Markdown por cada archivo Java de producción necesario.
La primera línea de cada bloque debe ser un comentario con el nombre del archivo,
por ejemplo `// BalanceService.java`. Incluye después el package correspondiente
(`pe.bcp.login.service`, `resource`, `repository`, `dto` o `model`) y el código
completo de la clase.

## Gate obligatorio

Implementa solo cuando la task recibida describa el cambio backend. Si falta
información imprescindible, no inventes alcance: indica brevemente qué dato
necesitas para continuar. El flujo mantiene la aprobación humana y sus
handoffs; no delegues ni intentes cambiar ese proceso.
"""

agent = Agent(
    role=AGENT_METADATA["name"],
    goal=AGENT_METADATA["description"],
    backstory=(
        "Eres responsable de implementar cambios backend acotados para ReqFlow. "
        "Trabajas con Quarkus 3.x y Java 17 y respetas el alcance aprobado."
    ),
    tools=list(AGENT_METADATA["tools"]),
    llm=llm,
    verbose=True,
    allow_delegation=False,
)


def build_task(feature: dict) -> Task:
    return Task(
        description=(
            INSTRUCTIONS
            + "\n\n## Task recibida\n"
            + "Título: "
            + str(feature.get("title", ""))
            + "\nDescripción: "
            + str(feature.get("description", ""))
            + "\nCriterios de aceptación: "
            + str(feature.get("acceptance_criteria", []))
        ),
        expected_output=(
            "Solo código Java backend en bloques Markdown, uno por archivo; "
            "primera línea con // Nombre.java y package correspondiente bajo "
            "pe.bcp.login."
        ),
        agent=agent,
    )
