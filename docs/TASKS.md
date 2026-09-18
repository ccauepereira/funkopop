# Runner Collectible 3D — Tasks V1

**Estado atual:** documentação e Concept Art V1 consolidados. T-010, T-011, T-012 e T-013 concluídas; T-014 pronta para início.

## Gate de entrada

O estado atual foi registrado em `PROJECT_SPEC.md`, `VISUAL_SPEC.md`, `DECISIONS.md`, `ENGINEERING_NOTES.md` e `docs/research/README.md`. T-013 está concluída com aprovação humana e T-014 pode começar.

| ID | Tarefa | Estado | Dependência | Critério de aceite |
|---|---|---|---|---|
| T-010 | Bootstrap Blender | CONCLUÍDA | Documentação consolidada | Estrutura mínima, execução reprodutível e sem geometria do personagem. |
| T-011 | Blender Smoke Test | CONCLUÍDA | T-010 | Abrir/executar o ambiente e registrar resultado sem modelar o personagem. |
| T-012 | Turnaround V1 | CONCLUÍDA | T-010, T-011 e Concept Art V1 | Frontal, perfis e costas consistentes, sem dimensões inventadas. |
| T-013 | Geometric Spec V1 | CONCLUÍDA | T-012 | Razões e decisões geométricas aprovadas; escala ainda baseada em evidência. |
| T-014 | Character JSON V1 | PRONTA PARA INICIAR | T-013 | Apenas parâmetros respaldados pela Geometric Spec; sem tolerâncias inventadas. |
| T-015 | Blockout V001 | BLOQUEADA | T-014 | Módulos com nomes estáveis, sem detalhes frágeis ou conectores finais. |
| T-016 | Visual QA V001 | BLOQUEADA | T-015 | Comparação documentada com Concept/Turnaround e lista de correções. |

## Trabalho técnico paralelo, não bloqueante

- Preparar os corpos de prova de dimensionalidade, conectores, óculos, cabelo e base descritos na pesquisa.
- Registrar firmware, slicer, perfil, PLA, bico de 0,4 mm e resultados antes de transformar qualquer hipótese em decisão.
- Não iniciar modelagem de conectores finais nem fatiamento de produção.

## Não autorizado nesta etapa

- código Blender para o personagem;
- definição de medidas absolutas;
- criação de conectores definitivos;
- STL/3MF final;
- G-code manual.
