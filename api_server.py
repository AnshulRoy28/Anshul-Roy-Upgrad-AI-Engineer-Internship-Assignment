"""Flask REST API server for AI Mock Interview Coach.

This server provides REST endpoints for the frontend to interact with
the ADK-based interview system.
"""
import os
import uuid
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.genai import Client
import config
from adk_agents.orchestrator import InterviewOrchestrator
from utils.latex_parser import parse_latex_resume, format_resume_for_context
from utils.job_parser import parse_job_description, format_job_for_context
import state

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Session storage (in-memory for now)
# In production, use Redis or a database
sessions: Dict[str, Dict[str, Any]] = {}

# Constants
MAX_RESUME_LENGTH = 50000  # characters
MAX_JOB_LENGTH = 20000  # characters
MAX_ANSWER_LENGTH = 5000  # characters
SESSION_TIMEOUT_HOURS = 24


def cleanup_expired_sessions():
    """Remove sessions older than SESSION_TIMEOUT_HOURS."""
    now = datetime.utcnow()
    expired = []
    for session_id, session_data in sessions.items():
        created_at = datetime.fromisoformat(session_data['created_at'])
        if now - created_at > timedelta(hours=SESSION_TIMEOUT_HOURS):
            expired.append(session_id)
    
    for session_id in expired:
        del sessions[session_id]
        logger.info(f"Cleaned up expired session: {session_id}")
    
    return len(expired)


def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Get session by ID, return None if not found or expired."""
    if session_id not in sessions:
        return None
    
    session = sessions[session_id]
    created_at = datetime.fromisoformat(session['created_at'])
    
    # Check if session expired
    if datetime.utcnow() - created_at > timedelta(hours=SESSION_TIMEOUT_HOURS):
        del sessions[session_id]
        logger.info(f"Session expired: {session_id}")
        return None
    
    return session


def validate_input_length(content: str, max_length: int, field_name: str) -> Optional[tuple]:
    """Validate input length, return error tuple if invalid."""
    if not content or not content.strip():
        return jsonify({
            'error': 'INVALID_REQUEST',
            'message': f'{field_name} cannot be empty'
        }), 400
    
    if len(content) > max_length:
        return jsonify({
            'error': 'INPUT_TOO_LONG',
            'message': f'{field_name} exceeds maximum length of {max_length} characters'
        }), 400
    
    return None


@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint with system status."""
    # Cleanup expired sessions
    expired_count = cleanup_expired_sessions()
    
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat(),
        'active_sessions': len(sessions),
        'api_key_configured': bool(config.GOOGLE_API_KEY)
    }), 200


@app.route('/api/v1/parse/resume', methods=['POST'])
def parse_resume():
    """Parse LaTeX resume into structured data.
    
    Request body:
        {
            "latex_content": "\\documentclass{article}..."
        }
    
    Response:
        {
            "raw_latex": "...",
            "plain_text": "...",
            "name": "John Doe",
            "contact": {...},
            "education": [...],
            "experience": [...],
            "skills": [...],
            "projects": [...]
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'latex_content' not in data:
            return jsonify({
                'error': 'INVALID_REQUEST',
                'message': 'latex_content is required'
            }), 400
        
        latex_content = data['latex_content']
        
        # Validate input length
        error = validate_input_length(latex_content, MAX_RESUME_LENGTH, 'Resume')
        if error:
            return error
        
        logger.info(f"Parsing resume ({len(latex_content)} characters)")
        
        # Parse resume
        resume_data = parse_latex_resume(latex_content)
        
        logger.info("Resume parsed successfully")
        return jsonify(resume_data), 200
        
    except Exception as e:
        logger.error(f"Resume parse error: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'RESUME_PARSE_ERROR',
            'message': str(e)
        }), 400


@app.route('/api/v1/parse/job', methods=['POST'])
def parse_job():
    """Parse plain text job description into structured data.
    
    Request body:
        {
            "job_text": "Senior Software Engineer..."
        }
    
    Response:
        {
            "raw_text": "...",
            "title": "Senior Software Engineer",
            "company": "...",
            "requirements": [...],
            "responsibilities": [...],
            "qualifications": [...],
            "skills": [...],
            "experience_level": "senior"
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'job_text' not in data:
            return jsonify({
                'error': 'INVALID_REQUEST',
                'message': 'job_text is required'
            }), 400
        
        job_text = data['job_text']
        
        # Validate input length
        error = validate_input_length(job_text, MAX_JOB_LENGTH, 'Job description')
        if error:
            return error
        
        logger.info(f"Parsing job description ({len(job_text)} characters)")
        
        # Parse job description
        job_data = parse_job_description(job_text)
        
        logger.info("Job description parsed successfully")
        return jsonify(job_data), 200
        
    except Exception as e:
        logger.error(f"Job parse error: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'JOB_PARSE_ERROR',
            'message': str(e)
        }), 400


