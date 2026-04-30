"""Job description parser."""
import re
from typing import Dict, List, Any


def parse_job_description(job_text: str) -> Dict[str, Any]:
    """Parse job description into structured data.
    
    Args:
        job_text: Job description in plain text
        
    Returns:
        Structured job data
    """
    job_data = {
        "raw_text": job_text,
        "title": _extract_job_title(job_text),
        "company": _extract_company(job_text),
        "requirements": _extract_requirements(job_text),
        "responsibilities": _extract_responsibilities(job_text),
        "qualifications": _extract_qualifications(job_text),
        "skills": _extract_required_skills(job_text),
        "experience_level": _extract_experience_level(job_text),
    }
    
    return job_data


def _extract_job_title(text: str) -> str:
    """Extract job title.
    
    Args:
        text: Job description text
        
    Returns:
        Job title
    """
    # Common patterns for job titles
    patterns = [
        r'(?i)^.*?(position|role|title):\s*(.+?)(?:\n|$)',
        r'(?i)^(.+?)\s*(?:position|role)(?:\n|$)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            title = match.group(2) if match.lastindex >= 2 else match.group(1)
            return title.strip()
    
    # Fallback: first line
    lines = text.strip().split('\n')
    if lines:
        return lines[0].strip()
    
    return "Position"


def _extract_company(text: str) -> str:
    """Extract company name.
    
    Args:
        text: Job description text
        
    Returns:
        Company name
    """
    patterns = [
        r'(?i)company:\s*(.+?)(?:\n|$)',
        r'(?i)at\s+([A-Z][a-zA-Z\s&]+?)(?:\n|,)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    
    return "Company"


def _extract_requirements(text: str) -> List[str]:
    """Extract job requirements.
    
    Args:
        text: Job description text
        
    Returns:
        List of requirements
    """
    return _extract_bulleted_section(
        text,
        ["requirements", "required", "must have"]
    )


def _extract_responsibilities(text: str) -> List[str]:
    """Extract job responsibilities.
    
    Args:
        text: Job description text
        
    Returns:
        List of responsibilities
    """
    return _extract_bulleted_section(
        text,
        ["responsibilities", "you will", "duties"]
    )


def _extract_qualifications(text: str) -> List[str]:
    """Extract qualifications.
    
    Args:
        text: Job description text
        
    Returns:
        List of qualifications
    """
    return _extract_bulleted_section(
        text,
        ["qualifications", "preferred", "nice to have"]
    )


def _extract_required_skills(text: str) -> List[str]:
    """Extract required skills.
    
    Args:
        text: Job description text
        
    Returns:
        List of skills
    """
    skills = []
    
    # Common technical skills patterns
    tech_patterns = [
        r'\b(Python|Java|JavaScript|TypeScript|C\+\+|Go|Rust|Ruby)\b',
        r'\b(React|Angular|Vue|Node\.js|Django|Flask|Spring)\b',
        r'\b(AWS|Azure|GCP|Docker|Kubernetes|Jenkins)\b',
        r'\b(SQL|NoSQL|MongoDB|PostgreSQL|MySQL|Redis)\b',
        r'\b(Git|CI/CD|Agile|Scrum|REST|GraphQL)\b',
    ]
    
    for pattern in tech_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            skill = match.group(0)
            if skill not in skills:
                skills.append(skill)
    
    return skills


def _extract_experience_level(text: str) -> str:
    """Extract experience level.
    
    Args:
        text: Job description text
        
    Returns:
        Experience level
    """
    text_lower = text.lower()
    
    if any(term in text_lower for term in ["entry level", "junior", "0-2 years"]):
        return "entry"
    elif any(term in text_lower for term in ["senior", "lead", "principal", "5+ years", "7+ years"]):
        return "senior"
    elif any(term in text_lower for term in ["mid level", "intermediate", "2-5 years", "3-5 years"]):
        return "mid"
    elif any(term in text_lower for term in ["intern", "internship"]):
        return "intern"
    
    return "mid"  # Default


def _extract_bulleted_section(text: str, section_names: List[str]) -> List[str]:
    """Extract bulleted items from a section.
    
    Args:
        text: Job description text
        section_names: Possible section names
        
    Returns:
        List of items
    """
    items = []
    
    for name in section_names:
        # Find section
        pattern = rf'(?i)^.*{name}.*$'
        match = re.search(pattern, text, re.MULTILINE)
        
        if match:
            start = match.end()
            
            # Find next section or end
            next_section = re.search(
                r'\n[A-Z][A-Z\s]+:?\n',
                text[start:],
                re.MULTILINE
            )
            
            if next_section:
                end = start + next_section.start()
            else:
                end = len(text)
            
            section_text = text[start:end]
            
            # Extract bulleted items
            bullet_patterns = [
                r'^\s*[•\-\*]\s*(.+?)$',
                r'^\s*\d+\.\s*(.+?)$',
            ]
            
            for bullet_pattern in bullet_patterns:
                matches = re.finditer(bullet_pattern, section_text, re.MULTILINE)
                for match in matches:
                    item = match.group(1).strip()
                    if item and len(item) > 10:
                        items.append(item)
            
            if items:
                break
    
    return items


def format_job_for_context(job_data: Dict[str, Any]) -> str:
    """Format parsed job data for agent context.
    
    Args:
        job_data: Parsed job data
        
    Returns:
        Formatted job description string
    """
    sections = []
    
    # Title and Company
    sections.append(f"Position: {job_data.get('title', 'N/A')}")
    sections.append(f"Company: {job_data.get('company', 'N/A')}")
    sections.append(f"Experience Level: {job_data.get('experience_level', 'N/A')}")
    
    # Requirements
    if job_data.get("requirements"):
        sections.append("\nRequirements:")
        for req in job_data["requirements"][:5]:  # Limit to top 5
            sections.append(f"  • {req}")
    
    # Responsibilities
    if job_data.get("responsibilities"):
        sections.append("\nResponsibilities:")
        for resp in job_data["responsibilities"][:5]:  # Limit to top 5
            sections.append(f"  • {resp}")
    
    # Skills
    if job_data.get("skills"):
        sections.append("\nRequired Skills:")
        sections.append(f"  {', '.join(job_data['skills'])}")
    
    # Qualifications
    if job_data.get("qualifications"):
        sections.append("\nPreferred Qualifications:")
        for qual in job_data["qualifications"][:3]:  # Limit to top 3
            sections.append(f"  • {qual}")
    
    return "\n".join(sections)
