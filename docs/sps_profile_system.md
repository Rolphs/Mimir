# SPS Profile System

The Symbolic Profile System (SPS) defines a set of symbolic fields that drive interface adaptation.

## Profile Fields

- `cromotipo` – color archetype of the user or agent.
- `ritmo_cognitivo` – preferred cognitive tempo (slow, medium, fast).
- `arquetipo_narrativo` – narrative archetype used for icons and motifs.
- `estilo_perceptual` – perceptual style influencing animations.

## Example

```json
{
  "cromotipo": "sol",
  "ritmo_cognitivo": "medio",
  "arquetipo_narrativo": "explorador",
  "estilo_perceptual": "visual"
}
```

The engine maps these symbolic values to design variables (colors, fonts, icons, animations) which are then translated into CSS or React code snippets.
