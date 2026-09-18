# T-011 — Blender Smoke Test

## Registro

- Data/hora: 2026-09-18T15:38:10-03:00
- Commit testado: `db8595fb9c70d3900aa8d016c484ca5d9fd33c54`
- Caminho do Blender: `/usr/bin/blender`
- Versão do Blender: `3.0.1`

## Comandos e resultados

| Comando | Código de saída | Resultado |
|---|---:|---|
| `git status --short --branch` | 0 | `## main...origin/main` com alterações documentais não commitadas de T-011 |
| `git rev-parse HEAD` | 0 | `db8595fb9c70d3900aa8d016c484ca5d9fd33c54` |
| `command -v blender` | 0 | `/usr/bin/blender` |
| `blender --version` | 0 | `Blender 3.0.1` |
| `blender --background --factory-startup --python-expr "import bpy; print(bpy.app.version_string); print('BLENDER_SMOKE_OK')"` | 0 | importação `bpy` concluída; versão `3.0.1`; marcador emitido |

## Saída relevante do smoke test

```text
3.0.1
BLENDER_SMOKE_OK
Blender quit
```

## Alerta não bloqueante: color management

O processo emitiu avisos de fallback/erro de color management, incluindo a
ausência da visualização `Filmic` e a seleção do padrão `Standard`. Também houve
um aviso de áudio do ambiente. Esses avisos não impediram a importação de `bpy`,
a emissão de `BLENDER_SMOKE_OK` nem o encerramento com código 0.

Este smoke test não valida qualidade visual de renders futuros. O ambiente de
color management deverá ser verificado antes de qualquer validação visual de
render, sem correção, instalação ou atualização do Blender nesta tarefa.

## Resultado

- Importação `bpy`: aprovada.
- Marcador `BLENDER_SMOKE_OK`: emitido.
- Decisão: **APROVADA**.

## Conformidade de escopo

O teste usou `--background`, `--factory-startup` e `--python-expr`, sem salvar
cena, render, script persistente ou artefato 3D. Nenhuma geometria, dimensão,
tolerância, conector ou arquivo de fabricação foi criado. T-011 está concluída;
T-012 está pronta para início, mas não foi iniciada nesta tarefa.
