# Astra Blender Workflow — Diretrizes Técnicas para Modelagem 3D

**Destinatário:** Agente Astra (e modeladores 3D do projeto Runner Collectible)  
**Versão:** 1.0  
**Status:** VIGENTE / NORMATIVO  
**Referência Normativa:** `AGENTS.md`, `docs/PROJECT_SPEC.md`, `docs/DECISIONS.md`, `docs/SAFETY_RULES.md`

---

## 1. Objetivo

Este documento define o protocolo técnico obrigatório para o modelador 3D / agente Astra durante a construção modular do personagem colecionável runner para impressão FDM na Flashforge AD5X.

O ambiente de trabalho padronizado encontra-se em:
`output/blender/runner_workspace_v001.blend`

---

## 2. Regras Mandatórias de Engenharia e Modelagem

1. **Trabalhar por versões incrementais:**
   - Cada entrega ou avanço de etapa deve gerar um novo arquivo `.blend` e nova pasta de renders (ex.: `runner_blockout_v002.blend`, `renders/v002/`).
2. **Nunca sobrescrever versão aprovada:**
   - Arquivos como `output/blender/runner_blockout_v001.blend`, `output/blender/runner_refinement_v002.blend` ou renders aprovados são imutáveis.
3. **Preservar nomes estáveis de objetos:**
   - Proibido manter nomes automáticos como `Cube.001`, `Sphere.014`, `Cylinder.003`.
   - Utilizar exclusivamente os nomes aprovados da arquitetura modular.
4. **Manter peças modulares estritamente separadas:**
   - Cada parte do corpo e acessório é um objeto independente.
5. **Não unir o personagem prematuramente:**
   - Proibido executar `Join` (`Ctrl+J`) ou aplicar uniões booleanas destrutivas unificando módulos do personagem. A arquitetura modular é indispensável para impressão multicolor, acabamento e orientações otimizadas de impressão.
6. **Não criar conectores durante o blockout:**
   - Conforme a Decisão Congelada **D-010**, pinos, cavidades, folgas e tolerâncias de encaixe serão definidos por corpos de prova físicos na AD5X, não por estimativa digital.
7. **Sempre gerar os 4 renders antes de declarar etapa concluída:**
   - Toda etapa deve registrar `front.png`, `side.png`, `back.png` e `three_quarter.png` usando o script `scripts/blender/render_views.py`.
8. **Alterações devem ser reversíveis:**
   - Priorizar modificadores (`BEVEL`, `SUBSURF`, `MIRROR`, `SOLIDIFY`) sem aplicá-los destrutivamente na malha base enquanto a forma estiver em aprovação.
9. **Nenhum STL final do personagem antes do QA:**
   - Exportações intermediárias destinam-se exclusivamente a corpos de prova e calibração (`CALIBRATION_CUBE_20MM`).
10. **Nenhum G-code manual:**
    - Fatiamento de produção deve ser feito via perfil oficial no slicer (OrcaSlicer / FlashPrint).
11. **Nenhum comando para a impressora:**
    - Proibido enviar comandos diretamente para o hardware.

---

## 3. Estrutura de Collections no Workspace

O workspace organiza a cena nas seguintes collections padronizadas:

| Collection | Finalidade | Regras de Uso |
|---|---|---|
| `00_REFERENCES` | Imagens de referência, turnaround e concept | Planos com material neutro ou empty images. Desabilitar render. |
| `01_CAMERAS` | Câmeras de inspeção e QA | Contém `TARGET_FRAME`, `CAM_FRONT`, `CAM_SIDE`, `CAM_BACK`, `CAM_3Q`. |
| `02_LIGHTING` | Iluminação neutra de estúdio | Contém `LIGHT_KEY`, `LIGHT_FILL`, `LIGHT_RIM` e background neutro. |
| `10_BLOCKOUT` | Primitivas e blocos da etapa de blocagem | Volumes primários, proporções e silhueta. |
| `20_CHARACTER` | Malhas refinadas de produção | Geometria detalhada das peças definitivas. |
| `30_ENGINEERING` | Calibração, conectores e testes | Contém `CALIBRATION_CUBE_20MM`, futuros corpos de prova. |
| `90_TEMP` | Geometria de rascunho, booleanas auxiliares | Objetos temporários; devem ser purgados antes da entrega. |

