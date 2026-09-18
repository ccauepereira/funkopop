# Runner Collectible 3D

Projeto de preparação para um personagem colecionável estilizado, multipartes e
reprodutível para impressão FDM na Flashforge AD5X. O conceito congelado é um
corredor maduro, com cabelo branco/grisalho curto, óculos escuros grossos,
cabeça grande, corpo compacto e tênis inspirados no Kichute preto.

Esta etapa é somente o bootstrap da estrutura do projeto. O primeiro teste real
no Blender será a tarefa T-011. Até lá, não há cena, geometria, personagem,
medidas, conectores ou arquivos de fabricação aprovados neste repositório.

## Estrutura

```text
src/                 fontes e módulos futuros do modelo
config/              configurações futuras
tests/               testes e cupons de validação futuros
scripts/             scripts auxiliares futuros
renders/             renders gerados
output/blender/      arquivos de trabalho e saídas do Blender
output/stl/          exportações STL
output/3mf/          exportações 3MF
references/          referências visuais existentes
docs/                especificações, decisões e notas do projeto
```

As pastas de saída são separadas por formato para manter os artefatos
reprodutíveis e rastreáveis. A escala candidata de 120 mm ou 140 mm ainda não
está aprovada; conectores dependem de testes físicos; o bico inicial é 0,4 mm,
com PLA inicial; e G-code nunca será escrito manualmente.

## Papéis

```text
Work → Codex → AGY → relatório para Work
```

- Work define a tarefa e os critérios de aceitação.
- Codex implementa e documenta as alterações autorizadas.
- AGY executa comandos, Blender, testes e gera os artefatos solicitados.
- O relatório retorna para Work com mudanças, comandos, validações, riscos e
  bloqueios.

## Próximo marco

T-011 será o primeiro teste real no Blender. Esta tarefa T-010 não cria script
`bpy`, cena, objeto, geometria, `character.json`, STL, 3MF ou G-code.