@app.route('/api/v1/interview/initialize', methods=['POST'])
def initialize_interview():
    """Initialize a new interview session.
    
    Request body:
        {
            "resume_data": {...},
            "job_data": {...},
            "focus_area": "behavioral",
            "adaptive_strategy": true,
            "outcome_prediction": true
        }
    
    Response:
        {
            "session_id": "uuid",
            "strategy": {...},
            "max_turns": 7,
            "current_turn": 1,
            "status": "initialized"
        }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['resume_data', 'job_data', 'focus_area']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': 'INVALID_REQUEST',
                    'message': f'{field} is required'
                }), 400
        
        # Validate focus_area
        valid_focus_areas = ['behavioral', 'technical', 'case', 'mixed']
        if data['focus_area'] not in valid_focus_areas:
            return jsonify({
                'error': 'INVALID_REQUEST',
                'message': f'focus_area must be one of: {", ".join(valid_focus_areas)}'
            }), 400
        
        # Get API key from header
        api_key = request.headers.get('X-API-Key') or config.GOOGLE_API_KEY
        if not api_key:
            return jsonify({
                'error': 'API_KEY_MISSING',
                'message': 'Google API key is required. Set X-API-Key header or GOOGLE_API_KEY environment variable.'
            }), 400
        
        # Create session ID
        session_id = str(uuid.uuid4())
        
        logger.info(f"Initializing interview session: {session_id}")
        
        # Initialize client and orchestrator
        client = Client(api_key=api_key)
        orchestrator = InterviewOrchestrator(client)
        
        # Build enhanced background
        resume_context = format_resume_for_context(data['resume_data'])
        job_context = format_job_for_context(data['job_data'])
        
        enhanced_background = f"""
CANDIDATE RESUME:
{resume_context}

