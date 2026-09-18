# T-015 — Blockout V001

## Estado e escopo

APROVADA — aprovado em revisão humana como Blockout V001 (base técnica de automação, módulos, proporção inicial e pose; não como aparência final).
Execução em 2026-09-18, após publicação de T-014 no commit
`d53721b50b2b95355426d16f5c8193214e00bf54`.

Este é um blockout visual em unidades relativas (`unit_settings.system = NONE`).
Coordenadas, escalas e raios do script são escolhas artísticas provisórias de
cena; não representam dimensões físicas, espessuras ou parâmetros aprovados.
A autorização desta tarefa permite um gerador com funções independentes por
módulo e apenas um render de evidência, sem turnaround.

## Arquivos

- `scripts/build_blockout_v001.py`: gerador determinístico de primitivas editáveis.
- `output/blender/runner_blockout_v001.blend`: cena real do blockout.
- `renders/runner_blockout_v001.png`: evidência interna produzida pelo Cycles.
- `docs/T015_BLOCKOUT_V001.md`: este relatório.
- `docs/TASKS.md`: T-015 concluída; T-016 pronta para iniciar.

Os arquivos de T-015 permanecem sem commit/push até validação independente.
Nenhuma referência externa foi copiada ou incorporada.

## Organização e leitura visual

Cada módulo tem coleção própria e objeto principal com o mesmo nome.
Componentes adicionais usam prefixos estáveis e permanecem editáveis.

| Módulo | Componentes de malha |
|---|---|
| BASE | 1 |
| TORSO | 5 |
| HEAD | 10 |
| HAIR | 11 |
| GLASSES | 7 |
| ARM_L | 4 |
| ARM_R | 4 |
| SHORTS | 3 |
| LEG_L | 3 |
| LEG_R | 3 |
| KICHUTE_L | 16 |
| KICHUTE_R | 16 |

São 12 módulos, não 11: a contagem acompanha todos os nomes do pedido.
A cena contém também câmera e três luzes com prefixo `EVIDENCE_`.

Cabeça dominante, corpo compacto, pele clara, cabelo branco/grisalho em massas,
óculos escuros grossos, regata e shorts escuros, mãos simplificadas e pose de
corrida compõem a leitura inicial. Os tênis separados têm perfil baixo,
biqueira arredondada, painéis simples, sola segmentada e cadarços grossos.
Não há texto, marca ou logotipo no personagem.

As primitivas fechadas se sobrepõem intencionalmente: não constituem uma malha
unificada nem uma prova de fabricação, montagem, resistência ou estabilidade.

## Reprodução e proteção de versões

Ambiente utilizado: `/usr/bin/blender`, versão 3.0.1; Cycles CPU, semente fixa.
Em um checkout sem os dois artefatos de saída, executar da raiz:

```sh
blender --background --factory-startup --python-exit-code 1 --python scripts/build_blockout_v001.py
```

O script recusa sobrescrever arquivos existentes por padrão. Durante esta
execução, somente os rascunhos gerados aqui foram regenerados com o sufixo
`-- --replace-draft`. Essa opção não deve ser usada em ativos aprovados;
iterações posteriores aprovadas devem receber outra versão.

## Evidências e códigos de saída

- `git push origin main`: código 0; publicou somente a conclusão de T-014.
- `git status --short --branch` e `git rev-parse HEAD origin/main`: código 0;
  worktree limpo e hashes iguais antes de iniciar T-015.
- `blender --version`: código 0, Blender 3.0.1.
- Geração inicial: código 0, mas PNG preto; não foi aceito como evidência visual.
- Diagnóstico com leitura de pixels de EXR simples: código 1 ao detectar imagem
  zerada. O arquivo temporário foi removido automaticamente.
- Diagnósticos efêmeros com render reduzido: código 0; o passe `Combined`
  estava zerado com denoising, enquanto `Noisy Image` continha valores válidos.
  Desativar denoising produziu um PNG com pixels não zerados.
- Gerador final com `-- --replace-draft`: código 0;
  `BLOCKOUT_V001_OK 3.0.1 modules 12`.
- Reabertura background com `--python-exit-code 1 --python-expr`: código 0;
  verificou coleções, objetos principais, unidades relativas, denoising
  desativado, ausência de nomes de fabricação/conectores e primitivas fechadas.
  Marcadores: `CLOSED_PRIMITIVES_OK` e `BLOCKOUT_OPEN_OK`. Não salvou a cena.
- `git diff --check`: código 0.
- Busca por STL, 3MF, OBJ, FBX, G-code e JSON: nenhum arquivo encontrado.

Para inspeção independente mínima, sem salvar ou regenerar:

```sh
blender --background output/blender/runner_blockout_v001.blend --python-exit-code 1 --python-expr "import bpy; names='BASE TORSO HEAD HAIR GLASSES ARM_L ARM_R SHORTS LEG_L LEG_R KICHUTE_L KICHUTE_R'.split(); print(bpy.app.version_string); print([(n,len(bpy.data.collections[n].objects)) for n in names]); assert all(n in bpy.data.objects for n in names); print('BLOCKOUT_OPEN_OK')"
```

## Limitações e pendências para T-016

- O Blender disponível foi compilado sem OpenColorIO. Persistem mensagens de
  fallback e ausência de Filmic. Uma tentativa temporária de configuração OCIO
  não resolveu o problema e foi removida do gerador; nenhuma instalação mudou.
- A saída preta foi isolada no denoising: ele está explicitamente desativado.
  O render direto do Cycles tem ruído e não comprova qualidade visual final,
  fidelidade de cor ou comportamento em outra versão do Blender.
- Avisos de áudio e de gravação da miniatura no cache não impediram a gravação
  do `.blend` e do PNG. Avisos iniciais de normais foram corrigidos no gerador.
- AGY deve validar os arquivos; a revisão humana deve avaliar a fidelidade ao
  Concept/Turnaround, maturidade facial, massas de cabelo, pose e calçado.
- T-016 pronta para iniciar após aprovação de T-015; não foi iniciado turnaround.
- Não há conectores, encaixes, tolerâncias finais, linhas de corte, parâmetros
  de fabricação, exportações de malha ou `character.json` físico.

## Aprovação humana de T-015

- Decisão: **APROVADA** somente como Blockout V001.
- O modelo V001 foi aprovado como base técnica de automação, módulos, proporção inicial e pose, mas **não como aparência final**.
- O alvo visual continua sendo o collectible estilizado de cabeça grande definido pelo Turnaround V1 aprovado, sem copiar marcas comerciais.
- T-016 está pronta para iniciar com a análise visual do V001.
