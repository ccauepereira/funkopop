# AGENTS.md — Runner Collectible 3D

## Project goal

Build a stylized multipart runner collectible for FDM 3D printing.

The project is based on:
- an older male reference;
- short white/gray hair;
- dark glasses;
- running pose;
- black Kichute-inspired shoes;
- stylized large-head collectible proportions.

The final asset must be reproducible, parametric where practical,
multipart, testable, and suitable for FDM printing.

---

## Source of truth

Before modifying anything, read:

1. docs/PROJECT_SPEC.md
2. docs/DECISIONS.md
3. docs/TASKS.md
4. relevant files under docs/research/

Do not contradict decisions marked CONGELADO.

If a requested task conflicts with a frozen decision:
STOP and report the conflict.

---

## AI / modeling restrictions

DO NOT use:
- Meshy
- Tripo
- Rodin
- Hunyuan 3D
- external automatic mesh-generation AI

Allowed:
- Blender
- Python
- bpy
- NumPy
- OpenCV
- procedural geometry
- traditional mesh operations

---

## Agent responsibilities

Codex:
- writes and refactors code;
- implements bpy tools;
- creates tests;
- modifies source files.

AGY / Antigravity:
- executes commands;
- runs Blender;
- runs tests;
- produces renders;
- produces logs;
- inspects outputs.

Do not let multiple agents independently redesign the same module.

---

## Git safety

NEVER:
- force push;
- rewrite git history;
- delete branches;
- commit directly to main unless explicitly requested;
- run `git reset --hard`;
- run `git clean -fd`;
- delete large groups of files;
- overwrite approved artifacts.

Use feature branches.

Branch naming examples:

feature/blender-smoke-test
feature/blockout-v001
feature/connectors
feature/kichute

Before changing files:
- inspect `git status`;
- inspect the task;
- identify files to modify.

After changing files:
- show `git diff`;
- run tests;
- report changed files.

---

## File protection

Never overwrite:

references/
docs/DECISIONS.md
approved renders
approved .blend files
prototype measurement data

Create new versions instead.

Examples:

runner_v001.blend
runner_v002.blend

renders/v001/
renders/v002/

Never replace an older version silently.

---

## Blender rules

Never manually edit binary .blend contents.

Modify Blender scenes through:
- bpy scripts;
- Blender UI only when explicitly requested.

All generated objects must use stable names.

Examples:

HEAD
HAIR
GLASSES
TORSO
ARM_L
ARM_R
SHORTS
LEG_L
LEG_R
KICHUTE_L
KICHUTE_R
BASE

Do not use names such as:
Cube.001
Cube.002
Sphere.014

for final project objects.

---

## Python environments

This project has two distinct Python environments.

### Project environment

Use `.venv` for:
- tests;
- data processing;
- OpenCV;
- NumPy;
- utility scripts.

Create with:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

### Blender environment

Scripts importing `bpy` must be executed using Blender's Python:

blender --background --python <script>

Do not assume packages installed in `.venv`
are available inside Blender.

Do not install or upgrade packages globally without explicit approval.

Do not add `bpy` to requirements.txt unless the project explicitly
decides to support standalone bpy execution.

---

## Units

Blender project units must represent millimeters consistently.

Do not invent physical dimensions.

Dimensions must come from:
- GEOMETRIC_SPEC.md;
- character.json;
- approved engineering tests.

---

## Geometry rules

Do not model the complete character in a single script.

Keep modules independent.

Do not apply destructive operations prematurely.

Preserve editable source geometry when practical.

Prefer:
- modifiers;
- parameters;
- reusable functions;
- deterministic scripts.

---

## Connectors

Do not invent connector clearances.

Connector tolerances remain experimental until physical testing.

Do not hardcode unexplained values.

Connector parameters must be centralized.

Every connector must document:
- type;
- nominal dimensions;
- clearance definition;
- chamfer;
- fillet;
- mating parts.

---

## 3D printing safety

Do not assume:
- minimum wall thickness;
- overhang angle;
- connector clearance;
- layer height;
- support settings.

Use research or physical test results.

Do not generate final production G-code manually.

G-code must be produced through an approved slicer profile.

---

## G-code

Do not edit printer G-code manually unless explicitly approved.

Never copy start/end G-code from another printer.

AD5X-specific commands must come from verified documentation or
an exported official slicer profile.

---

## Testing

Every new geometry system must have a small test before being used
on the character.

Examples:
- connector coupon;
- glasses thickness test;
- hair detail test;
- shoe relief test.

The full character must not be used as the first test.

---

## Rendering

Every meaningful geometry version must generate:

front.png
left.png
right.png
back.png
three_quarter.png

Save into:

renders/vXXX/

Never overwrite another render version.

---

## Definition of done

A task is complete only when:

1. requested code exists;
2. Blender runs without fatal error;
3. expected artifacts exist;
4. tests pass;
5. output is saved under a new version;
6. git diff is reviewed;
7. no frozen decision was violated;
8. agent provides a summary of:
   - files changed;
   - commands run;
   - tests run;
   - outputs produced;
   - known limitations.

---

## Stop conditions

STOP and ask/report instead of guessing when:

- reference information is missing;
- a frozen decision conflicts with the task;
- a destructive operation would be required;
- the agent would need to overwrite an approved asset;
- a physical dimension is undefined;
- printer behavior is not confirmed;
- a command would affect files outside this repository.