# Runner Collectible 3D — Geometric Spec V1

## Escopo e não-escopo

Esta especificação orienta conceitualmente as próximas etapas de parâmetros e
blockout do personagem colecionável multipartes. A fabricação-alvo continua
sendo FDM na Flashforge AD5X, com bico inicial de 0,4 mm e PLA inicial.

A especificação conceitual V1 foi aprovada em revisão humana. Essa aprovação
não transforma hipóteses de fabricação em valores ou decisões finais.

As escalas de 120 mm e 140 mm são apenas candidatas e permanecem não aprovadas.
Este documento não define dimensões finais, espessuras finais, tolerâncias
finais, conectores finais, orientação de impressão, perfil de slicer ou G-code.
Também não contém desenho, malha, cena ou instrução de modelagem executável.

## Inventário de módulos futuros

Os módulos abaixo são uma organização futura do ativo. A listagem não define
encaixes, superfícies de contato ou geometria final.

| Módulo futuro | Papel conceitual |
|---|---|
| `HAIR` | Cabelo curto branco/grisalho em grandes massas. |
| `HEAD` | Cabeça dominante e leitura facial estilizada. |
| `GLASSES` | Óculos escuros de armação grossa. |
| `TORSO` | Tronco compacto com regata provisória. |
| `ARM_L` e `ARM_R` | Braços da pose de corrida. |
| `SHORTS` | Shorts escuros provisórios. |
| `LEG_L` e `LEG_R` | Pernas na pose dinâmica de corrida. |
| `KICHUTE_L` e `KICHUTE_R` | Módulos separados de tênis pretos inspirados no Kichute, sem marca ou logotipo. |
| `BASE` | Apoio estrutural discreto para a pose. |

## Regras qualitativas de proporção e leitura

- Manter a cabeça visualmente dominante e o corpo compacto.
- Representar o cabelo por massas grandes e conectadas, sem fios ou
  microtextura.
- Preservar a leitura central dos óculos escuros com armação grossa.
- Manter mãos simplificadas, sem dedos individuais frágeis.
- Tratar os tênis como volumes grossos e simplificados, sem reprodução de marca.
- Preservar a pose dinâmica de corrida aprovada no Turnaround V1.
- Evitar espessuras visualmente frágeis, microdetalhe, microtextura, fios e
  elementos flutuantes.

Essas regras são qualitativas. Nenhuma razão numérica de proporção, dimensão ou
espessura é aprovada nesta versão.

## Diretrizes futuras para `KICHUTE_L` e `KICHUTE_R`

`KICHUTE_L` e `KICHUTE_R` permanecem módulos separados. A geometria futura deve
permitir impressão e montagem sem costuras visuais excessivas, priorizando áreas
limpas de alinhamento e colagem. Essas diretrizes não descrevem superfícies,
encaixes, valores ou geometria final.

O tênis preto inspirado no Kichute é prioridade visual, sem marca, logotipo ou
reprodução proprietária. Essa prioridade não aprova geometria final do calçado.

Conectores continuam não definidos e dependem de testes físicos. Nenhuma área de
alinhamento ou colagem constitui conector aprovado nesta fase.

## Modelo paramétrico de conectores — hipóteses para teste físico

Nenhum dos modelos abaixo seleciona um conector para o personagem. Eles existem
somente como hipóteses a serem avaliadas com cupons físicos na AD5X, considerando
material, orientação e acabamento.

### Folga

`D_fêmea = D_macho + C_efetiva`

`C_efetiva` é uma variável experimental. Ela deverá ser determinada por cupons
físicos que representem a Flashforge AD5X, o material, a orientação de impressão
e o acabamento aplicáveis. Esta fórmula não atribui valor a nenhuma variável.

### Pinos / dowels

A razão `H/D` é uma variável de estudo para pinos. A faixa `2D ≤ H ≤ 4D` é uma
hipótese de pesquisa, não uma regra aprovada. A seleção de diâmetro, altura,
folga, chanfro, filete ou material de acoplamento permanece pendente de teste.

### Snap-fit

Uma eventual deflexão depende do comprimento do braço, espessura, módulo do
material, deformação admissível e orientação das camadas. Snap-fit não está
selecionado para PLA nesta fase.

### Dovetail

Ângulo e proporções de um eventual dovetail são variáveis de estudo. A faixa de
`8°–15°` é hipótese de pesquisa, não decisão. Dovetail não está escolhido como
conector final.

## Plano de validação futura

Antes de qualquer decisão de escala ou conector, a sequência futura deve incluir:

1. teste de folga;
2. teste de pinos;
3. teste de retenção;
4. teste de orientação de impressão;
5. teste de força manual;
6. inspeção visual.

Esta tarefa não cria cupom, medida, perfil de slicer, G-code ou artefato físico.
Cada ensaio futuro deverá registrar as condições e resultados exigidos pela
pesquisa do projeto antes de transformar hipótese em decisão.

## Resultado da revisão e pendências

- Especificação conceitual V1 aprovada em revisão humana.
- T-014 está liberada para início, mas não foi iniciada nesta tarefa.
- Escala, dimensões, espessuras, tolerâncias e conectores continuam pendentes.
- Nenhuma hipótese de conector deste documento constitui decisão final.
