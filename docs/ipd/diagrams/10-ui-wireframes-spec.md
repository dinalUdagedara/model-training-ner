# UI Wireframes Specification (Low Fidelity)

**Chapter 6, Section 6.6**

Use this spec to create low-fidelity wireframes in draw.io, Figma, PowerPoint, or pen-and-paper. Screenshots from the running app can also serve as wireframes.

---

## Wireframe 1: CV Upload Page

**Route:** `/cv-upload`  
**Location:** `crackint-frontend/app/cv-upload/page.tsx`, `components/cv-upload/CVUploadView.tsx`

### Layout (ASCII)

```
┌─────────────────────────────────────────────────────────┐
│ [Sidebar]  │  CV Upload                                  │
│            │                                             │
│ - Home     │  ┌─────────────────────────────────────┐   │
│ - CV       │  │  [Upload PDF]  │  [Paste text]      │   │
│ - Job      │  └─────────────────────────────────────┘   │
│ - Sessions │                                             │
│            │  ┌─────────────────────────────────────┐   │
│            │  │  Drop zone OR Textarea               │   │
│            │  │  (PDF / PNG / JPEG / WebP)           │   │
│            │  └─────────────────────────────────────┘   │
│            │                                             │
│            │  [ Extract ]  (primary button)              │
│            │                                             │
└─────────────────────────────────────────────────────────┘
```

### Elements

| Element | Type | Description |
|---------|------|-------------|
| Tabs | Tabs | "Upload PDF" \| "Paste text" |
| Drop zone | File input / drag area | Accept PDF, PNG, JPEG, WebP; max 5MB |
| Textarea | Multi-line input | Raw resume text paste |
| Extract button | Primary button | Triggers extraction; shows loading state |

---

## Wireframe 2: Extracted Entities (Resume)

**Same page after extraction**

### Layout

```
┌─────────────────────────────────────────────────────────┐
│ [Sidebar]  │  Extracted Information                      │
│            │                                             │
│            │  ┌─────────────────────────────────────┐   │
│            │  │ NAME:     [John Doe]                 │   │
│            │  │ EMAIL:    [john@example.com]         │   │
│            │  │ SKILLS:   [Python, Java, SQL, ...]   │   │
│            │  │ OCCUPATION: [Software Engineer]      │   │
│            │  │ EDUCATION: [BSc CS, University of..] │   │
│            │  │ EXPERIENCE: [Virtusa, WSO2]          │   │
│            │  └─────────────────────────────────────┘   │
│            │                                             │
│            │  [ Edit ]  [ Replace resume ]               │
│            │                                             │
└─────────────────────────────────────────────────────────┘
```

### Elements

| Element | Type | Description |
|---------|------|-------------|
| Entity card | Card / list | Labelled groups (NAME, EMAIL, SKILL, etc.) |
| Edit button | Button | Opens Edit Entities modal |
| Replace resume | Button | Return to upload/paste |

---

## Wireframe 3: Edit Entities Modal

**Location:** `components/cv-upload/EditEntitiesDialog.tsx`

### Layout

```
┌─────────────────────────────────────────────────────────┐
│  Edit Extracted Information                    [X]      │
├─────────────────────────────────────────────────────────┤
│  NAME:     [________________________]  [+] [-]          │
│  EMAIL:    [________________________]  [+] [-]          │
│  SKILLS:   [Python] [Java] [SQL] ...  [+] [-]          │
│  OCCUPATION: [Software Engineer]       [+] [-]          │
│  EDUCATION: [BSc CS] [University of Colombo]  [+] [-]   │
│  EXPERIENCE: [Virtusa] [WSO2]         [+] [-]          │
│                                                         │
│                    [ Cancel ]  [ Save ]                  │
└─────────────────────────────────────────────────────────┘
```

### Elements

| Element | Type | Description |
|---------|------|-------------|
| Modal | Dialog | Overlay; editable inputs per entity type |
| Add/Remove | Buttons | For multi-value entities (e.g. SKILL) |
| Save | Button | PATCH /api/v1/resumes/{id} |
| Cancel | Button | Close without saving |

---

## Wireframe 4: Job Description Page

**Route:** `/job-upload`  
**Location:** `components/job-upload/JobUploadView.tsx`

### Layout

```
┌─────────────────────────────────────────────────────────┐
│ [Sidebar]  │  Job Description                            │
│            │                                             │
│            │  ┌─────────────────────────────────────┐   │
│            │  │  Paste job description text          │   │
│            │  │  (or upload PDF)                     │   │
│            │  │  _____________________________       │   │
│            │  └─────────────────────────────────────┘   │
│            │                                             │
│            │  [ Extract ]                                │
│            │                                             │
│            │  ┌─────────────────────────────────────┐   │
│            │  │ Skills: [Python, AWS, ...]           │   │
│            │  │ Experience: [3+ years]               │   │
│            │  │ Education: [BSc required]            │   │
│            │  └─────────────────────────────────────┘   │
│            │                                             │
└─────────────────────────────────────────────────────────┘
```

---

## Wireframe 5: Sessions / Chat (Placeholder)

**Route:** `/sessions`, `/sessions/[id]`  
**Location:** `components/sessions/SessionChatView.tsx`  
**Note:** Chat UI exists; LLM question generation and semantic feedback pending.

### Layout

```
┌─────────────────────────────────────────────────────────┐
│ [Sidebar]  │  Practice Session                           │
│            │                                             │
│            │  ┌─────────────────────────────────────┐   │
│            │  │ ASSISTANT: Tell me about your        │   │
│            │  │ experience with Python projects.     │   │
│            │  └─────────────────────────────────────┘   │
│            │                                             │
│            │  ┌─────────────────────────────────────┐   │
│            │  │ USER: I worked on a data pipeline... │   │
│            │  └─────────────────────────────────────┘   │
│            │                                             │
│            │  ┌─────────────────────────────────────┐   │
│            │  │ Your answer:                         │   │
│            │  │ [_____________________________]      │   │
│            │  │ [ Submit ]                           │   │
│            │  └─────────────────────────────────────┘   │
│            │                                             │
└─────────────────────────────────────────────────────────┘
```

---

## How to Create Wireframes

1. **draw.io / diagrams.net:** Use Rectangle, Text, Button shapes; group by screen.
2. **Figma:** Create frames per screen; use gray boxes for placeholders.
3. **PowerPoint / Google Slides:** Insert shapes and text boxes.
4. **Screenshots:** Capture actual app screens as low-fidelity alternatives.
5. **Pen and paper:** Sketch boxes and labels; photograph for report.

---

## Export for Report

- Export as PNG or PDF at ~1200px width for print clarity.
- Add figure numbers and captions when inserting into thesis.
- Example caption: *"Figure X: Low-fidelity wireframe – CV Upload page"*.
