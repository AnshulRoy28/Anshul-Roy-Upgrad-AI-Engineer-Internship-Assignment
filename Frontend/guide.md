# Interview AI — Build Guide

## File Structure

```
├── styles.css          ← shared styles (already created)
├── index.html          ← landing page (static)
├── interview.html      ← interview page (3 states)
└── app.js              ← interview logic & API calls
```

---

## Shared Head Block (use in both pages)

```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interview AI — ...</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://code.iconify.design/iconify-icon/1.0.7/iconify-icon.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
</head>
```

## Shared Background (use in both pages, right after `<body>`)

Copy from template lines 174-190 (the background glow effects div). Remove the UnicornStudio div (lines 154-163) — it's a third-party dependency we don't need.

---

## Page 1: Landing Page (`index.html`)

**Purpose**: Static marketing page. No JS logic needed. Links to `interview.html`.

### Section 1: Navigation Header
- **Reuse**: Template lines 193-252
- **Changes**:
  - Logo text: "Lumina" → "Interview AI"  
  - Icon: keep `solar:play-bold` or change to `solar:chat-round-dots-bold`
  - Nav links: `Product` → `Features`, `Resources` → `How It Works`, `Pricing` → remove
  - Login button → remove
  - CTA button text: "Start Today It's Free" → "Start Practicing"
  - CTA `href` → `interview.html`

### Section 2: Hero
- **Reuse**: Template lines 253-398
- **Left side changes** (lines 260-330):
  - H1: Replace with:
    ```
    Ace Your Next
    Interview With
    <span class="text-zinc-500">AI Coaching</span>
    ```
  - CTA buttons:
    - Primary: "Start Practicing" → links to `interview.html`
    - Secondary: "Learn More" → scrolls to features
  - Feature list bullets:
    - "**Adaptive AI** : adjusts to your skill level"
    - "**Real-time Scoring** : instant 5-dimension feedback"
    - "**Personalized Reports** : actionable practice plans"
- **Right side** (lines 332-397):
  - Option A: Keep the floating image cluster as-is (decorative)
  - Option B: Replace images with screenshots of the interview UI (if you have them later)
  - The Supabase image URLs should still work, they're just decorative

### Section 3: Feature Cards
- **Reuse**: Template lines 404-917 (the 6-card grid)
- **Replace card content** (keep all the animated inner graphics, just change text):

| Card # | Original Title | New Title | New Description | Inner Graphic |
|--------|---------------|-----------|-----------------|---------------|
| 1 | SOC 2 Compliance | Real-Time Evaluation | Get scored on completeness, depth, structure, relevance & confidence | Keep the audit dashboard graphic — change labels to score names |
| 2 | SSO and Domain Capture | Smart Question Engine | AI generates contextual questions from your resume and job description | Keep login routing graphic — change labels to "Parsing Resume" → "Generating Questions" |
| 3 | Fine-Grained Permissions | Multi-Focus Interviews | Choose behavioral, technical, case study, or mixed interview styles | Keep permissions matrix — change column headers to focus areas |
| 4 | Role-Based Access Control | Adaptive Difficulty | AI adjusts question difficulty based on your performance in real-time | Keep the role assignment graphic — change role tags to "Easy", "Medium", "Hard" |
| 5 | Workspaces Per Org | Outcome Prediction | Get early pass/fail predictions after just 3 questions | Keep workspace switcher — change items to prediction outcomes |
| 6 | On-Premise Deployment | Coaching Reports | Comprehensive practice plans with skill gap analysis and weekly schedules | Keep terminal graphic — change commands to report generation |

### Section 4: How It Works (replace Dashboard Preview section)
- **Reuse**: Template lines 919-1377 (the dashboard section)
- **Simpler alternative**: Replace the entire dashboard with a 3-step visual:

```html
<section class="...container...">
    <h2>How It Works</h2>
    <p>Three simple steps to interview mastery</p>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- Step 1 -->
        <div class="panel p-8 text-center">
            <div class="w-16 h-16 rounded-2xl bg-white/5 border border-white/10 
                 flex items-center justify-center mx-auto mb-6">
                <iconify-icon icon="solar:document-text-linear" class="w-8 h-8 text-zinc-300"/>
            </div>
            <h3 class="text-xl font-medium text-white mb-2 font-geist">1. Upload</h3>
            <p class="text-zinc-400">Paste your resume (LaTeX) and the job description you're targeting</p>
        </div>
        
        <!-- Step 2: icon solar:chat-round-dots-linear -->
        <h3>2. Practice</h3>
        <p>Answer AI-generated questions tailored to your background and the role</p>
        
        <!-- Step 3: icon solar:chart-2-linear -->
        <h3>3. Improve</h3>
        <p>Get a personalized coaching report with practice plans and skill gap analysis</p>
    </div>
</section>
```

