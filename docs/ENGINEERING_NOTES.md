# Runner Collectible 3D — Engineering Notes V1

## Propósito

Este documento traduz as pesquisas existentes em limites de implementação. Ele não define geometria, tolerâncias ou parâmetros finais de impressão.

## Plataforma de experimentação

| Item | Estado |
|---|---|
| Processo | FDM |
| Impressora | Flashforge AD5X |
| Bico inicial | 0,4 mm |
| Material inicial | PLA |
| Escalas candidatas | 120 mm e 140 mm, não aprovadas |
| Slicer | Perfil compatível e registrado; escolha/versão pendentes |

## Regras de engenharia para a primeira implementação

1. O Blender deve usar unidades coerentes com milímetros, mas nenhuma dimensão pode ser criada antes da Geometric Spec V1.
2. O blockout deve manter módulos independentes: `HEAD`, `HAIR`, `GLASSES`, `TORSO`, `ARM_L`, `ARM_R`, `SHORTS`, `LEG_L`, `LEG_R`, `KICHUTE_L`, `KICHUTE_R`, `BASE`.
3. Cabelo, óculos, cadarços, mãos e sola devem ser representados por formas grandes e contínuas; o nível final de detalhe depende dos cupons físicos.
4. Nenhum conector, folga, parede mínima, overhang, camada, suporte ou orientação pode ser codificado como fato antes de teste.
5. A geometria deve ser reprodutível e editável: módulos, parâmetros documentados e nomes estáveis; não usar objetos finais com nomes automáticos.
6. O Kichute é inspiração de silhueta e leitura, não cópia de logo, texto, textura ou desenho proprietário.

## Plano de validação antes de decisões físicas

| Área | Evidência necessária |
|---|---|
| Dimensional | Chapa/cupom de furos, pinos e paredes com medições. |
| Conectores | Séries de ajustes e ensaio de montagem/torção, registrando folga radial ou diametral. |
| Óculos | Cartela de armações/hastes com teste de remoção e resistência. |
| Cabelo/cadarços | Relevos e volumes impressos para leitura e falhas. |
| Base | Ensaio de estabilidade e inclinação compatível com a pose. |
| Multicor | Medição de purga, tempo e qualidade antes de adotar estratégia final. |

## G-code e slicing

O G-code é saída do slicer e do perfil verificado para a AD5X. Não deve ser escrito, copiado de outra impressora ou alterado manualmente. Antes de qualquer impressão, registrar impressora, firmware, slicer, versão, perfil, filamento, bico, camada, orientação, suporte, tempo e resultado.

## Riscos abertos

- a pose de corrida pode exigir uma base mais estrutural do que a aparência inicial sugere;
- a escala final altera a viabilidade de cabelo, óculos, cadarços e conectores;
- a AD5X, PLA e o perfil real precisam de calibração para dados de ajuste;
- o Concept Art V1 não supre vistas de perfil/costas necessárias para a modelagem.
