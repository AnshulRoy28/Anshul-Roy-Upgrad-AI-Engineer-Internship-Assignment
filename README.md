# AI Mock Interview Coach

A multi-agent system that conducts realistic mock interviews and provides structured feedback to help candidates prepare for their target roles.

## Features

- **Adaptive Interviewing**: Intelligent follow-ups based on answer quality
- **Multi-Agent Architecture**: 4 specialized agents working together
- **Comprehensive Feedback**: Structured coaching report with actionable insights
- **Role-Specific**: Tailored questions for different roles and seniority levels
- **Focus Areas**: Behavioral, technical, case, or mixed interviews

## Quick Start

### Prerequisites

- Python 3.8+
- Google API Key (for Gemini models)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd interview-coach
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
   - Copy `.env.example` to `.env` (or create `.env`)
   - Add your Google API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

### Run the Interview

```bash
python main.py
```

Follow the prompts to:
1. Enter your target role (e.g., "Product Manager", "Frontend Engineer Intern")
2. Optionally provide background information
3. Choose focus area: behavioral / technical / case / mixed

The interview will run for 5-7 turns, then provide comprehensive feedback.

## Architecture Overview

### Multi-Agent System

The system uses 4 specialized agents, each with a distinct role:

#### 1. **The Profiler** (Silent Strategist)
- **Runs**: Once at the start
- **Job**: Transforms candidate input into structured interview strategy
- **Output**: JSON strategy with competency pillars, difficulty arc, seniority calibration
- **Forbidden**: Never speaks to candidate

#### 2. **The Interviewer** (Conversational Agent)
- **Runs**: Every turn during the interview loop
- **Job**: Asks questions, follows up, maintains natural conversation
- **Adapts**: Based on Turn Evaluator's signals
- **Forbidden**: Never evaluates answers or gives feedback

#### 3. **The Turn Evaluator** (Silent Judge)
- **Runs**: After every candidate answer
- **Job**: Scores answer across 5 dimensions, emits next-move signal
- **Output**: JSON with scores, answer type, notable signals
- **Forbidden**: Never speaks to candidate

#### 4. **The Coach** (Mentor)
- **Runs**: Once at the end
- **Job**: Synthesizes all data into actionable coaching report
- **Output**: Structured Markdown with strengths, gaps, practice items
- **Forbidden**: Never re-conducts interview

### Agent Communication Flow

```
Profiler
   │ writes: session_strategy (JSON)
   ▼
[Session State]
   │
   ├──► Interviewer reads: strategy, last_signal
   │         │ asks question
   │         ▼
   │    [Candidate answers]
   │         │
   ├──► Turn Evaluator reads: question, answer, strategy
   │         │ writes: turn_score (JSON)
   │         │ emits: next_move signal
   │         ▼
   │    [Loop continues or terminates]
   │
   └──► Coach reads: everything
              │ writes: coaching_report (Markdown)
              ▼
         [End of session]
```

### Session State

All agents communicate through a shared session state (dictionary):

- `candidate_role`: Target role
- `candidate_background`: Background info
- `focus_area`: Interview focus
- `session_strategy`: Profiler's strategy (JSON)
- `conversation_history`: All Q&A pairs
- `turn_scores`: Evaluator scores for each turn
- `last_evaluator_signal`: Most recent next-move signal
- `current_turn`: Turn counter
- `interview_complete`: Termination flag
- `coaching_report`: Final feedback (Markdown)

## Key Design Decisions

### 1. **Separation of Concerns**
Each agent has exactly one job it cannot delegate and one thing it's forbidden from doing. This prevents agents from collapsing into a single over-engineered prompt.

### 2. **Signal-Based Adaptation**
The Interviewer doesn't evaluate answers itself — it acts on signals from the Turn Evaluator. This separates sensing (evaluation) from acting (questioning).

### 3. **Structured Outputs**
- Profiler & Turn Evaluator: JSON (machine-readable)
- Coach: Markdown (human-readable)
- This ensures consistency and parseability

### 4. **State as Single Source of Truth**
Agents never pass data directly to each other. Everything flows through session state, making the system debuggable and extensible.

### 5. **Prompt Engineering for Messiness**
Each agent's prompt explicitly handles edge cases:
- "I don't know" responses
- Vague or rambling answers
- Off-topic responses
- Partial correctness

## Project Structure

```
interview-coach/
├── main.py                 # CLI entry point
├── config.py               # Configuration and constants
├── requirements.txt        # Dependencies
├── README.md              # This file
│
├── prompts/               # Agent prompts (one per agent)
│   ├── profiler.md
│   ├── interviewer.md
│   ├── turn_evaluator.md
│   └── coach.md
│
├── agents/                # Agent definitions
│   ├── __init__.py
│   ├── profiler.py
│   ├── interviewer.py
│   ├── turn_evaluator.py
│   └── coach.py
│
├── tools/                 # Tools for agents
│   ├── __init__.py
│   └── cli_input.py       # Candidate response capture
│
└── state/                 # State management
    ├── __init__.py
    └── schema.py          # State schema and helpers
```

## Example Transcripts

### Example 1: Strong Candidate (Product Manager)