### Section 5: CTA Footer (replace Pricing section)
- **Reuse**: Template lines 1379-1606 (pricing section)
- **Replace with** a simple call-to-action:

```html
<section class="...container... text-center py-32">
    <h2 class="text-3xl md:text-5xl font-medium tracking-tight mb-4 font-geist text-white">
        Ready to ace your interview?
    </h2>
    <p class="text-lg text-zinc-400 mb-8 max-w-2xl mx-auto">
        Free to use. Powered by Google Gemini. Start practicing now.
    </p>
    <!-- Reuse the animated CTA button from the hero, linking to interview.html -->
</section>
```

### Remove from template:
- Google Analytics script (lines 126-133)
- UnicornStudio background (lines 154-162)
- All `aura-*` meta tags (lines 115-118)

---

## Page 2: Interview Page (`interview.html`)

**Purpose**: Functional SPA with 3 view states. Include `<script src="app.js"></script>` at bottom.

### Top Bar (always visible)
```
┌──────────────────────────────────────────────────────────┐
│ ◆ Interview AI          [API Key: ••••••••••] [Config ▾] │
└──────────────────────────────────────────────────────────┘
```
- Logo links back to `index.html`
- API Key input field (type="password", id="apiKeyInput")
- Config dropdown for API base URL (default: `http://localhost:8000/api/v1`)
- Store API key in `localStorage` so it persists

### State 1: Setup View (`id="setup-view"`)

```
┌─────────────────────────────────────────────────────┐
│                  🎯 Setup Your Interview             │
│                                                      │
│  ┌─ Info Box ──────────────────────────────────────┐ │
│  │ How it works: 1. Paste resume 2. Paste job      │ │
│  │ 3. Configure settings 4. Start interview        │ │
│  └─────────────────────────────────────────────────┘ │
│                                                      │
│  ┌─ Resume Panel (panel class) ────────────────────┐ │
│  │ Your Resume (LaTeX Format)                      │ │
│  │ ┌─ textarea (input-field, 300px height) ──────┐ │ │
│  │ │ \documentclass{article}...                   │ │ │
│  │ └─────────────────────────────────────────────┘ │ │
│  │ [Preview Parsed ▾] ← collapsible               │ │
│  │   Name: John Doe                                │ │
│  │   Skills: Python, JS...                         │ │
│  └─────────────────────────────────────────────────┘ │
│                                                      │
│  ┌─ Job Panel (panel class) ──────────────────────┐ │
│  │ Job Description (Plain Text)                    │ │
│  │ ┌─ textarea (input-field, 300px height) ──────┐ │ │
│  │ │ Senior Software Engineer...                  │ │ │
│  │ └─────────────────────────────────────────────┘ │ │
│  │ [Preview Parsed ▾] ← collapsible               │ │
│  └─────────────────────────────────────────────────┘ │
│                                                      │
│  ┌─ Settings Panel ───────────────────────────────┐ │
│  │ Focus Area: [behavioral ▾]                      │ │
│  │ ☑ Enable Adaptive Strategy                      │ │
│  │ ☑ Enable Outcome Prediction                     │ │
│  └─────────────────────────────────────────────────┘ │
│                                                      │
│        [ ◆ Start Interview ]  (btn-primary)          │
│        disabled until resume + job filled             │
└─────────────────────────────────────────────────────┘
```

**Key IDs**:
- `#resumeInput` — textarea
- `#jobInput` — textarea
- `#focusArea` — select
- `#adaptiveToggle` — checkbox
- `#predictionToggle` — checkbox
- `#startBtn` — button
- `#resumePreview` — collapsible div
- `#jobPreview` — collapsible div

**API calls on Start** (sequential):
1. `POST /parse/resume` → store response as `resumeData`
2. `POST /parse/job` → store response as `jobData`
3. `POST /interview/initialize` → get `session_id`, transition to Interview view

### State 2: Interview View (`id="interview-view"`)