---

## 4. Convenção de Nomenclatura dos Objetos do Personagem

Ao modelar na collection `10_BLOCKOUT` ou `20_CHARACTER`, utilize rigorosamente os nomes:

- `HEAD` — Cabeça estilizada
- `HAIR` — Cabelo curto branco/grisalho em grandes volumes
- `CAP` — Boné / viseira (quando aplicável)
- `GLASSES` — Armação e lentes dos óculos escuros robustos
- `TORSO` — Tronco e regata
- `SHORTS` — Bermuda de corrida
- `ARM_L` — Braço esquerdo
- `ARM_R` — Braço direito
- `LEG_L` — Perna esquerda
- `LEG_R` — Perna direita
- `KICHUTE_L` — Tênis esquerdo inspirado no Kichute clássico (sem marcas)
- `KICHUTE_R` — Tênis direito inspirado no Kichute clássico (sem marcas)
- `BASE` — Base de apoio para fixação do collectible

Submódulos permitidos devem usar sufixos explícitos (ex.: `KICHUTE_L_SOLE`, `GLASSES_FRAME`, `GLASSES_LENS`).

---

## 5. Unidades e Escala de Impressão 3D

- **Sistema:** Métrico (`METRIC`)
- **Escala de Unidade:** `0.001` (1 Blender Unit = 1 milímetro)
- **Unidade de Comprimento:** Milímetros (`MILLIMETERS`)
- **Regra de ouro:** Todo objeto criado com dimensão `20 mm` tem medida de `20.0` no Blender e exporta diretamente em milímetros para o OrcaSlicer.
- **Importante:** Sempre aplique a escala (`Ctrl+A` -> *Scale*) antes de qualquer exportação ou análise física. Objetos com escala diferente de `(1.0, 1.0, 1.0)` geram alerta no `scene_audit.py`.

---

## 6. Ferramentas e Scripts de Automação

O Astra deve utilizar os scripts utilitários fornecidos em `scripts/blender/`:

### 6.1. Auditoria de Cena (`scene_audit.py`)
Executa inspeção estrita sem alterar a cena:
```bash
blender <arquivo.blend> --background --factory-startup --python-exit-code 1 --python scripts/blender/scene_audit.py
```
Gera relatório com unidades, collections, lista de objetos, dimensões, escala, contagem de vértices/faces e lista de anomalias (como `.001` ou escalas não aplicadas).

### 6.2. Renderizador Multi-Ângulo (`render_views.py`)
Gera automaticamente as 4 vistas padronizadas enquadrando o personagem ou collection:
```bash
blender <arquivo.blend> --background --factory-startup --python-exit-code 1 --python scripts/blender/render_views.py -- --output-dir renders/v00X --target 20_CHARACTER --samples 32
```
Vistas geradas:
- `front.png` (Ortográfica frontal)
- `side.png` (Ortográfica lateral)
- `back.png` (Ortográfica posterior)
- `three_quarter.png` (Perspectiva 3/4 com lente 85mm)

### 6.3. Smoke Test de Validação do Pipeline (`smoke_test.py`)
Testa o ciclo completo de operações, render e persistência:
```bash
blender --background --factory-startup --python-exit-code 1 --python scripts/blender/smoke_test.py
```
Também pode ser validado pela suíte pytest:
```bash
.venv/bin/pytest tests/test_workspace_pipeline.py
```

---

## 7. Critérios de Pronto (Definition of Done) para o Astra

Uma etapa só pode ser dada como concluída quando:
1. O arquivo `.blend` foi salvo com a nova versão sem sobrescrever anteriores;
2. Todos os objetos pertencem às collections designadas e possuem nomes padronizados;
3. Todas as escalas estão aplicadas (`scale = (1.0, 1.0, 1.0)`);
4. O script `scene_audit.py` retorna `[PASS]` sem erros;
5. Os renders das 4 vistas foram gerados na pasta de versão correspondente;
6. Nenhuma regra de segurança ou decisão congelada foi infringida;
7. O relatório da versão foi registrado documentando as decisões e limites.
