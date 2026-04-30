// ===== State Management =====
const state = {
    apiKey: localStorage.getItem('interviewai_apikey') || '',
    baseUrl: localStorage.getItem('interviewai_baseurl') || '/api/v1',
    sessionId: null,
    currentTurn: 0,
    maxTurns: 8,
    currentQuestion: null,
    conversationHistory: [],
    resumeData: null,
    jobData: null,
    isLoading: false,
    apiHealthy: false,
    retryCount: 0,
    maxRetries: 3,
};

// ===== Constants =====
const RETRY_DELAY = 2000; // 2 seconds
const DRAFT_SAVE_KEY = 'interviewai_draft_answer';

// ===== API Helper with Retry Logic =====
async function apiCall(method, path, body = null, retryCount = 0) {
    const url = `${state.baseUrl}${path}`;
    const opts = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'X-API-Key': state.apiKey,
        },
    };
    if (body) opts.body = JSON.stringify(body);
    
    try {
        const res = await fetch(url, opts);
        if (!res.ok) {
            const err = await res.json().catch(() => ({ message: res.statusText }));
            
            // Retry on 5xx errors
            if (res.status >= 500 && retryCount < state.maxRetries) {
                showToast(`Server error, retrying... (${retryCount + 1}/${state.maxRetries})`, 'warning');
                await sleep(RETRY_DELAY);
                return apiCall(method, path, body, retryCount + 1);
            }
            
            throw new Error(err.message || `API Error ${res.status}`);
        }
        return res.json();
    } catch (error) {
        // Retry on network errors
        if (error.name === 'TypeError' && retryCount < state.maxRetries) {
            showToast(`Network error, retrying... (${retryCount + 1}/${state.maxRetries})`, 'warning');
            await sleep(RETRY_DELAY);
            return apiCall(method, path, body, retryCount + 1);
        }
        
        throw error;
    }
}

// ===== Utility Functions =====
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function sanitizeInput(input) {
    const div = document.createElement('div');
    div.textContent = input;
    return div.innerHTML;
}

// ===== View Switching =====
function showView(viewId) {
    document.querySelectorAll('.page-section').forEach(el => el.classList.remove('active'));
    const view = document.getElementById(viewId);
    if (view) {
        view.classList.add('active');
    }
}

// ===== Loading States =====
function setLoading(buttonEl, isLoading) {
    if (!buttonEl) return;
    buttonEl.disabled = isLoading;
    if (isLoading) {
        buttonEl.innerHTML = '<div class="flex gap-1 items-center justify-center"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div>';
    } else {
        buttonEl.innerHTML = buttonEl.dataset.label || 'Submit';
    }
}

// ===== Toast Notifications =====
function showToast(message, type = 'error') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 5000);
}

// ===== Health Check =====
async function checkApiHealth() {
    try {
        const response = await fetch(`${state.baseUrl}/health`);
        if (response.ok) {
            const data = await response.json();
            state.apiHealthy = data.status === 'healthy';
            
            if (!data.api_key_configured && !state.apiKey) {
                showToast('API key not configured. Please enter your Google API key.', 'warning');
            }
            
            return state.apiHealthy;
        }
        state.apiHealthy = false;
        return false;
    } catch (error) {
        state.apiHealthy = false;
        showToast('Cannot connect to API server. Please ensure it is running.', 'error');
        return false;
    }
}

// ===== Connection Status Indicator =====
function updateConnectionStatus(isConnected) {
    const statusIndicator = document.getElementById('connectionStatus');
    if (statusIndicator) {
        if (isConnected) {
            statusIndicator.innerHTML = '<span class="text-green-400">● Connected</span>';
        } else {
            statusIndicator.innerHTML = '<span class="text-red-400">● Disconnected</span>';
        }
    }
}