```
┌─────────────────────────────────────────────────────┐
│  Turn 3 of 8                                         │
│  ┌─ progress-track ──────────────────────────────┐  │
│  │████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│  │
│  └───────────────────────────────────────────────┘  │
│                                                      │
│  ┌─ Conversation History (chat-scroll) ──────────┐  │
│  │                                                │  │
│  │  🤖 Q1: Tell me about a time you led a team... │  │
│  │  👤 A1: In my previous role at...              │  │
│  │  📊 Scores: ████ 4/5 completeness              │  │
│  │  ─────────────────────────────────              │  │
│  │  🤖 Q2: How did you handle conflicts?          │  │
│  │  👤 A2: I approached the situation by...        │  │
│  │  📊 Scores: ███░ 3/5 completeness              │  │
│  │                                                │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ┌─ Current Question (glass-card) ───────────────┐  │
│  │  Question 3 • Behavioral                       │  │
│  │  "Describe a situation where you had to         │  │
│  │   deliver results under tight deadlines."       │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ┌─ Answer Input ────────────────────────────────┐  │
│  │ Type your answer... Use STAR format            │  │
│  │                                                │  │
│  │                                                │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  [ ◆ Submit Answer ]          [ End Early ]          │
│                                                      │
│  ┌─ Prediction Alert (shown after turn 3) ───────┐  │
│  │ 🔮 Predicted: Pass (78% confidence)            │  │
│  └────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

**Key IDs**:
- `#progressBar` — div with `progress-fill` inside `progress-track`
- `#turnLabel` — "Turn X of Y" text
- `#chatHistory` — scrollable div, append turns here
- `#questionBox` — glass-card showing current question
- `#answerInput` — textarea
- `#submitBtn` — button
- `#endBtn` — button
- `#predictionAlert` — hidden by default, shown after turn 3

**API flow per turn**:
1. `GET /interview/{session_id}/question` → display in `#questionBox`
2. User types answer in `#answerInput`
3. `POST /interview/{session_id}/answer` → receive evaluation
4. Append Q+A+scores to `#chatHistory`
5. If `should_continue` → repeat from step 1
6. If `!should_continue` → transition to Results view

**Conversation history item HTML** (append per turn):
```html
<div class="panel p-4 mb-3">
    <div class="flex items-center gap-2 mb-2">
        <iconify-icon icon="solar:chat-round-dots-bold" class="text-zinc-500"/>
        <span class="text-xs text-zinc-500">Question {N} • {competency}</span>
    </div>
    <p class="text-zinc-300 text-sm mb-3">{question}</p>
    
    <div class="flex items-center gap-2 mb-2">
        <iconify-icon icon="solar:user-bold" class="text-zinc-500"/>
        <span class="text-xs text-zinc-500">Your Answer</span>
    </div>
    <p class="text-zinc-400 text-sm mb-3">{answer}</p>
    
    <!-- Score bars -->
    <div class="grid grid-cols-5 gap-2 text-xs">
        <div>
            <span class="text-zinc-500">Complete</span>
            <div class="score-bar-bg mt-1">
                <div class="score-bar-fill score-{n}" style="width:{n*20}%"></div>
            </div>
        </div>
        <!-- repeat for: depth, structure, relevance, confidence -->
    </div>
</div>
```

### State 3: Results View (`id="results-view"`)

```
┌─────────────────────────────────────────────────────┐
│  ┌─ Success Banner ──────────────────────────────┐  │
│  │ ✅ Great job! Your interview is complete.      │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ┌─ Benchmark Card (glass-card) ─────────────────┐  │
│  │  Readiness: READY        Percentile: Top 30%   │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ┌─ Coaching Report (panel) ─────────────────────┐  │
│  │  [rendered markdown from report.markdown]       │  │
│  │  ...                                           │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ┌─ Insights Grid (2 cols) ──────────────────────┐  │
│  │ ┌─ Strengths ──┐  ┌─ Skill Gaps ────────────┐ │  │
│  │ │ ✓ Clear comm  │  │ ⚠ Critical: No metrics  │ │  │
│  │ │ ✓ Good struct │  │ ● Moderate: Vague examp │ │  │
│  │ └──────────────┘  └─────────────────────────┘ │  │
│  │ ┌─ Answer Patterns ┐  ┌─ Stats ────────────┐ │  │
│  │ │ Strengths: ...    │  │ Turns: 8           │ │  │
│  │ │ Weaknesses: ...   │  │ Agent calls: 24    │ │  │
│  │ └──────────────────┘  └────────────────────┘ │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│        [ ◆ Start New Interview ]                     │
└─────────────────────────────────────────────────────┘
```

**Key IDs**:
- `#resultsBanner`
- `#benchmarkCard` — readiness + percentile
- `#reportContent` — rendered markdown
- `#strengthsList`
- `#skillGapsList`  
- `#patternCard`
- `#statsCard`
- `#restartBtn`

**API call**: `GET /interview/{session_id}/report` → populate all sections

---

## `app.js` — State Management & API Logic

### State Object
```javascript
const state = {
    apiKey: localStorage.getItem('interviewai_apikey') || '',
    baseUrl: localStorage.getItem('interviewai_baseurl') || 'http://localhost:8000/api/v1',
    sessionId: null,
    currentTurn: 0,
    maxTurns: 8,
    currentQuestion: null,
    conversationHistory: [],
    resumeData: null,
    jobData: null,
    isLoading: false,
};
```

