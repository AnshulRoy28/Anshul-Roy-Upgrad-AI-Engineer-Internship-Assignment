# AI Mock Interview Coach

An intelligent mock interview system powered by Google's Agent Development Kit (ADK) and Gemini API. Features a multi-agent architecture with adaptive difficulty, real-time evaluation, outcome prediction, and personalized coaching.

**UpGrad AI Engineer Internship Assignment - Anshul Roy**

---

## 📋 Table of Contents

- [Setup & Run Instructions](#setup--run-instructions)
- [Architecture Overview](#architecture-overview)
- [Key Design Decisions](#key-design-decisions)
- [Example Interview Transcripts](#example-interview-transcripts)
- [Project Structure](#project-structure)

---

## 🚀 Setup & Run Instructions

### Prerequisites

- Python 3.8+
- Google API Key ([Get one here](https://aistudio.google.com/app/apikey))

### Local Development

```bash
# 1. Clone the repository
git clone https://github.com/AnshulRoy28/Anshul-Roy-Upgrad-AI-Engineer-Internship-Assignment.git
cd Anshul-Roy-Upgrad-AI-Engineer-Internship-Assignment

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env and add: GOOGLE_API_KEY=your_api_key_here

# 4. Run the server
python run_server.py
```

**Or use startup scripts:**
- Linux/Mac: `./start.sh`
- Windows: `start.bat`

Open http://localhost:8000 in your browser.

### Deploy to Google Cloud Run

1. **Push code to GitHub**

2. **Go to Cloud Run Console**: https://console.cloud.google.com/run

3. **Create Service** → **Deploy from GitHub**
   - Repository: This repo
   - Branch: `main`
   - Build Type: Dockerfile

4. **Configure**:
   - Region: `us-central1`
   - Authentication: Allow unauthenticated
   - Container port: `8080`
   - Environment variable: `GOOGLE_API_KEY=your_key`

5. **Deploy** - Cloud Run will build and deploy automatically

---

## 🏗️ Architecture Overview

### Multi-Agent System

The system uses **four specialized agents** orchestrated in a pipeline:

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                             │
│  (Coordinates agents, manages state, handles workflow)      │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   PROFILER   │    │ INTERVIEWER  │    │  EVALUATOR   │
│              │    │              │    │              │
│ Analyzes     │───▶│ Generates    │───▶│ Scores       │
│ candidate &  │    │ contextual   │    │ answers on   │
│ creates      │    │ questions    │    │ 5 dimensions │
│ strategy     │    │              │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
                                                │
                                                ▼
                                        ┌──────────────┐
                                        │    COACH     │
                                        │              │
                                        │ Generates    │
                                        │ personalized │
                                        │ feedback     │
                                        └──────────────┘
```

### Agent Responsibilities

#### 1. **ProfilerAgent** (`adk_agents/profiler_agent.py`)

**Purpose**: Analyzes candidate background and creates interview strategy

**Inputs**:
- Candidate resume (parsed)
- Target job description (parsed)
- Focus area (behavioral/technical/case/mixed)

**Outputs**:
- Interview strategy with:
  - Competencies to assess
  - Difficulty level
  - Question distribution
  - Success criteria

**Key Features**:
- Identifies skill gaps between resume and job requirements
- Determines appropriate difficulty level
- Creates personalized competency map

**Prompt**: `prompts/profiler.md`

#### 2. **InterviewerAgent** (`adk_agents/interviewer_agent.py`)

**Purpose**: Generates contextual interview questions

**Inputs**:
- Interview strategy (from Profiler)
- Conversation history
- Last evaluator signal (advance/probe/wrap_up)
- Current competency being assessed

**Outputs**:
- Next interview question
- Question type (new_competency/follow_up/probe)
- Target competency

**Key Features**:
- Adaptive questioning based on previous answers
- Follows STAR format for behavioral questions
- Maintains conversation flow
- Uses memory to avoid repetition

**Prompt**: `prompts/interviewer.md`

#### 3. **EvaluatorAgent** (`adk_agents/evaluator_agent.py`)

**Purpose**: Scores answers and provides real-time feedback

**Inputs**:
- Question asked
- Candidate's answer
- Interview strategy
- Conversation history

**Outputs**:
- Scores on 5 dimensions (1-5 scale):
  - **Completeness**: Did they answer fully?
  - **Depth**: How detailed was the answer?
  - **Structure**: Was it well-organized (STAR format)?
  - **Relevance**: Did it relate to the job?
  - **Confidence**: How assured was the delivery?
- Next move signal (advance/probe/wrap_up)
- Aggregate metrics

**Key Features**:
- Real-time scoring
- Pattern detection across answers
- Adaptive difficulty adjustment
- Outcome prediction (after 3 turns)

**Prompt**: `prompts/turn_evaluator.md`

#### 4. **CoachAgent** (`adk_agents/coach_agent.py`)

**Purpose**: Generates personalized coaching report

**Inputs**:
- Complete conversation history
- All evaluation scores
- Interview strategy
- Aggregate metrics

**Outputs**:
- Comprehensive coaching report with:
  - Overall performance assessment
  - Readiness level (READY/NEEDS_PRACTICE/NOT_READY)
  - Percentile ranking
  - Strengths identified
  - Skill gaps with severity
  - 2-week practice plan
  - Answer pattern analysis

**Key Features**:
- Benchmarking against typical candidates
- Actionable improvement recommendations
- Structured practice plan
- Pattern recognition

**Prompt**: `prompts/coach.md`

### Orchestrator (`adk_agents/orchestrator.py`)

**Responsibilities**:
- Coordinates all agents in sequence
- Manages session state
- Handles conversation history
- Implements adaptive features:
  - Adaptive strategy adjustment
  - Outcome prediction
  - Pattern detection
- Tracks metadata (agent calls, timing)

**State Management** (`state/schema.py`):
- Session strategy
- Conversation history
- Turn scores
- Current turn number
- Evaluator signals
- Aggregate metrics

### Data Flow

```
1. User uploads resume + job description
   ↓
2. ProfilerAgent creates interview strategy
   ↓
3. For each turn (1 to MAX_TURNS):
   a. InterviewerAgent generates question
   b. User provides answer
   c. EvaluatorAgent scores answer
   d. Check if should continue
   ↓
4. CoachAgent generates final report
```

---

## 🎯 Key Design Decisions

### 1. **Multi-Agent Architecture (ADK Pattern)**

**Decision**: Use specialized agents instead of a monolithic system

**Rationale**:
- **Separation of concerns**: Each agent has a single, well-defined responsibility
- **Modularity**: Easy to update/replace individual agents
- **Scalability**: Can run agents in parallel or distributed
- **Maintainability**: Easier to debug and test individual components

**Tradeoffs**:
- ✅ More maintainable and testable
- ✅ Better prompt engineering per agent
- ❌ More complex orchestration
- ❌ Higher latency (sequential agent calls)

### 2. **Agent Memory System**

**Decision**: Implement three-tier memory (short-term, long-term, working)

**Rationale**:
- **Short-term**: Recent context (last 3 turns)
- **Long-term**: Persistent patterns across session
- **Working**: Current task-specific data

**Tradeoffs**:
- ✅ Agents maintain context
- ✅ Avoid repetitive questions
- ✅ Better pattern detection
- ❌ Increased state management complexity

### 3. **Real-Time Evaluation (5 Dimensions)**

**Decision**: Score each answer on 5 specific dimensions

**Rationale**:
- Provides granular feedback
- Easier to identify specific weaknesses
- More actionable than single score
- Industry-standard dimensions

**Tradeoffs**:
- ✅ Detailed, actionable feedback
- ✅ Better coaching insights
- ❌ More complex evaluation logic
- ❌ Requires careful prompt engineering

### 4. **Adaptive Difficulty**

**Decision**: Adjust question difficulty based on performance

**Rationale**:
- Keeps candidates engaged (not too easy/hard)
- Better assessment of true skill level
- More realistic interview experience

**Implementation**:
- Monitor average scores across turns
- Adjust strategy if consistently high/low
- Signal to Interviewer via evaluator feedback

**Tradeoffs**:
- ✅ More engaging experience
- ✅ Better skill assessment
- ❌ Harder to compare across candidates
- ❌ More complex logic

### 5. **Unified Server (Flask)**

**Decision**: Single server for both API and frontend

**Rationale**:
- Simpler deployment (one process)
- No CORS issues (same origin)
- Easier local development
- Production-ready with Gunicorn

**Tradeoffs**:
- ✅ Simple deployment
- ✅ No CORS configuration
- ❌ Less flexible than microservices
- ❌ Frontend and backend coupled

### 6. **LaTeX Resume Parsing**

**Decision**: Support LaTeX format for resumes

**Rationale**:
- Common format in tech/academia
- Structured, parseable format
- Rich semantic information

**Implementation**: `utils/latex_parser.py`

**Tradeoffs**:
- ✅ Better parsing accuracy
- ✅ Structured data extraction
- ❌ Limited to LaTeX format
- ❌ Requires format compliance

### 7. **Session Management (In-Memory)**

**Decision**: Store sessions in memory with 24-hour expiration

**Rationale**:
- Simple implementation
- Fast access
- Sufficient for demo/prototype

**Tradeoffs**:
- ✅ Fast and simple
- ✅ No database needed
- ❌ Lost on server restart
- ❌ Not suitable for high scale

**Production Alternative**: Redis or database-backed sessions

### 8. **Gemini 2.5 Flash Model**

**Decision**: Use Gemini 2.5 Flash for all agents

**Rationale**:
- Fast response times (3-7s per turn)
- Cost-effective
- Sufficient capability for task
- Consistent behavior across agents

**Tradeoffs**:
- ✅ Fast and affordable
- ✅ Good quality responses
- ❌ Not as capable as larger models
- ❌ Occasional inconsistencies

---

## 📝 Example Interview Transcripts

### Example 1: Strong Candidate (Senior Software Engineer)

**Background**:
- 5 years experience
- Strong system design skills
- Leadership experience

**Strategy**: Behavioral + Technical, Senior level

---

**Turn 1**

**Interviewer**: "Tell me about a time when you had to scale a system to handle significantly increased traffic. What was the situation, and how did you approach it?"

**Candidate**: "At my previous company, we experienced a 10x traffic spike during a product launch. I was the tech lead responsible for ensuring our API could handle it. I started by profiling our current bottlenecks using New Relic and found our database queries were the main issue. I implemented Redis caching for frequently accessed data, optimized our most expensive queries by adding indexes, and set up horizontal scaling with Kubernetes. We also implemented rate limiting to prevent abuse. The result was we handled the spike with 99.9% uptime and reduced average response time from 800ms to 200ms."

**Evaluation**:
- Completeness: 5/5 (Full STAR format)
- Depth: 5/5 (Specific metrics and tools)
- Structure: 5/5 (Clear, organized)
- Relevance: 5/5 (Directly addresses question)
- Confidence: 5/5 (Assured delivery)

**Signal**: Advance to next competency

---

**Turn 2**

**Interviewer**: "Describe a situation where you had to make a difficult technical decision with incomplete information. How did you approach it?"

**Candidate**: "We needed to choose between microservices and a monolith for a new product with uncertain scale. I didn't have clear traffic projections. I gathered the team, listed our constraints: 3-month deadline, team of 5 engineers, unknown scale. I created a decision matrix weighing factors like development speed, operational complexity, and future flexibility. We decided on a modular monolith - easier to build quickly but structured for future splitting. I documented the decision and set review points at 6 and 12 months. This proved right - we launched on time and split into microservices after 18 months when we had real data."

**Evaluation**:
- Completeness: 5/5
- Depth: 5/5
- Structure: 5/5
- Relevance: 5/5
- Confidence: 5/5

**Signal**: Advance

---

**Final Assessment**:
- **Readiness**: READY
- **Percentile**: Top 10%
- **Strengths**: Excellent STAR format, quantifiable results, strategic thinking
- **Recommendation**: Strong hire

---

### Example 2: Weak Candidate (Junior Developer)

**Background**:
- 1 year experience
- Limited project scope
- Applying for mid-level role

**Strategy**: Behavioral + Technical, Mid level

---

**Turn 1**

**Interviewer**: "Tell me about a challenging technical problem you solved recently. What was your approach?"

**Candidate**: "I had a bug in my code that was hard to find. I spent a lot of time looking at it and eventually found it was a typo in a variable name. It took me a few hours but I fixed it."

**Evaluation**:
- Completeness: 2/5 (Vague, missing context)
- Depth: 1/5 (No technical details)
- Structure: 2/5 (No clear structure)
- Relevance: 2/5 (Too simple for mid-level)
- Confidence: 3/5 (Uncertain)

**Signal**: Probe deeper

---

**Turn 2**

**Interviewer**: "Can you elaborate on the debugging process? What tools or techniques did you use to identify the issue?"

**Candidate**: "Um, I just used console.log statements to see what was happening. I printed out the variables and saw one was undefined. Then I checked the spelling and fixed it."

**Evaluation**:
- Completeness: 3/5 (More detail but still basic)
- Depth: 2/5 (Basic debugging only)
- Structure: 3/5 (Somewhat organized)
- Relevance: 2/5 (Still too simple)
- Confidence: 2/5 (Hesitant)

**Signal**: Probe

---

**Turn 3**

**Interviewer**: "Tell me about a time you had to work with a team to deliver a feature under a tight deadline."

**Candidate**: "We had a project due and everyone was working on it. I did my part and we finished on time. It was stressful but we made it."

**Evaluation**:
- Completeness: 2/5 (Very vague)
- Depth: 1/5 (No specifics)
- Structure: 2/5 (Lacks STAR format)
- Relevance: 2/5 (Generic answer)
- Confidence: 2/5 (Uncertain)

**Signal**: Wrap up (low performance)

---

**Final Assessment**:
- **Readiness**: NEEDS_PRACTICE
- **Percentile**: Bottom 30%
- **Skill Gaps**: 
  - STAR format (Critical)
  - Technical depth (High)
  - Quantifiable results (High)
- **Recommendation**: Practice behavioral questions, work on more complex projects

---

### Example 3: Tricky/Edge Case (Career Switcher)

**Background**:
- 10 years in finance
- 1 year coding bootcamp + self-taught
- Strong analytical skills but limited tech experience

**Strategy**: Mixed (behavioral from finance, technical from bootcamp)

---

**Turn 1**

**Interviewer**: "Tell me about a time when you had to learn a new technology quickly to solve a problem."

**Candidate**: "In my bootcamp capstone project, I needed to implement real-time notifications but had never used WebSockets. I had 2 weeks before the demo. I started by reading the Socket.io documentation and building a simple chat app to understand the concepts. Then I watched a few tutorials on YouTube to see different implementation patterns. I applied it to my project - a stock trading simulator that needed live price updates. I ran into CORS issues initially, which I debugged using Chrome DevTools. The final implementation worked smoothly and impressed the instructors. This experience taught me I can pick up new technologies quickly when needed."

**Evaluation**:
- Completeness: 4/5 (Good STAR format)
- Depth: 4/5 (Specific technologies and process)
- Structure: 5/5 (Well organized)
- Relevance: 4/5 (Shows learning ability)
- Confidence: 4/5 (Assured)

**Signal**: Advance

---

**Turn 2**

**Interviewer**: "Describe a situation where you had to handle conflicting priorities. How did you manage it?"

**Candidate**: "In my previous finance role, I was managing a portfolio rebalancing project while also being asked to prepare an urgent client presentation. Both were high priority. I assessed the deadlines - presentation was in 2 days, rebalancing had a week. I delegated parts of the rebalancing to my junior analyst with clear instructions and checkpoints. I focused on the presentation, working late to ensure quality. I checked in with my analyst daily on the rebalancing progress. Both were delivered successfully. The key was clear communication with stakeholders about timelines and delegation to my team."

**Evaluation**:
- Completeness: 5/5 (Complete STAR)
- Depth: 4/5 (Good detail)
- Structure: 5/5 (Excellent structure)
- Relevance: 3/5 (Finance context, not tech)
- Confidence: 5/5 (Very confident)

**Signal**: Advance but probe technical depth

---

**Turn 3**

**Interviewer**: "Walk me through how you would design a REST API for a simple todo application. What endpoints would you create?"

**Candidate**: "I would create a RESTful API with these endpoints: GET /todos to list all todos, POST /todos to create a new todo, GET /todos/:id to get a specific todo, PUT /todos/:id to update a todo, and DELETE /todos/:id to delete a todo. Each todo would have an id, title, description, completed status, and timestamps. I'd use proper HTTP status codes - 200 for success, 201 for created, 404 for not found, 400 for bad requests. For authentication, I'd use JWT tokens passed in the Authorization header. I'd also implement pagination for the list endpoint using query parameters like ?page=1&limit=10."

**Evaluation**:
- Completeness: 4/5 (Covers main points)
- Depth: 3/5 (Good basics, lacks advanced concepts)
- Structure: 4/5 (Organized)
- Relevance: 5/5 (Directly answers question)
- Confidence: 4/5 (Confident)

**Signal**: Advance

---

**Final Assessment**:
- **Readiness**: READY (with caveats)
- **Percentile**: Top 40%
- **Strengths**: 
  - Excellent soft skills and communication
  - Strong learning ability
  - Good STAR format
  - Transferable skills from finance
- **Skill Gaps**:
  - Limited production experience (Moderate)
  - Depth in system design (Moderate)
  - Advanced technical concepts (Moderate)
- **Recommendation**: Good fit for junior-to-mid level role with mentorship. Strong potential given learning ability and soft skills.

---

## 📁 Project Structure

```
├── api_server.py              # Flask server (API + static files)
├── run_server.py              # Server launcher
├── main.py                    # CLI interface
├── config.py                  # Configuration
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container definition
├── cloudbuild.yaml            # Cloud Build config
├── .env.example               # Environment template
│
├── Frontend/                  # Web interface
│   ├── index.html             # Landing page
│   ├── interview.html         # Interview application
│   ├── app.js                 # Frontend logic
│   └── styles.css             # Styling
│
├── adk_agents/                # Multi-agent system
│   ├── base_agent.py          # Base agent class with memory
│   ├── orchestrator.py        # Agent coordinator
│   ├── profiler_agent.py      # Strategy creation
│   ├── interviewer_agent.py   # Question generation
│   ├── evaluator_agent.py     # Answer evaluation
│   └── coach_agent.py         # Coaching reports
│
├── prompts/                   # Agent prompts (separate files)
│   ├── profiler.md            # Profiler agent prompt
│   ├── interviewer.md         # Interviewer agent prompt
│   ├── turn_evaluator.md      # Evaluator agent prompt
│   └── coach.md               # Coach agent prompt
│
├── state/                     # State management
│   ├── schema.py              # State schema definitions
│   └── __init__.py
│
├── utils/                     # Utilities
│   ├── latex_parser.py        # Resume parser
│   ├── job_parser.py          # Job description parser
│   └── __init__.py
│
├── tools/                     # Agent tools
│   ├── cli_input.py           # CLI input tool
│   └── __init__.py
│
└── examples/                  # Sample data
    ├── sample_resume.tex      # Example resume
    └── sample_job_description.txt
```

---

## 🛠️ Tech Stack

- **Backend**: Flask, Python 3.11
- **Frontend**: Vanilla JavaScript (no build step)
- **AI**: Google Gemini 2.5 Flash
- **Architecture**: Google ADK patterns
- **Deployment**: Google Cloud Run (Docker)

---

## 📄 License

MIT License

---

**Anshul Roy**  
GitHub: [@AnshulRoy28](https://github.com/AnshulRoy28)  
Repository: [AI Interview Coach](https://github.com/AnshulRoy28/Anshul-Roy-Upgrad-AI-Engineer-Internship-Assignment)

**UpGrad AI Engineer Internship Assignment**