TARGET JOB:
{job_context}
"""
        
        # Initialize session
        orchestrator.initialize_session(
            role=data['job_data'].get('title', 'Position'),
            background=enhanced_background,
            focus_area=data['focus_area']
        )
        
        # Run profiler phase
        profiler_result = orchestrator.run_profiler_phase()
        
        # Store session
        sessions[session_id] = {
            'orchestrator': orchestrator,
            'resume_data': data['resume_data'],
            'job_data': data['job_data'],
            'focus_area': data['focus_area'],
            'adaptive_strategy': data.get('adaptive_strategy', True),
            'outcome_prediction': data.get('outcome_prediction', True),
            'created_at': datetime.utcnow().isoformat(),
            'last_activity': datetime.utcnow().isoformat(),
            'status': 'initialized'
        }
        
        logger.info(f"Interview session initialized successfully: {session_id}")
        
        return jsonify({
            'session_id': session_id,
            'strategy': orchestrator.session_state[state.SESSION_STRATEGY],
            'max_turns': config.MAX_INTERVIEW_TURNS,
            'current_turn': 1,
            'status': 'initialized'
        }), 200
        
    except Exception as e:
        logger.error(f"Interview initialization error: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'INTERVIEW_INIT_ERROR',
            'message': str(e)
        }), 500


@app.route('/api/v1/interview/<session_id>/question', methods=['GET'])
def get_question(session_id: str):
    """Get the next interview question.
    
    Response:
        {
            "question": "Tell me about...",
            "turn_number": 1,
            "competency": "leadership",
            "question_type": "new_competency"
        }
    """
    try:
        session = get_session(session_id)
        if not session:
            return jsonify({
                'error': 'SESSION_NOT_FOUND',
                'message': 'Session not found or expired'
            }), 404
        
        orchestrator = session['orchestrator']
        
        # Generate question
        interviewer_context = {
            "strategy": orchestrator.session_state[state.SESSION_STRATEGY],
            "last_signal": orchestrator.session_state.get(state.LAST_EVALUATOR_SIGNAL, "advance"),
            "conversation_history": orchestrator.session_state[state.CONVERSATION_HISTORY],
            "turn_number": orchestrator.session_state[state.CURRENT_TURN],
            "current_competency": orchestrator.interviewer.get_memory("current_competency", "working"),
        }
        
        interviewer_result = orchestrator.interviewer.process(interviewer_context)
        
        orchestrator.metadata["total_agent_calls"] += 1
        
        # Store current question in session
        session['current_question'] = interviewer_result["question"]
        
        return jsonify({
            'question': interviewer_result["question"],
            'turn_number': orchestrator.session_state[state.CURRENT_TURN],
            'competency': interviewer_result.get("competency", "general"),
            'question_type': interviewer_result.get("question_type", "new_competency")
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'QUESTION_GENERATION_ERROR',
            'message': str(e)
        }), 500


@app.route('/api/v1/interview/<session_id>/answer', methods=['POST'])
def submit_answer(session_id: str):
    """Submit answer and get evaluation.
    
    Request body:
        {
            "answer": "In my previous role..."
        }
    
    Response:
        {
            "evaluation": {...},
            "aggregate_metrics": {...},
            "should_continue": true,
            "adaptive_adjustment": {...},
            "outcome_prediction": {...}
        }
    """
    try:
        session = get_session(session_id)
        if not session:
            return jsonify({
                'error': 'SESSION_NOT_FOUND',
                'message': 'Session not found or expired'
            }), 404
        
        data = request.get_json()
        if not data or 'answer' not in data:
            return jsonify({
                'error': 'INVALID_REQUEST',
                'message': 'answer is required'
            }), 400
        
        answer = data['answer']
        
        # Validate answer length
        error = validate_input_length(answer, MAX_ANSWER_LENGTH, 'Answer')
        if error:
            return error
        
        orchestrator = session['orchestrator']
        question = session.get('current_question', '')
        
        logger.info(f"Processing answer for session {session_id}, turn {orchestrator.session_state[state.CURRENT_TURN]}")
        
        # Record conversation
        state.add_conversation_turn(orchestrator.session_state, question, answer)
        
        # Evaluate answer
        evaluator_context = {
            "question": question,
            "answer": answer,
            "strategy": orchestrator.session_state[state.SESSION_STRATEGY],
            "turn_number": orchestrator.session_state[state.CURRENT_TURN],
            "conversation_history": orchestrator.session_state[state.CONVERSATION_HISTORY],
            "current_competency": orchestrator.interviewer.get_memory("current_competency", "working"),
        }
        
        evaluator_result = orchestrator.evaluator.process(evaluator_context)
        evaluation = evaluator_result["evaluation"]
        
        orchestrator.metadata["total_agent_calls"] += 1
        
        # Store evaluation
        state.append_turn_score(orchestrator.session_state, evaluation)
        orchestrator.session_state[state.LAST_EVALUATOR_SIGNAL] = evaluation["next_move"]
        orchestrator.session_state["aggregate_metrics"] = evaluator_result.get("aggregate_metrics", {})
        
        # Check adaptive strategy
        adaptive_adjustment = {'triggered': False}
        if session.get('adaptive_strategy') and orchestrator.session_state[state.CURRENT_TURN] >= 3:
            orchestrator.enable_adaptive_strategy()
            adaptive_adjustment = {'triggered': True, 'reason': 'Performance-based adjustment'}
        
        # Check outcome prediction
        outcome_prediction = {'available': False}
        if session.get('outcome_prediction') and orchestrator.session_state[state.CURRENT_TURN] == 3:
            prediction = orchestrator.enable_outcome_prediction()
            if prediction:
                outcome_prediction = {
                    'available': True,
                    'outcome': prediction.get('outcome', 'unknown'),
                    'confidence': prediction.get('confidence', 0)
                }
        
        # Determine if should continue
        should_continue = (
            evaluation["next_move"] != "wrap_up" and
            orchestrator.session_state[state.CURRENT_TURN] < config.MAX_INTERVIEW_TURNS
        )
        
        # Increment turn
        state.increment_turn(orchestrator.session_state)
        
        # Update session status and activity
        if not should_continue:
            session['status'] = 'completed'
        session['last_activity'] = datetime.utcnow().isoformat()
        
        logger.info(f"Answer evaluated successfully for session {session_id}")
        
        return jsonify({
            'evaluation': evaluation,
            'aggregate_metrics': evaluator_result.get("aggregate_metrics", {}),
            'should_continue': should_continue,
            'adaptive_adjustment': adaptive_adjustment,
            'outcome_prediction': outcome_prediction
        }), 200
        
    except Exception as e:
        logger.error(f"Answer evaluation error: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'ANSWER_EVALUATION_ERROR',
            'message': str(e)
        }), 500


@app.route('/api/v1/interview/<session_id>/history', methods=['GET'])
def get_conversation_history(session_id: str):
    """Get conversation history.
    
    Response:
        {
            "turns": [...],
            "total_turns": 5
        }
    """
    try:
        session = get_session(session_id)
        if not session:
            return jsonify({
                'error': 'SESSION_NOT_FOUND',
                'message': 'Session not found or expired'
            }), 404
        
        orchestrator = session['orchestrator']
        conversation_history = orchestrator.session_state[state.CONVERSATION_HISTORY]
        
        return jsonify({
            'turns': conversation_history,
            'total_turns': len(conversation_history)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'ERROR',
            'message': str(e)
        }), 500


@app.route('/api/v1/interview/<session_id>/end', methods=['POST'])
def end_interview(session_id: str):
    """End interview early.
    
    Response:
        {
            "status": "completed",
            "total_turns": 5,
            "message": "Interview ended"
        }
    """
    try:
        session = get_session(session_id)
        if not session:
            return jsonify({
                'error': 'SESSION_NOT_FOUND',
                'message': 'Session not found or expired'
            }), 404
        
        orchestrator = session['orchestrator']
        session['status'] = 'completed'
        
        return jsonify({
            'status': 'completed',
            'total_turns': orchestrator.session_state[state.CURRENT_TURN] - 1,
            'message': 'Interview ended successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'ERROR',
            'message': str(e)
        }), 500


@app.route('/api/v1/interview/<session_id>/report', methods=['GET'])
def get_coaching_report(session_id: str):
    """Generate and retrieve coaching report.
    
    Response:
        {
            "report": {...},
            "metadata": {...}
        }
    """
    try:
        session = get_session(session_id)
        if not session:
            return jsonify({
                'error': 'SESSION_NOT_FOUND',
                'message': 'Session not found or expired'
            }), 404
        
        if session['status'] != 'completed':
            return jsonify({
                'error': 'INTERVIEW_NOT_COMPLETE',
                'message': 'Interview must be completed before generating report'
            }), 400
        
        orchestrator = session['orchestrator']
        
        # Generate coaching report
        logger.info(f"Generating coaching report for session {session_id}")
        coach_result = orchestrator.run_coach_phase()
        logger.info(f"Coach result keys: {coach_result.keys() if coach_result else 'None'}")
        
        # Get agent insights
        insights = orchestrator.get_agent_insights()
        logger.info(f"Insights keys: {insights.keys() if insights else 'None'}")
        
        # Build comprehensive report with safe access
        report = {
            'markdown': coach_result.get('report', '') if coach_result else '',
            'summary': {
                'overall_performance': coach_result.get('overall_performance', 'N/A') if coach_result else 'N/A',
                'readiness_level': insights.get('coach', {}).get('benchmark', {}).get('readiness_level', 'N/A') if insights else 'N/A',
                'percentile': insights.get('coach', {}).get('benchmark', {}).get('percentile', 'N/A') if insights else 'N/A'
            },
            'strengths': coach_result.get('strengths', []) if coach_result else [],
            'skill_gaps': insights.get('coach', {}).get('skill_gaps', {}).get('gaps', []) if insights else [],
            'practice_plan': coach_result.get('practice_plan', {}) if coach_result else {},
            'answer_patterns': insights.get('evaluator', {}).get('answer_patterns', {}) if insights else {}
        }
        
        metadata = {
            'total_agent_calls': orchestrator.metadata.get('total_agent_calls', 0),
            'total_turns': orchestrator.session_state[state.CURRENT_TURN] - 1,
            'session_duration': 'N/A'  # Could calculate from timestamps
        }
        
        logger.info(f"Report generated successfully for session {session_id}")
        
        return jsonify({
            'report': report,
            'metadata': metadata
        }), 200
        
    except Exception as e:
        logger.error(f"Report generation error for session {session_id}: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'REPORT_GENERATION_ERROR',
            'message': str(e)
        }), 500


@app.route('/api/v1/interview/<session_id>/status', methods=['GET'])
def get_session_status(session_id: str):
    """Get session status.
    
    Response:
        {
            "session_id": "...",
            "status": "in_progress",
            "current_turn": 3,
            "max_turns": 7,
            "progress_percentage": 42.8,
            "adaptive_strategy_enabled": true,
            "outcome_prediction_enabled": true,
            "interview_complete": false
        }
    """
    try:
        session = get_session(session_id)
        if not session:
            return jsonify({
                'error': 'SESSION_NOT_FOUND',
                'message': 'Session not found or expired'
            }), 404
        
        orchestrator = session['orchestrator']
        current_turn = orchestrator.session_state[state.CURRENT_TURN]
        max_turns = config.MAX_INTERVIEW_TURNS
        
        return jsonify({
            'session_id': session_id,
            'status': session['status'],
            'current_turn': current_turn,
            'max_turns': max_turns,
            'progress_percentage': (current_turn / max_turns) * 100,
            'adaptive_strategy_enabled': session.get('adaptive_strategy', False),
            'outcome_prediction_enabled': session.get('outcome_prediction', False),
            'interview_complete': session['status'] == 'completed'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'ERROR',
            'message': str(e)
        }), 500


if __name__ == '__main__':
    # Check API key
    if not config.GOOGLE_API_KEY:
        print("❌ Error: GOOGLE_API_KEY not found in environment")
        print("   Please set it in your .env file")
        exit(1)
    
    print("\n" + "=" * 60)
    print("🚀 AI Mock Interview Coach - API Server")
    print("=" * 60)
    print(f"\n📡 Server starting on http://localhost:8000")
    print(f"📚 API Base URL: http://localhost:8000/api/v1")
    print(f"\n✅ Ready to accept requests!\n")
    
    # Run server
    app.run(host='0.0.0.0', port=8000, debug=True)