### API Helper
```javascript
async function apiCall(method, path, body = null) {
    const url = `${state.baseUrl}${path}`;
    const opts = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'X-API-Key': state.apiKey,
        },
    };
    if (body) opts.body = JSON.stringify(body);
    
    const res = await fetch(url, opts);
    if (!res.ok) {
        const err = await res.json().catch(() => ({ message: res.statusText }));
        throw new Error(err.message || `API Error ${res.status}`);
    }
    return res.json();
}
```

### View Switching
```javascript
function showView(viewId) {
    document.querySelectorAll('.page-section').forEach(el => el.classList.remove('active'));
    document.getElementById(viewId).classList.add('active');
}
// showView('setup-view')    — default
// showView('interview-view') — after init
// showView('results-view')   — after completion
```

### Key Functions

| Function | Trigger | API Call | Next Action |
|----------|---------|----------|-------------|
| `handleStart()` | Start button click | `POST /parse/resume` → `POST /parse/job` → `POST /interview/initialize` | `showView('interview-view')`, `fetchQuestion()` |
| `fetchQuestion()` | After init + after each submit | `GET /interview/{id}/question` | Display in `#questionBox` |
| `handleSubmit()` | Submit button click | `POST /interview/{id}/answer` | Append to history, check `should_continue`, either `fetchQuestion()` or `handleComplete()` |
| `handleEndEarly()` | End Early button | `POST /interview/{id}/end` | `handleComplete()` |
| `handleComplete()` | Auto or manual end | `GET /interview/{id}/report` | `showView('results-view')`, render report |
| `handleRestart()` | Restart button | none | Reset state, `showView('setup-view')` |

### Loading States
Wrap each API call with:
```javascript
function setLoading(buttonEl, isLoading) {
    buttonEl.disabled = isLoading;
    buttonEl.innerHTML = isLoading 
        ? '<div class="flex gap-1 items-center justify-center"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div>'
        : buttonEl.dataset.label;  // store original label in data-label
}
```

### Error Handling
```javascript
function showToast(message, type = 'error') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 5000);
}
```

### Markdown Rendering (simple)
For the coaching report, use a lightweight approach:
```javascript
function renderMarkdown(md) {
    return md
        .replace(/^### (.*$)/gim, '<h3 class="text-lg font-medium text-white mt-4 mb-2 font-geist">$1</h3>')
        .replace(/^## (.*$)/gim, '<h2 class="text-xl font-medium text-white mt-6 mb-3 font-geist">$1</h2>')
        .replace(/^# (.*$)/gim, '<h1 class="text-2xl font-medium text-white mt-8 mb-4 font-geist">$1</h1>')
        .replace(/\*\*(.*?)\*\*/g, '<strong class="text-zinc-200">$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/^- (.*$)/gim, '<li class="text-zinc-400 ml-4">$1</li>')
        .replace(/\n/g, '<br>');
}
```

---

## Tailwind Classes Cheat Sheet (from template's design language)

| Use Case | Classes |
|----------|---------|
| Page background | `bg-[#09090b] text-white` |
| Card/Panel bg | `bg-[#0e0e11]` or `bg-white/[0.02]` |
| Inner card bg | `bg-[#131316]` |
| Darkest bg | `bg-[#09090b]` |
| Border subtle | `border-white/5` |
| Border medium | `border-white/10` |
| Text primary | `text-white` or `text-zinc-200` |
| Text secondary | `text-zinc-400` |
| Text muted | `text-zinc-500` |
| Heading | `font-geist font-medium tracking-tight` |
| Rounded card | `rounded-3xl` |
| Rounded button | `rounded-full` |
| Rounded input | `rounded-xl` |
| Hover card | `hover:bg-white/[0.02] transition-all duration-500` |
| Shadow heavy | `shadow-[0_20px_40px_rgba(0,0,0,0.3)]` |
| Animation entry | `[animation:animationIn_0.8s_ease-out_0.1s_both] animate-on-scroll` |

---

## Init Script (add to both pages, before `</body>`)

```html
<script>
    // Initialize scroll animations
    (function () {
        const once = true;
        if (!window.__inViewIO) {
            window.__inViewIO = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("animate");
                        if (once) window.__inViewIO.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.2, rootMargin: "0px 0px -10% 0px" });
        }
        document.querySelectorAll(".animate-on-scroll").forEach((el) => {
            window.__inViewIO.observe(el);
        });
        // Initialize Lucide icons
        lucide.createIcons();
    })();
</script>
```
