# Astra Blender Workspace V1 — Relatório Técnico de Preparação

**Data:** 19/09/2026  
**Ambiente:** Blender 4.0.2 (Linux x86_64, embedded Python 3.10 / venv Python 3.12.3)  
**Status do Pipeline:** APROVADO NO SMOKE TEST  
**Branch:** `main`

---

## 1. Resumo Executivo

O ambiente técnico e estrutural para a modelagem do personagem colecionável runner foi concluído e validado. Nenhuma geometria do personagem foi modelada prematuramente. O workspace foi construído para ser determinístico, reproduzível, com unidades métricas voltadas à impressão 3D (FDM na Flashforge AD5X), collections organizadas, câmeras com autoenquadramento, iluminação de estúdio neutra e ferramentas de inspeção e renderização automatizadas.

---

## 2. Arquivos Criados e Alterados

### 2.1. Arquivos Criados
| Arquivo | Finalidade |
|---|---|
| `scripts/blender/setup_workspace.py` | Script idempotente para inicialização e configuração do workspace Blender e exportação do cubo de calibração |
| `scripts/blender/render_views.py` | Ferramenta de renderização automatizada das 4 vistas (`front`, `side`, `back`, `three_quarter`) com auto-framing |
| `scripts/blender/scene_audit.py` | Ferramenta de auditoria estrita somente-leitura para validação de integridade da cena |
| `scripts/blender/smoke_test.py` | Script de teste de fumaça (criação, transformação, movimentação de collection, render, auditoria e limpeza) |
| `tests/test_workspace_pipeline.py` | Suíte de testes automatizados via `pytest` para integração contínua |
| `output/blender/runner_workspace_v001.blend` | Arquivo `.blend` do workspace configurado |
| `output/calibration/calibration_cube_20mm.stl` | Corpo de prova de 20 × 20 × 20 mm para validação de escala no OrcaSlicer |
| `renders/workspace_v001/front.png` | Render de validação da vista frontal |
| `renders/workspace_v001/side.png` | Render de validação da vista lateral |
| `renders/workspace_v001/back.png` | Render de validação da vista posterior |
| `renders/workspace_v001/three_quarter.png` | Render de validação da vista 3/4 em perspectiva controlada |
| `renders/smoke_test/smoke_*.png` | Artefatos visuais produzidos durante a execução do smoke test |
| `docs/ASTRA_BLENDER_WORKFLOW.md` | Guia normativo de boas práticas e regras para o agente Astra |
| `docs/ASTRA_WORKSPACE_V1_REPORT.md` | Este relatório técnico |

### 2.2. Arquivos Alterados
Nenhum arquivo pré-existente foi alterado. Artefatos aprovados (`runner_blockout_v001.blend`, `runner_refinement_v002.blend`) foram rigorosamente preservados.

---

## 3. Configurações Técnicas do Blender

### 3.1. Unidades e Escala de Impressão 3D
- **Versão do Blender:** 4.0.2
- **Sistema de unidades (`system`):** `METRIC`
- **Escala de unidade (`scale_length`):** `0.001` (1 Blender Unit = 1 milímetro)
- **Unidade de comprimento (`length_unit`):** `MILLIMETERS`
- **Rationale:** Com `scale_length = 0.001`, todas as coordenadas de malha no Blender correspondem diretamente a milímetros físicos. Na exportação STL com `use_scene_unit=False` e `global_scale=1.0`, cada unidade do arquivo STL corresponde a 1 mm, que é o padrão nativo interpretado por fatiadores FDM (OrcaSlicer, PrusaSlicer, Bambu Studio).

### 3.2. Estrutura de Collections
A cena contém as collections padronizadas:
1. `00_REFERENCES` — Referências visuais e turnarounds (sem renderização);
2. `01_CAMERAS` — `TARGET_FRAME`, `CAM_FRONT`, `CAM_SIDE`, `CAM_BACK`, `CAM_3Q`;
3. `02_LIGHTING` — `LIGHT_KEY`, `LIGHT_FILL`, `LIGHT_RIM`;
4. `10_BLOCKOUT` — Destinada à futura blocagem de volumes pelo Astra;
5. `20_CHARACTER` — Destinada às geometrias refinadas de produção;
6. `30_ENGINEERING` — Contém `CALIBRATION_CUBE_20MM` e corpos de prova;
7. `90_TEMP` — Espaço para operações booleanas e malhas temporárias.

### 3.3. Câmeras e Sistema de Autoenquadramento
- **`TARGET_FRAME`:** Empty no centro de interesse com o qual todas as câmeras mantêm restrição `TRACK_TO` (`-Z` track, `Y` up).
- **`CAM_FRONT`:** Projeção ortográfica (`ORTHO`), escala 60.0 mm, alinhada ao eixo Y negativo olhando para +Y.
- **`CAM_SIDE`:** Projeção ortográfica (`ORTHO`), escala 60.0 mm, alinhada ao eixo X positivo olhando para o perfil do personagem.
- **`CAM_BACK`:** Projeção ortográfica (`ORTHO`), escala 60.0 mm, alinhada ao eixo Y positivo olhando para -Y.
- **`CAM_3Q`:** Projeção perspectiva (`PERSP`), distância focal de 85.0 mm (perspectiva controlada sem distorção angular de grande-angular), posicionada em ângulo de 3/4 superior.
- **Limites de corte (`Clipping`):** `clip_start = 0.1 mm`, `clip_end = 10000.0 mm`.
- **Autoenquadramento:** Função matemática em `render_views.py` e `setup_workspace.py` que calcula a bounding box da collection/objeto alvo e recalcula automaticamente a posição e `ortho_scale`.