**Input:**
- Role: Product Manager
- Background: 2 years as APM at B2B SaaS startup
- Focus: Behavioral

**Interview Highlights:**
- Turn 1: Warm-up question about product prioritization
  - Answer: Used STAR format, mentioned specific metrics (20% increase in retention)
  - Score: 4.5/5 average
  
- Turn 3: Conflict resolution with engineering team
  - Answer: Concrete example with timeline and outcome
  - Score: 4.8/5 average

**Coaching Summary:**
- Strengths: Excellent use of STAR format, concrete metrics, clear outcomes
- Gaps: Could provide more context on stakeholder management
- Priority: Practice articulating trade-offs in ambiguous situations

### Example 2: Weak Candidate (Frontend Engineer Intern)

**Input:**
- Role: Frontend Engineer Intern
- Background: (none provided)
- Focus: Technical

**Interview Highlights:**
- Turn 1: Explain the difference between let and const
  - Answer: Vague, mentioned "variables" but no specifics
  - Score: 2.1/5 average
  
- Turn 3: How would you debug a React component not rendering?
  - Answer: "I don't know, maybe check the console?"
  - Score: 1.5/5 average

**Coaching Summary:**
- Strengths: Willing to attempt answers even when uncertain
- Gaps: Fundamental concepts unclear, no structured problem-solving approach
- Priority: Study JavaScript fundamentals (scope, hoisting, closures) before next interview

### Example 3: Tricky/Edge Case (Data Analyst)

**Input:**
- Role: Senior Data Analyst
- Background: 5 years in finance analytics
- Focus: Mixed

**Interview Highlights:**
- Turn 2: SQL optimization question
  - Answer: Started strong, then went off-topic discussing Python pandas
  - Evaluator: Issued "clarify" signal
  - Follow-up: Brought back to SQL, provided solid answer
  - Score: 3.5/5 average (recovered well)
  
- Turn 5: Stakeholder communication scenario
  - Answer: Very detailed but rambling, lost thread
  - Score: 2.8/5 (completeness: 4, structure: 2)

**Coaching Summary:**
- Strengths: Deep technical knowledge, recovers well from redirects
- Gaps: Tends to over-explain, loses structure in behavioral questions
- Priority: Practice concise STAR format for behavioral questions — aim for 90 seconds per answer

## Technical Implementation

### Technology Stack

- **Python 3.8+**: Core language
- **Google Gemini 2.5 Flash**: LLM for all agents
- **google-generativeai**: Official Python client for Gemini API
- **python-dotenv**: Environment configuration

### Architecture Approach: Direct API Calls (No Frameworks)

This system uses **direct API calls** to Google's Gemini API rather than agent frameworks (ADK, LangChain, CrewAI, etc.). This was a deliberate design choice:

**Why Direct API Calls:**
- **Transparency**: Every agent interaction is explicit and visible in the code
- **Simplicity**: Only 2 dependencies instead of 10+
- **Control**: Full control over orchestration logic and agent behavior
- **Debuggability**: Easy to trace exactly what each agent does and when
- **Learning**: Clear demonstration of multi-agent patterns without framework abstractions

**Tradeoffs:**
- Manual orchestration (no built-in agent primitives)
- More boilerplate code
- No framework-specific features (streaming, built-in memory, etc.)

**Verdict**: For a prototype demonstrating multi-agent architecture and prompt engineering, direct API calls provide maximum clarity. For production systems with complex workflows, frameworks would add value.

## Tradeoffs and Limitations

### Current Limitations

1. **No Persistent Memory**: Each session is independent
2. **CLI Only**: No web interface (by design for MVP)
3. **No RAG**: Questions come from model knowledge, not external databases
4. **Single Language**: English only
5. **No Voice**: Text-based only
6. **Manual Orchestration**: No framework-based agent coordination

### Deliberate Tradeoffs

1. **Simplicity over Features**: Focused on core multi-agent architecture
2. **Direct API Calls**: Using Google GenAI client directly instead of frameworks
3. **In-Memory State**: No database (sessions are ephemeral)
4. **Fixed Turn Limit**: 7 turns maximum (prevents runaway sessions)
5. **Synchronous Execution**: No async/parallel agent execution

### Future Enhancements

- [ ] Web interface (Streamlit/Gradio)
- [ ] Session persistence and history
- [ ] RAG for role-specific question banks
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Real-time feedback during interview
- [ ] Comparison with previous sessions
- [ ] Industry-specific interview templates

## Development

### Running Tests

```bash
# TODO: Add tests
pytest tests/
```

### Modifying Prompts

All prompts are in `prompts/` as Markdown files. Edit them directly — no code changes needed.

### Adding New Agents

1. Create prompt in `prompts/your_agent.md`
2. Create agent definition in `agents/your_agent.py`
3. Wire into orchestration in `main.py`

### Debugging

Set environment variable for verbose logging:
```bash
export DEBUG=1
python main.py
```

## License

MIT

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Acknowledgments

Built with:
- **Google Gemini 2.5 Flash** - LLM powering all agent reasoning
- **Python 3.8+** - Core implementation language  
- **Direct API Integration** - No agent frameworks, pure API calls for maximum transparency

## Contact

For questions or feedback, please open an issue on GitHub.
