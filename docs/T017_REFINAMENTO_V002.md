# T-017 — Refinamento V002

## Estado e escopo

EM VALIDAÇÃO — evolução visual do personagem (Refinamento V002) baseada nas correções mandatórias apontadas no relatório de QA Visual V001 (`docs/T016_VISUAL_QA_V001.md`).

Esta entrega preserva a arquitetura modular e os arquivos do Blockout V001 como histórico reproduzível, refinando as superfícies anatômicas, a estilização de collectible e os detalhes de vestuário e calçado.

---

## Arquivos criados na etapa

- `scripts/build_refinement_v002.py`: gerador determinístico procedural do Refinamento V002.
- `output/blender/runner_refinement_v002.blend`: cena binária do modelo refinado (3,7 MB).
- `renders/runner_refinement_v002_3q.png`: render de evidência em vista 3/4 frontal (Cycles, 900x1000).
- `renders/runner_refinement_v002_side.png`: render de evidência em vista lateral de perfil (Cycles, 900x1000).
- `docs/T017_REFINAMENTO_V002.md`: este relatório de validação.

---

## Ambiente de execução e versão

- **Versão do Blender:** `3.0.1` (`/usr/bin/blender`).
- **Engine de render:** Cycles CPU, 48 amostras, semente fixa (`seed = 0`), `use_denoising = False`.
- **Unidades:** Relativas de cena (`unit_settings.system = NONE`).

### Avisos do ambiente (não bloqueantes)
Durante a execução, o ambiente emitiu mensagens conhecidas de fallback de gerenciamento de cores:
```text
Color management: using fallback mode for management
Color management: Error could not find role data role.
Color management: scene view "Filmic" not found, setting default "Standard".
```
Esses avisos decorrem da compilação do Blender do sistema operacional sem OpenColorIO e foram contornados com a renderização direta em modo Standard sem denoising, produzindo saídas PNG válidas e contrastadas.

---

## Diferenças visuais e evoluções em relação ao V001

1. **Cabeça e proporções:** A cabeça foi redefinida com crânio mais largo, dominante e arredondado (`1.10 x 0.88 x 1.00`), acentuando a linguagem de collectible estilizado aprovada no Turnaround V1.
2. **Cabelo (eliminação do aspecto de esferas):** A antiga cadeia de bolinhas foi substituída por um conjunto esculpido de mechas largas e direcionadas (`HAIR_LOCK_CREST`, `HAIR_LOCK_SWEEP_L/R`, `HAIR_LOCK_CROWN_L/R`, volumes laterais e posteriores), com transições suaves e sem fios finos.
3. **Expressão facial escultórica:** O rosto ganhou bochechas mais suaves e integradas (`HEAD_CHEEK_L/R`), orelhas estilizadas compactas, nariz suavemente arredondado e um sorriso amplo e amigável (`HEAD_SMILE`).
4. **Membros contínuos e anatômicos:** Braços (`ARM_L`/`ARM_R`) e pernas (`LEG_L`/`LEG_R`) deixaram de usar articulações esféricas aparentes, adotando volumes contínuos, cônicos e suaves. As mãos foram modeladas como punhos/luvas estilizados compactos, sem dedos individuais frágeis.
5. **Calçado refinado (`KICHUTE_L` e `KICHUTE_R`):** A leitura visual do tênis foi aprimorada com perfil baixo robusto, biqueira arredondada clássica (`TOE`), sola grossa segmentada (`SOLE` e `TREAD`), painel de calcanhar limpo e cadarços grossos destacados (`LACES`). Nenhuma marca, logotipo ou cópia proprietária foi introduzida.
6. **Pose e estabilidade:** Mantida a dinâmica da corrida, com o pé esquerdo em apoio estável na base cilíndrica e o pé direito em impulsão traseira.

---

## Comandos executados e códigos de saída

1. **Geração do modelo e renders:**
   ```sh
   blender --background --factory-startup --python scripts/build_refinement_v002.py
   ```
   - Código de saída: `0`.
   - Saídas geradas: `RENDER_3Q_OK`, `RENDER_SIDE_OK`, `REFINEMENT_V002_OK 3.0.1 modules 12`.
2. **Inspeção independente dos 12 módulos em background:**
   ```sh
   blender --background output/blender/runner_refinement_v002.blend --python-exit-code 1 --python-expr "..."
   ```
   - Código de saída: `0`.
   - Marcador: `REFINEMENT_V002_OPEN_OK`.
   - Módulos confirmados: `BASE`, `TORSO`, `HEAD`, `HAIR`, `GLASSES`, `ARM_L`, `ARM_R`, `SHORTS`, `LEG_L`, `LEG_R`, `KICHUTE_L`, `KICHUTE_R`.
3. **Verificação de formatação (`git diff --check`):** Código de saída `0`.

---

## Limites e conformidade

- **Sem aprovação de fabricação:** O Refinamento V002 é uma iteração de aparência visual e silhueta. Não define dimensões métricas finais, escalas de impressão, tolerâncias, folgas, espessuras de parede, conectores, encaixes ou linhas de corte para montagem.
- **Sem arquivos restritos:** Zero arquivos `.stl`, `.3mf`, `.obj`, `.fbx`, G-code ou `character.json`.
- **Integridade do histórico:** Todos os arquivos da versão V001 permanecem intocados e preservados no repositório.

---

## Decisão provisória

**EM VALIDAÇÃO**

A entrega técnica e visual do Refinamento V002 aguarda a revisão e direcionamento humano.

