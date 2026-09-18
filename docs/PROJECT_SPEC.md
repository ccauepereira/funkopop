# Runner Collectible 3D — Project Specification V1

**Repositório:** `ccauepereira/funkopop`
**Branch de trabalho atual:** `main`
**Estado:** pronto para iniciar a preparação técnica; nenhuma geometria, `.blend`, STL, 3MF ou G-code final foi produzido.

## Objetivo

Criar um personagem colecionável 3D original de um corredor de aparência madura, preparado para futura impressão FDM. A identidade visual é inspirada no homem de referência aprovado pelo diretor; o resultado deve ser estilizado e reconhecível, não uma réplica realista.

O **Concept Art V1 está aprovado como referência visual inicial**. Ele orienta silhueta, linguagem de formas e organização modular, mas não é uma especificação dimensional nem substitui um turnaround.

## Estado visual consolidado

- corredor de aparência madura;
- cabelo curto branco/grisalho em grandes volumes;
- óculos escuros de armação robusta;
- cabeça proporcionalmente grande e corpo compacto;
- regata e shorts escuros provisórios, sem marcas ou textos;
- tênis preto inspirado no Kichute clássico, sem logotipo ou reprodução de marca;
- pose de corrida dinâmica, porém estruturalmente simples, sobre base.

## Arquitetura do ativo

O personagem será multipartes, com módulos independentes sempre que isso melhorar fabricação, acabamento, multicolor ou iteração:

`HEAD`, `HAIR`, `GLASSES`, `TORSO`, `ARM_L`, `ARM_R`, `SHORTS`, `LEG_L`, `LEG_R`, `KICHUTE_L`, `KICHUTE_R` e `BASE`.

Conectores não fazem parte da aparência do concept e não serão definidos antes de corpos de prova físicos.

## Fabricação-alvo

| Item | Estado oficial |
|---|---|
| Processo | FDM |
| Impressora | Flashforge AD5X |
| Bico de partida | 0,4 mm |
| Material inicial de experimentação | PLA |
| Escalas candidatas | 120 mm e 140 mm — **não aprovadas** |
| Material definitivo, escala definitiva e perfil de slicer | PENDENTES de testes |

## Restrições

- Não usar Meshy, Tripo, Rodin, Hunyuan 3D ou IA externa de geração automática de mesh.
- A geometria futura será criada por Blender, Python/bpy, NumPy, OpenCV e operações tradicionais/procedurais permitidas.
- Não inventar dimensões, espessuras, tolerâncias, ângulos de suporte ou conectores.
- Não escrever G-code manualmente; a impressão será fatiada por perfil aprovado no slicer compatível com a AD5X.
- Não copiar marcas, logotipos ou elementos proprietários do Kichute ou de brinquedos comerciais.

## Critérios para avançar a implementação

1. Ambiente Blender inicializado e smoke test concluído.
2. Turnaround V1 registrado a partir do Concept Art V1.
3. Geometric Spec V1 aprovada, com razões e escala selecionada sem suposições.
4. `character.json` criado somente com parâmetros respaldados pela Geometric Spec.
5. Conectores e detalhes delicados mantidos como hipóteses até ensaio físico na AD5X.

## Referências normativas internas

- `docs/VISUAL_SPEC.md`: fidelidade visual e lacunas.
- `docs/DECISIONS.md`: decisões congeladas e em teste.
- `docs/TASKS.md`: ordem autorizada de trabalho.
- `docs/ENGINEERING_NOTES.md`: limites técnicos para a primeira implementação.
- `docs/research/README.md`: índice da evidência de fabricação.
