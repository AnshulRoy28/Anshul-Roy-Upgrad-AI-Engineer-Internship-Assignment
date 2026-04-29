# AI Mock Interview Coach

A multi-agent system built with Google's Agent Development Kit (ADK) that conducts realistic mock interviews and provides structured feedback.

## Features

- **Adaptive Interviewing**: Intelligently probes deeper on weak answers, moves on from strong ones
- **Multi-Dimensional Evaluation**: Scores answers on completeness, depth, structure, role-fit, and specificity
- **Structured Coaching**: Delivers actionable feedback with specific examples from the interview
- **4-Agent Architecture**: Profiler, Interviewer, Turn Evaluator, and Coach working in orchestration

## Setup

### Prerequisites

- Python 3.10 or later
- Google AI Studio API key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

1. Clone or download this repository

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set your API key:
```bash
echo 'GOOGLE_API_KEY="your-api-key-here"' > .env
```

## Usage

Run the interview coach:

```bash
python main.py
```

You'll be prompted to provide:
1. Target role (e.g., "Product Manager", "Frontend Engineer Intern")
2. Optional background (2-3 lines about your experience)
3. Focus area (Behavioral, Technical, Case, or Mixed)

The system will then conduct a 5-7 turn interview and provide detailed feedback at the end.

## Architecture

### Agent Roles

**1. Profiler** (Silent Strategist)
- Runs once at the start
- Transforms candidate input into structured interview strategy
- Outputs: seniority calibration, competency pillars, difficulty arc

**2. Interviewer** (Conversational Agent)
- Only agent that interacts with the candidate
- Asks questions and follows up based on evaluator signals
- Adapts behavior: probe deeper, advance, clarify, recover, or wrap up

**3. Turn Evaluator** (Silent Judge)
- Runs after every candidate answer
- Scores on 5 dimensions (1-5 scale)
- Emits next_move signal to guide the Interviewer

**4. Coach** (Feedback Synthesizer)
- Runs once after interview completes
- Reads full transcript and all scores
- Produces structured Markdown report with actionable feedback

### Orchestration

```
Profiler → [Interview Loop: Interviewer ↔ Turn Evaluator] → Coach
```

The Interview Loop uses ADK's `LoopAgent` to iterate between the Interviewer and Turn Evaluator until:
- 7 turns are reached (max_iterations), OR
- Turn Evaluator signals "wrap_up"

### State Management

All agents communicate through session state:
- `session_strategy`: Profiler's output, read by all downstream agents
- `last_evaluator_signal`: Turn Evaluator's output, read by Interviewer
- `turn_scores`: List of all evaluation JSONs, read by Coach
- `conversation_history`: Full transcript, read by Coach
- `interview_complete`: Boolean flag for loop termination

## Key Design Decisions

### 1. Separation of Concerns
Each agent has exactly one job it cannot delegate:
- Profiler: Strategy creation
- Interviewer: Question asking
- Turn Evaluator: Answer scoring
- Coach: Feedback synthesis

### 2. Signal-Based Adaptation
The Interviewer doesn't evaluate answers itself. It reads the Turn Evaluator's `next_move` signal and adapts accordingly. This separates sensing (evaluation) from acting (interviewing).

### 3. Stateless Agents with Shared State
Agents use `include_contents='none'` to avoid context bloat. They read what they need from session state via placeholder syntax (`{variable_name}`).

### 4. Structured Outputs
Profiler and Turn Evaluator emit JSON. Coach emits Markdown. This makes outputs machine-readable and human-readable respectively.

### 5. Termination via Callback
The Turn Evaluator's `after_agent_callback` checks termination conditions and sets `interview_complete` flag, which the LoopAgent respects.

## Tradeoffs

**What We Optimized For:**
- Clear agent boundaries
- Robust handling of messy input ("I don't know", vague answers, off-topic responses)
- Actionable feedback (not just scores)

**What We Didn't Build:**
- Web UI (CLI only)
- RAG/grounding (uses LLM knowledge only)
- Multi-session persistence (in-memory only)
- Real-time streaming of feedback

## Example Transcripts

See `examples/` directory for:
- `strong_candidate.txt`: High-performing candidate
- `weak_candidate.txt`: Struggling candidate
- `edge_case.txt`: Tricky responses (vague, off-topic, "I don't know")

## Project Structure

```
interview-coach/
├── main.py                      # CLI entry point
├── config.py                    # Constants and prompt loader
├── requirements.txt
├── README.md
├── prompts/                     # Agent system prompts
│   ├── profiler.md
│   ├── interviewer.md
│   ├── turn_evaluator.md
│   └── coach.md
├── agents/                      # Agent definitions
│   ├── profiler.py
│   ├── interviewer.py
│   ├── turn_evaluator.py
│   └── coach.py
├── tools/                       # Custom tools
│   └── cli_input.py
├── orchestration/               # Agent composition
│   ├── interview_loop.py
│   └── pipeline.py
└── state/
    └── schema.py                # State keys and helpers
```

## Extending the System

### Add New Competency Pillars
Edit `prompts/profiler.md` to include role-specific competencies.

### Change Interview Length
Modify `MAX_INTERVIEW_TURNS` in `config.py`.

### Add Web UI
Replace `tools/cli_input.py` with a web-based input tool and update the Interviewer agent's tools list.

### Add RAG/Grounding
Integrate Google Search or Knowledge Engine tools into the Interviewer agent for role-specific question banks.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

Built with [Google Agent Development Kit (ADK)](https://adk.dev/)