// ===== Markdown Rendering =====
function renderMarkdown(md) {
    if (!md) return '';
    return md
        .replace(/^### (.*$)/gim, '<h3 class="text-lg font-medium text-white mt-4 mb-2 font-geist">$1</h3>')
        .replace(/^## (.*$)/gim, '<h2 class="text-xl font-medium text-white mt-6 mb-3 font-geist">$1</h2>')
        .replace(/^# (.*$)/gim, '<h1 class="text-2xl font-medium text-white mt-8 mb-4 font-geist">$1</h1>')
        .replace(/\*\*(.*?)\*\*/g, '<strong class="text-zinc-200">$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/^- (.*$)/gim, '<li class="text-zinc-400 ml-4">$1</li>')
        .replace(/\n\n/g, '<br><br>')
        .replace(/\n/g, '<br>');
}

// ===== Setup View Functions =====
function validateInputs() {
    const resumeInput = document.getElementById('resumeInput');
    const jobInput = document.getElementById('jobInput');
    const startBtn = document.getElementById('startBtn');
    
    if (resumeInput && jobInput && startBtn) {
        const hasResume = resumeInput.value.trim().length > 0;
        const hasJob = jobInput.value.trim().length > 0;
        const hasApiKey = state.apiKey.length > 0;
        
        startBtn.disabled = !(hasResume && hasJob && hasApiKey && state.apiHealthy);
        
        // Show helpful message if API not healthy
        if (hasResume && hasJob && hasApiKey && !state.apiHealthy) {
            startBtn.title = 'API server not connected. Please check connection.';
        } else {
            startBtn.title = '';
        }
    }
}

// ===== Auto-save Draft Answer =====
function saveDraftAnswer(answer) {
    if (answer && answer.trim().length > 0) {
        localStorage.setItem(DRAFT_SAVE_KEY, answer);
    }
}

function loadDraftAnswer() {
    return localStorage.getItem(DRAFT_SAVE_KEY) || '';
}

function clearDraftAnswer() {
    localStorage.removeItem(DRAFT_SAVE_KEY);
}

async function handleStart() {
    const resumeInput = document.getElementById('resumeInput');
    const jobInput = document.getElementById('jobInput');
    const focusArea = document.getElementById('focusArea');
    const adaptiveToggle = document.getElementById('adaptiveToggle');
    const predictionToggle = document.getElementById('predictionToggle');
    const startBtn = document.getElementById('startBtn');
    
    if (!resumeInput || !jobInput) return;
    
    const resumeText = resumeInput.value.trim();
    const jobText = jobInput.value.trim();
    
    // Validate inputs
    if (!resumeText || !jobText) {
        showToast('Please fill in both resume and job description', 'error');
        return;
    }
    
    if (!state.apiKey) {
        showToast('Please enter your API key', 'error');
        return;
    }
    
    // Check API health before starting
    const isHealthy = await checkApiHealth();
    if (!isHealthy) {
        showToast('Cannot connect to API server. Please check if it is running.', 'error');
        return;
    }
    
    setLoading(startBtn, true);
    
    try {
        // Parse resume
        showToast('Parsing resume...', 'success');
        state.resumeData = await apiCall('POST', '/parse/resume', {
            latex_content: resumeText
        });
        
        // Parse job
        showToast('Parsing job description...', 'success');
        state.jobData = await apiCall('POST', '/parse/job', {
            job_text: jobText
        });
        
        // Initialize interview
        showToast('Initializing interview...', 'success');
        const initResponse = await apiCall('POST', '/interview/initialize', {
            resume_data: state.resumeData,
            job_data: state.jobData,
            focus_area: focusArea?.value || 'behavioral',
            adaptive_strategy: adaptiveToggle?.checked ?? true,
            outcome_prediction: predictionToggle?.checked ?? true
        });
        
        state.sessionId = initResponse.session_id;
        state.maxTurns = initResponse.max_turns || 8;
        state.currentTurn = 1;
        state.conversationHistory = [];
        
        // Switch to interview view
        showView('interview-view');
        
        // Fetch first question
        await fetchQuestion();
        
        // Load any draft answer
        const draft = loadDraftAnswer();
        if (draft) {
            const answerInput = document.getElementById('answerInput');
            if (answerInput && confirm('You have a saved draft answer. Would you like to restore it?')) {
                answerInput.value = draft;
            } else {
                clearDraftAnswer();
            }
        }
        
    } catch (error) {
        showToast(`Error: ${error.message}`, 'error');
        setLoading(startBtn, false);
    }
}

async function fetchQuestion() {
    if (!state.sessionId) return;
    
    try {
        const response = await apiCall('GET', `/interview/${state.sessionId}/question`);
        
        state.currentQuestion = response;
        
        // Update UI
        const questionText = document.getElementById('questionText');
        const questionMeta = document.getElementById('questionMeta');
        const turnLabel = document.getElementById('turnLabel');
        const progressBar = document.getElementById('progressBar');
        
        if (questionText) questionText.textContent = response.question;
        if (questionMeta) questionMeta.textContent = `Question ${response.turn_number} • ${response.competency || 'General'}`;
        if (turnLabel) turnLabel.textContent = `Turn ${state.currentTurn} of ${state.maxTurns}`;
        if (progressBar) {
            const progress = (state.currentTurn / state.maxTurns) * 100;
            progressBar.style.width = `${progress}%`;
        }
        
        // Clear answer input
        const answerInput = document.getElementById('answerInput');
        if (answerInput) answerInput.value = '';
        
    } catch (error) {
        showToast(`Error fetching question: ${error.message}`, 'error');
    }
}

async function handleSubmit() {
    const answerInput = document.getElementById('answerInput');
    const submitBtn = document.getElementById('submitBtn');
    
    if (!answerInput || !state.sessionId) return;
    
    const answer = answerInput.value.trim();
    if (!answer) {
        showToast('Please enter an answer', 'error');
        return;
    }
    
    // Validate answer length
    if (answer.length > 5000) {
        showToast('Answer is too long. Please keep it under 5000 characters.', 'error');
        return;
    }
    
    setLoading(submitBtn, true);
    
    try {
        const response = await apiCall('POST', `/interview/${state.sessionId}/answer`, {
            answer: answer
        });
        
        // Clear draft after successful submission
        clearDraftAnswer();
        
        // Add to conversation history
        state.conversationHistory.push({
            turn: state.currentTurn,
            question: state.currentQuestion.question,
            answer: answer,
            evaluation: response.evaluation,
            competency: state.currentQuestion.competency
        });
        
        // Append to chat history
        appendTurnToHistory(state.currentTurn, state.currentQuestion.question, answer, response.evaluation, state.currentQuestion.competency);
        
        // Show prediction if available
        if (response.outcome_prediction && response.outcome_prediction.available) {
            showPrediction(response.outcome_prediction);
        }
        
        // Check if should continue
        if (response.should_continue && state.currentTurn < state.maxTurns) {
            state.currentTurn++;
            await fetchQuestion();
        } else {
            await handleComplete();
        }
        
        setLoading(submitBtn, false);
        
    } catch (error) {
        showToast(`Error submitting answer: ${error.message}`, 'error');
        setLoading(submitBtn, false);
    }
}

function appendTurnToHistory(turn, question, answer, evaluation, competency) {
    const chatHistory = document.getElementById('chatHistory');
    if (!chatHistory) return;
    
    const turnDiv = document.createElement('div');
    turnDiv.className = 'panel p-4 mb-3';
    
    const scores = evaluation?.scores || {};
    
    // Sanitize text content
    const safeQuestion = sanitizeInput(question);
    const safeAnswer = sanitizeInput(answer);
    const safeCompetency = sanitizeInput(competency || 'General');
    
    turnDiv.innerHTML = `
        <div class="flex items-center gap-2 mb-2">
            <iconify-icon icon="solar:chat-round-dots-bold" class="text-zinc-500"></iconify-icon>
            <span class="text-xs text-zinc-500">Question ${turn} • ${safeCompetency}</span>
        </div>
        <p class="text-zinc-300 text-sm mb-3">${safeQuestion}</p>
        
        <div class="flex items-center gap-2 mb-2">
            <iconify-icon icon="solar:user-bold" class="text-zinc-500"></iconify-icon>
            <span class="text-xs text-zinc-500">Your Answer</span>
        </div>
        <p class="text-zinc-400 text-sm mb-3">${safeAnswer}</p>
        
        <div class="grid grid-cols-5 gap-2 text-xs">
            ${createScoreBar('Complete', scores.completeness || 0)}
            ${createScoreBar('Depth', scores.depth || 0)}
            ${createScoreBar('Structure', scores.structure || 0)}
            ${createScoreBar('Relevance', scores.relevance || 0)}
            ${createScoreBar('Confidence', scores.confidence || 0)}
        </div>
    `;
    
    chatHistory.appendChild(turnDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function createScoreBar(label, score) {
    const scoreInt = Math.round(score);
    const width = scoreInt * 20;
    return `
        <div>
            <span class="text-zinc-500">${label}</span>
            <div class="score-bar-bg mt-1">
                <div class="score-bar-fill score-${scoreInt}" style="width:${width}%"></div>
            </div>
        </div>
    `;
}

function showPrediction(prediction) {
    const predictionAlert = document.getElementById('predictionAlert');
    const predictionText = document.getElementById('predictionText');
    
    if (!predictionAlert || !predictionText) return;
    
    const outcomeMap = {
        'strong pass': { text: 'Strong Pass', class: 'badge-pass' },
        'pass': { text: 'Pass', class: 'badge-pass' },
        'borderline': { text: 'Borderline', class: 'badge-borderline' },
        'fail': { text: 'Fail', class: 'badge-fail' }
    };
    
    const outcome = outcomeMap[prediction.outcome.toLowerCase()] || { text: prediction.outcome, class: 'badge-borderline' };
    
    predictionText.innerHTML = `
        Predicted: <span class="${outcome.class} px-2 py-1 rounded text-xs font-medium">${outcome.text}</span> 
        (${prediction.confidence}% confidence)
    `;
    
    predictionAlert.classList.remove('hidden');
}

async function handleEndEarly() {
    if (!state.sessionId) return;
    
    if (!confirm('Are you sure you want to end the interview early?')) {
        return;
    }
    
    try {
        await apiCall('POST', `/interview/${state.sessionId}/end`);
        await handleComplete();
    } catch (error) {
        showToast(`Error ending interview: ${error.message}`, 'error');
    }
}

async function handleComplete() {
    if (!state.sessionId) return;
    
    try {
        showToast('Generating coaching report...', 'success');
        const response = await apiCall('GET', `/interview/${state.sessionId}/report`);
        
        // Switch to results view
        showView('results-view');
        
        // Populate results
        populateResults(response);
        
    } catch (error) {
        showToast(`Error generating report: ${error.message}`, 'error');
    }
}

function populateResults(reportData) {
    const report = reportData.report;
    const metadata = reportData.metadata;
    
    // Readiness level
    const readinessLevel = document.getElementById('readinessLevel');
    if (readinessLevel && report.summary) {
        readinessLevel.textContent = (report.summary.readiness_level || 'READY').toUpperCase();
    }
    
    // Percentile
    const percentileRank = document.getElementById('percentileRank');
    if (percentileRank && report.summary) {
        percentileRank.textContent = report.summary.percentile || 'Top 30%';
    }
    
    // Report content
    const reportContent = document.getElementById('reportContent');
    if (reportContent && report.markdown) {
        reportContent.innerHTML = renderMarkdown(report.markdown);
    }
    
    // Strengths
    const strengthsList = document.getElementById('strengthsList');
    if (strengthsList && report.strengths) {
        strengthsList.innerHTML = report.strengths.map(s => 
            `<li class="flex items-start gap-2">
                <iconify-icon icon="solar:check-circle-linear" class="text-green-400 mt-0.5 flex-shrink-0"></iconify-icon>
                <span>${s}</span>
            </li>`
        ).join('');
    }
    
    // Skill gaps
    const skillGapsList = document.getElementById('skillGapsList');
    if (skillGapsList && report.skill_gaps) {
        skillGapsList.innerHTML = report.skill_gaps.map(gap => {
            const severityClass = gap.severity === 'critical' ? 'severity-critical' : 
                                 gap.severity === 'moderate' ? 'severity-moderate' : 'severity-minor';
            return `<li class="flex items-start gap-2">
                <span class="${severityClass} px-2 py-0.5 rounded text-xs font-medium">${gap.severity}</span>
                <span class="text-zinc-300">${gap.description}</span>
            </li>`;
        }).join('');
    }
    
    // Answer patterns
    const patternCard = document.getElementById('patternCard');
    if (patternCard && report.answer_patterns) {
        const patterns = report.answer_patterns;
        patternCard.innerHTML = `
            <p><strong class="text-zinc-200">Strengths:</strong> ${patterns.consistent_strengths?.join(', ') || 'N/A'}</p>
            <p><strong class="text-zinc-200">Weaknesses:</strong> ${patterns.consistent_weaknesses?.join(', ') || 'N/A'}</p>
        `;
    }
    
    // Stats
    const statsCard = document.getElementById('statsCard');
    if (statsCard && metadata) {
        statsCard.innerHTML = `
            <p><strong class="text-zinc-200">Total Turns:</strong> ${metadata.total_turns || state.currentTurn}</p>
            <p><strong class="text-zinc-200">Agent Calls:</strong> ${metadata.total_agent_calls || 'N/A'}</p>
            <p><strong class="text-zinc-200">Duration:</strong> ${metadata.session_duration || 'N/A'}</p>
        `;
    }
}

function handleRestart() {
    // Reset state
    state.sessionId = null;
    state.currentTurn = 0;
    state.conversationHistory = [];
    state.resumeData = null;
    state.jobData = null;
    
    // Clear inputs
    const resumeInput = document.getElementById('resumeInput');
    const jobInput = document.getElementById('jobInput');
    const answerInput = document.getElementById('answerInput');
    const chatHistory = document.getElementById('chatHistory');
    
    if (resumeInput) resumeInput.value = '';
    if (jobInput) jobInput.value = '';
    if (answerInput) answerInput.value = '';
    if (chatHistory) chatHistory.innerHTML = '';
    
    // Hide prediction
    const predictionAlert = document.getElementById('predictionAlert');
    if (predictionAlert) predictionAlert.classList.add('hidden');
    
    // Switch to setup view
    showView('setup-view');
}

// ===== Event Listeners =====
document.addEventListener('DOMContentLoaded', async () => {
    // Check API health on startup
    const isHealthy = await checkApiHealth();
    updateConnectionStatus(isHealthy);
    
    // Periodic health check every 30 seconds
    setInterval(async () => {
        const healthy = await checkApiHealth();
        updateConnectionStatus(healthy);
        validateInputs();
    }, 30000);
    
    // API Key and Base URL inputs
    const apiKeyInput = document.getElementById('apiKeyInput');
    const baseUrlInput = document.getElementById('baseUrlInput');
    
    if (apiKeyInput) {
        apiKeyInput.value = state.apiKey;
        apiKeyInput.addEventListener('input', (e) => {
            state.apiKey = e.target.value;
            localStorage.setItem('interviewai_apikey', state.apiKey);
            validateInputs();
        });
    }
    
    if (baseUrlInput) {
        baseUrlInput.value = state.baseUrl;
        baseUrlInput.addEventListener('input', (e) => {
            state.baseUrl = e.target.value;
            localStorage.setItem('interviewai_baseurl', state.baseUrl);
        });
    }
    
    // Resume and Job inputs
    const resumeInput = document.getElementById('resumeInput');
    const jobInput = document.getElementById('jobInput');
    
    if (resumeInput) {
        resumeInput.addEventListener('input', validateInputs);
    }
    
    if (jobInput) {
        jobInput.addEventListener('input', validateInputs);
    }
    
    // Answer input with auto-save
    const answerInput = document.getElementById('answerInput');
    if (answerInput) {
        // Auto-save draft every 2 seconds
        let saveTimeout;
        answerInput.addEventListener('input', (e) => {
            clearTimeout(saveTimeout);
            saveTimeout = setTimeout(() => {
                saveDraftAnswer(e.target.value);
            }, 2000);
        });
    }
    
    // Preview buttons
    const resumePreviewBtn = document.getElementById('resumePreviewBtn');
    const resumePreview = document.getElementById('resumePreview');
    
    if (resumePreviewBtn && resumePreview) {
        resumePreviewBtn.addEventListener('click', () => {
            resumePreview.classList.toggle('hidden');
        });
    }
    
    const jobPreviewBtn = document.getElementById('jobPreviewBtn');
    const jobPreview = document.getElementById('jobPreview');
    
    if (jobPreviewBtn && jobPreview) {
        jobPreviewBtn.addEventListener('click', () => {
            jobPreview.classList.toggle('hidden');
        });
    }
    
    // Start button
    const startBtn = document.getElementById('startBtn');
    if (startBtn) {
        startBtn.addEventListener('click', handleStart);
    }
    
    // Submit button
    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn) {
        submitBtn.addEventListener('click', handleSubmit);
    }
    
    // End button
    const endBtn = document.getElementById('endBtn');
    if (endBtn) {
        endBtn.addEventListener('click', handleEndEarly);
    }
    
    // Restart button
    const restartBtn = document.getElementById('restartBtn');
    if (restartBtn) {
        restartBtn.addEventListener('click', handleRestart);
    }
    
    // Initial validation
    validateInputs();
});
