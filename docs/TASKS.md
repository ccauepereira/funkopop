# Runner Collectible 3D — Tasks V1

**Estado atual:** documentação e Concept Art V1 consolidados. T-010 a T-016 concluídas; T-017 em validação.

## Gate de entrada

O estado atual foi registrado em `PROJECT_SPEC.md`, `VISUAL_SPEC.md`, `DECISIONS.md`, `ENGINEERING_NOTES.md` e `docs/research/README.md`. O Refinamento V002 (T-017) está em validação visual e aguarda revisão humana, visando aproximar o modelo do Turnaround V1 aprovado, sem aprovação de fabricação.

| ID | Tarefa | Estado | Dependência | Critério de aceite |
|---|---|---|---|---|
| T-010 | Bootstrap Blender | CONCLUÍDA | Documentação consolidada | Estrutura mínima, execução reprodutível e sem geometria do personagem. |
| T-011 | Blender Smoke Test | CONCLUÍDA | T-010 | Abrir/executar o ambiente e registrar resultado sem modelar o personagem. |
| T-012 | Turnaround V1 | CONCLUÍDA | T-010, T-011 e Concept Art V1 | Frontal, perfis e costas consistentes, sem dimensões inventadas. |
| T-013 | Geometric Spec V1 | CONCLUÍDA | T-012 | Razões e decisões geométricas aprovadas; escala ainda baseada em evidência. |
| T-014 | Character JSON V1 | CONCLUÍDA | T-013 | Contrato conceitual de módulos aprovado em revisão humana; sem JSON físico de fabricação ou tolerâncias inventadas. |
| T-015 | Blockout V001 | CONCLUÍDA | T-014 | Módulos com nomes estáveis, sem detalhes frágeis ou conectores finais. |
| T-016 | Visual QA V001 | CONCLUÍDA | T-015 | Comparação documentada com Concept/Turnaround e lista de correções. |
| T-017 | Refinamento V002 | EM VALIDAÇÃO | T-016 | Aproximação visual do Turnaround V1 (mechas, rosto, membros, calçado); sem aprovação de fabricação. |

## Trabalho técnico paralelo, não bloqueante

- Preparar os corpos de prova de dimensionalidade, conectores, óculos, cabelo e base descritos na pesquisa.
- Registrar firmware, slicer, perfil, PLA, bico de 0,4 mm e resultados antes de transformar qualquer hipótese em decisão.
- Não iniciar modelagem de conectores finais nem fatiamento de produção.

## Não autorizado nesta etapa

- código Blender além do blockout T-015 autorizado em unidades relativas;
- definição de medidas absolutas;
- criação de conectores definitivos;
- STL/3MF final;
- G-code manual.
