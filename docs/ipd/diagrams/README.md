# IPD Diagrams

Mermaid diagram files for the CrackInt IPD report. Export to PNG or SVG for the thesis and presentation.

---

## Diagram List

| File | Diagram | Chapter | Section |
|------|---------|---------|---------|
| `01-stakeholder-onion.mmd` | Stakeholder Onion Diagram | 4 | 4.3.1 |
| `02-system-architecture-high-level.mmd` | System Architecture (Target) | 6 | 6.3.1 |
| `03-prototype-component.mmd` | Current Prototype Component Diagram | 6 | 6.3.2 |
| `04-class-diagram.mmd` | Class Diagram (Backend) | 6 | 6.4 |
| `05-sequence-resume-extract.mmd` | Sequence: Resume Extract | 6 | 6.4 |
| `06-sequence-job-extract.mmd` | Sequence: Job Extract | 6 | 6.4 |
| `07-sequence-session-flow.mmd` | Sequence: Session / Chat Flow | 6 | 6.4 |
| `08-activity-main-user-flow.mmd` | Activity: Main User Flows | 6 | 6.4 |
| `09-bilstm-crf-architecture.mmd` | BiLSTM-CRF Neural Network | 6 | 6.5 |
| `10-ui-wireframes-spec.md` | UI Wireframe Specifications | 6 | 6.6 |
| `11-concept-map.mmd` | Concept Map (Literature Review) | 2 | 2.2 |

---

## Concept Map Export Tip

For `11-concept-map.mmd`, use **Theme: Default** in mermaid.live (not Sketch) for clean, professional lines suitable for the thesis.

---

## How to Export to PNG/SVG

### Option 1: Mermaid Live Editor (Recommended)

1. Go to [mermaid.live](https://mermaid.live)
2. Copy the contents of a `.mmd` file
3. Paste into the left panel
4. Use **Actions → PNG** or **Actions → SVG** to download

### Option 2: VS Code

1. Install extension: **Mermaid Preview** or **Markdown Preview Mermaid Support**
2. Open a `.mmd` file
3. Right-click → "Export" or use preview and screenshot

### Option 3: Mermaid CLI (`mmdc`)

```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i 01-stakeholder-onion.mmd -o 01-stakeholder-onion.png
mmdc -i 01-stakeholder-onion.mmd -o 01-stakeholder-onion.svg
```

### Option 4: GitHub

Push the `.mmd` files to GitHub; Mermaid is rendered in `.md` files. Screenshot or use GitHub's export.

---

## Stakeholder Onion Diagram Note

The Mermaid file `01-stakeholder-onion.mmd` uses nested subgraphs (layered boxes). For a **true onion** (concentric circles), redraw in PowerPoint or draw.io:

- **Layer 1 (centre):** Job seekers, Students, Early-career professionals  
- **Layer 2:** Career services, Technical support, Development team  
- **Layer 3:** Academic institutions, Corporate partners, Research community  
- **Layer 4 (outer):** Regulatory bodies, AI ethics orgs, Competitors, Tech providers  

---

## UI Wireframes

`10-ui-wireframes-spec.md` contains ASCII layouts and element specs. Use them to:

- Draw wireframes in draw.io, Figma, or PowerPoint  
- Take screenshots of the running app as wireframe alternatives  
- Create low-fidelity mockups for the report  

Export wireframes as PNG for the thesis.
