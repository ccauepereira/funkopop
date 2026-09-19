# T-016 — Visual QA V001

## Estado e escopo

CONCLUÍDA — aprovada em revisão humana. O relatório documenta a análise visual do Blockout V001, registrando que o modelo V001 não é aparência final e estabelecendo a lista de correções mandatórias para a evolução visual em T-017 (Refinamento V002).

Esta revisão documenta uma avaliação visual honesta e estruturada da primeira iteração tridimensional (Blockout V001), separando a base técnica já validada das correções anatômicas e estilísticas mandatórias para as próximas etapas.

---

## Aspectos aprovados no V001

O Blockout V001 cumpre com êxito seu papel de fundação de proporções iniciais e modularidade:

1. **Leitura imediata de corredor:** A atitude corporal transmite claramente a atividade esportiva de corrida sem ambiguidade.
2. **Pose dinâmica inicial:** A postura dinâmica — com tronco levemente projetado à frente, braço anterior flexionado, braço posterior em impulsão e pernas em passadas alternadas apoiadas sobre a base — funciona como ponto de partida sólido.
3. **Óculos grandes e escuros como traço visual forte:** O módulo `GLASSES` estabelece a identidade principal do personagem com armação grossa, ponte central e hastes laterais bem definidas.
4. **Linguagem de collectible (cabeça dominante / corpo compacto):** A relação volumétrica geral respeita o arquétipo estilizado com cabeça pronunciada, tronco curto, bermuda e base de sustentação integrada.
5. **Arquitetura modular e automação reproduzível:** Os 12 módulos canônicos (`BASE`, `TORSO`, `HEAD`, `HAIR`, `GLASSES`, `ARM_L`, `ARM_R`, `SHORTS`, `LEG_L`, `LEG_R`, `KICHUTE_L`, `KICHUTE_R`) estão perfeitamente isolados em coleções estáveis e gerados via script procedural determinístico.

---

## Correções obrigatórias antes de qualquer aprovação visual final

O modelo atual é estritamente um *blockout* preliminar de primitivas e não possui acabamento de escultura ou collectible final. As seguintes deficiências devem ser corrigidas nas próximas iterações:

1. **Cabelo (mechas vs. esferas):** O módulo `HAIR` atual apresenta uma leitura fragmentada de "bolinhas" ou esferas justapostas. Deve evoluir para massas volumétricas grandes, direcionadas e com sobreposição limpa, expressando o penteado curto grisalho sem fios finos ou aspecto granular.
2. **Tratamento facial e expressão:** O rosto atual éExcessivamente rígido e esquemático. Deve ganhar uma leitura escultórica mais limpa, simpática, orgânica e amigável, preservando a maturidade do corredor.
3. **Membros (continuidade anatômica):** Braços (`ARM_L`/`ARM_R`) e pernas (`LEG_L`/`LEG_R`) parecem atualmente cadeias de esferas e cilindros desconectados. Devem transicionar para volumes contínuos, suaves e com transições anatômicas fluidas entre ombro, braço, antebraço e mãos simplificadas.
4. **Aproximação do Turnaround V1:** A silhueta geral da cabeça e do tronco deve convergir fielmente para o estilo consolidado e aprovado na prancha de Turnaround V1, suavizando cantos facetados e quinas duras de primitivas puras.
5. **Prioridade do calçado inspirado no Kichute:** O módulo do calçado (`KICHUTE_L`/`KICHUTE_R`) necessita de refinamento prioritário de design:
   - Perfil baixo característico;
   - Biqueira arredondada robusta;
   - Sola grossa, robusta e segmentada;
   - Painéis de cabedal simples, legíveis e limpos;
   - Cadarços grossos e simplificados;
   - Rigorosa ausência de qualquer marca, logotipo ou cópia proprietária (respeito a D-015).
6. **Diretrizes para manufatura FDM:** Qualquer refinamento visual futuro deve respeitar a printabilidade em FDM na Flashforge AD5X (bico 0,4 mm), mantendo paredes consistentes e eliminando microdetalhes frágeis ou geometrias flutuantes.

---

## Limites desta análise

- **Sem nova geometria:** A tarefa T-016 é estritamente documental e analítica; não cria, exporta ou modifica qualquer malha ou cena 3D.
- **Sem aprovação de fabricação:** Não autoriza nem aprova dimensões finais, escalas de impressão, tolerâncias, conectores, arquivos STL, 3MF ou G-code.
- **Ambiente de color management:** Conforme registrado no smoke test e no relatório T-015, o Blender do ambiente opera com fallback padrão de gerenciamento de cor (sem perfil Filmic e sem OpenColorIO). Portanto, a imagem renderizada não serve como validação de iluminação final, shading ou fidelidade de materiais.
- **Integridade do repositório:** Nenhuma imagem de referência externa foi copiada ou versionada no Git.

---

## Decisão final

**APROVADA**

Aprovação humana concedida pelo Work para o relatório de QA Visual do Blockout V001:
- O Blockout V001 **não é aprovado como aparência final**;
- Aprovado como diagnóstico e base técnica de correções;
- O alvo visual continua sendo o collectible estilizado de cabeça grande definido pelo Turnaround V1 aprovado, sem copiar marcas comerciais;
- A tarefa T-017 (Refinamento V002) está liberada para execução com base nas correções registradas neste documento.

