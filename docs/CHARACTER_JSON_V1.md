# T-014 — Character JSON V1 (template conceitual)

## Propósito e limite

Este documento é o contrato conceitual de módulos aprovado em revisão humana
para o Character JSON V1. Não é um JSON físico de fabricação. A aprovação
libera T-015 para o blockout em unidades relativas, sem decisões físicas finais.

```json
{
  "schema_version": "v1",
  "status": "APPROVED_CONCEPTUAL_CONTRACT",
  "asset": {
    "id": "runner_collectible_3d",
    "type": "stylized_collectible",
    "character_role": "mature_runner"
  },
  "visual_identity": {
    "hair": "short_white_gray_large_masses",
    "glasses": "dark_thick_frame",
    "proportions": "dominant_head_compact_body",
    "pose": "dynamic_running_pose"
  },
  "apparel": {
    "top": "plain_dark_tank_top_provisional",
    "bottom": "plain_dark_shorts_provisional",
    "footwear": {
      "role": "priority_visual_signature",
      "description": "black_low_profile_rounded_toe_segmented_thick_sole",
      "upper": "simple_legible_panels",
      "laces": "thick_simplified",
      "brand_policy": "original_no_logo_no_text_no_proprietary_copy"
    }
  },
  "future_module_names": [
    "HAIR",
    "HEAD",
    "GLASSES",
    "TORSO",
    "ARM_L",
    "ARM_R",
    "SHORTS",
    "LEG_L",
    "LEG_R",
    "KICHUTE_L",
    "KICHUTE_R",
    "BASE"
  ],
  "reference_governance": {
    "concept_art_v1": "approved_external_reference",
    "turnaround_v1": "approved_external_reference",
    "external_images_versioned_in_git": false
  }
}
```

## Exclusões intencionais

O template exclui intencionalmente dimensões, espessuras, tolerâncias,
conectores, encaixes, geometria, Blender, orientação de impressão e dados de
fabricação. As imagens de Concept Art V1 e Turnaround V1 continuam como
referências externas aprovadas, não versionadas no Git.

## Governança visual e próxima etapa

O calçado preto inspirado no Kichute é uma prioridade visual, mas isso não
autoriza reproduzir marca, logotipo, texto ou desenho proprietário.

A aprovação humana de T-014 foi concedida. T-015 está pronta para iniciar;
nenhum Character JSON físico de fabricação é criado ou autorizado aqui.