### 3.4. Iluminação Neutra de Estúdio
O setup de 3 pontos foi dimensionado em milímetros para priorizar leitura de silhueta, planos e volumes, com sombras suaves:
- **`LIGHT_KEY`:** Area light 400 mm, 120 W, posição `(-250, -350, 350)` mm, neutra `(1.0, 1.0, 1.0)`.
- **`LIGHT_FILL`:** Area light 500 mm, 60 W, posição `(300, -250, 200)` mm, suave `(0.95, 0.97, 1.0)`.
- **`LIGHT_RIM`:** Area light 300 mm, 90 W, posição `(0, 350, 400)` mm, contra-luz suave `(1.0, 0.98, 0.95)`.
- **Background:** Cinza escuro neutro `(0.12, 0.12, 0.12)` sem nódulos de iluminação indireta complexos, proporcionando contraste tanto para áreas claras (cabelo) quanto escuras (óculos, tênis).

---

## 4. Cubo de Calibração e Validação STL

- **Objeto:** `CALIBRATION_CUBE_20MM`
- **Collection:** `30_ENGINEERING`
- **Dimensões no Blender:** 20.00 × 20.00 × 20.00 mm
- **Posição:** `(0, 0, 10)` mm (base perfeitamente assentada no plano `Z = 0`)
- **Arquivo Exportado:** `output/calibration/calibration_cube_20mm.stl`
- **Propriedades da Exportação:**
  - Facetas: 12 triângulos (cubo perfeito)
  - Vértices mínimos: `[-10.0, -10.0, 0.0]`
  - Vértices máximos: `[10.0, 10.0, 20.0]`
  - Dimensões do envelope: `20.0 × 20.0 × 20.0`
  - Parâmetros do operador: `use_selection=True, use_scene_unit=False, global_scale=1.0, ascii=False, use_mesh_modifiers=True`

---

## 5. Resultado do Smoke Test

O smoke test (`scripts/blender/smoke_test.py`) foi executado e concluiu todos os passos com sucesso:

1. **Carga do arquivo:** Leitura bem-sucedida de `runner_workspace_v001.blend`.
2. **Validação de collections:** Todas as 7 collections verificadas.
3. **Criação de primitivas:** Criação de `ASTRA_TEST_CUBE` e `ASTRA_TEST_SPHERE` em `90_TEMP`.
4. **Transformação:** Translação, rotação e aplicação de escala normalizada (`scale = 1.0`).
5. **Movimentação entre collections:** Transferência de `90_TEMP` para `10_BLOCKOUT` confirmada.
6. **Renderização das 4 câmeras:** Geração comprovada dos arquivos em `renders/smoke_test/`.
7. **Auditoria de cena:** Detecção estrita de objetos, dimensões e ausência de anomalias.
8. **Persistência temporária:** Salvamento e reabertura de `.blend` de teste verificados.
9. **Purga:** Remoção completa dos objetos de teste (`ASTRA_TEST_*`).
10. **Preservação de engenharia:** `CALIBRATION_CUBE_20MM` mantido intacto em `30_ENGINEERING`.
11. **Suíte Pytest:** `3 passed in 8.46s` executando `tests/test_workspace_pipeline.py`.

---

## 6. Limitações Conhecidas

1. **Interpretação do Slicer:** O arquivo STL possui 20 × 20 × 20 unidades puras, mas não embute metadados de unidade física (limitação do padrão binário STL). A correta leitura como milímetros depende da configuração padrão do OrcaSlicer.
2. **Comportamento do Material FDM:** Fatores físicos reais (contração térmica do PLA, dilatação volumétrica e compensação de furos) requerem ensaio impresso na AD5X e não podem ser simulados apenas no Blender.
3. **Perspectiva 3Q:** A câmera `CAM_3Q` utiliza lente de 85 mm com enquadramento adaptativo; objetos com razões de aspecto extremas podem necessitar de ajuste manual de distância para enquadramento estético.

---

## 7. Itens que Necessitam Validação Humana

1. **Validação no OrcaSlicer:**
   - Importar `output/calibration/calibration_cube_20mm.stl` no OrcaSlicer com perfil da AD5X e confirmar se as dimensões informadas na barra de transformação são exatamente 20,0 × 20,0 × 20,0 mm.
2. **Avaliação Visual do Estúdio:**
   - Abrir `output/blender/runner_workspace_v001.blend` e verificar se a iluminação e as cores de fundo atendem ao conforto visual do modelador humano/supervisor.
