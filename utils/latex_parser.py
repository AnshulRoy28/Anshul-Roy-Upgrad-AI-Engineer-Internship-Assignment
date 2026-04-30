"""LaTeX resume parser."""
import re
from typing import Dict, List, Any
from pylatexenc.latex2text import LatexNodes2Text


def parse_latex_resume(latex_content: str) -> Dict[str, Any]:
    """Parse LaTeX resume into structured data.
    
    Args:
        latex_content: Resume in LaTeX format
        
    Returns:
        Structured resume data
    """
    # Convert LaTeX to plain text
    converter = LatexNodes2Text()
    plain_text = converter.latex_to_text(latex_content)
    
    # Extract structured information
    resume_data = {
        "raw_latex": latex_content,
        "plain_text": plain_text,
        "name": _extract_name(latex_content, plain_text),
        "contact": _extract_contact(plain_text),
        "education": _extract_education(plain_text),
        "experience": _extract_experience(plain_text),
        "skills": _extract_skills(plain_text),
        "projects": _extract_projects(plain_text),
    }
    
    return resume_data


def _extract_name(latex: str, plain: str) -> str:
    """Extract candidate name from resume.
    
    Args:
        latex: LaTeX content
        plain: Plain text content
        
    Returns:
        Candidate name
    """
    # Try to find name in LaTeX commands
    name_patterns = [
        r'\\name\{([^}]+)\}',
        r'\\author\{([^}]+)\}',
        r'\\title\{([^}]+)\}',
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, latex)
        if match:
            return match.group(1).strip()
    
    # Fallback: first line of plain text
    lines = plain.strip().split('\n')
    if lines:
        return lines[0].strip()
    
    return "Candidate"


def _extract_contact(plain: str) -> Dict[str, str]:
    """Extract contact information.
    
    Args:
        plain: Plain text content
        
    Returns:
        Contact information
    """
    contact = {}
    
    # Email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', plain)
    if email_match:
        contact["email"] = email_match.group(0)
    
    # Phone
    phone_match = re.search(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', plain)
    if phone_match:
        contact["phone"] = phone_match.group(0)
    
    # LinkedIn
    linkedin_match = re.search(r'linkedin\.com/in/[\w\-]+', plain)
    if linkedin_match:
        contact["linkedin"] = linkedin_match.group(0)
    
    # GitHub
    github_match = re.search(r'github\.com/[\w\-]+', plain)
    if github_match:
        contact["github"] = github_match.group(0)
    
    return contact


def _extract_education(plain: str) -> List[Dict[str, str]]:
    """Extract education information.
    
    Args:
        plain: Plain text content
        
    Returns:
        List of education entries
    """
    education = []
    
    # Find education section
    edu_section = _extract_section(plain, ["education", "academic"])
    
    if edu_section:
        # Look for degree patterns
        degree_patterns = [
            r'(Bachelor|Master|PhD|B\.S\.|M\.S\.|Ph\.D\.).*?(?=\n\n|\Z)',
            r'(University|College|Institute).*?(?=\n\n|\Z)',
        ]
        
        for pattern in degree_patterns:
            matches = re.finditer(pattern, edu_section, re.IGNORECASE | re.DOTALL)
            for match in matches:
                education.append({
                    "entry": match.group(0).strip()
                })
    
    return education


def _extract_experience(plain: str) -> List[Dict[str, str]]:
    """Extract work experience.
    
    Args:
        plain: Plain text content
        
    Returns:
        List of experience entries
    """
    experience = []
    
    # Find experience section
    exp_section = _extract_section(plain, ["experience", "work", "employment"])
    
    if exp_section:
        # Split by common delimiters
        entries = re.split(r'\n(?=[A-Z][a-z]+ \d{4}|\d{4})', exp_section)
        
        for entry in entries:
            if entry.strip() and len(entry.strip()) > 20:
                experience.append({
                    "entry": entry.strip()
                })
    
    return experience


def _extract_skills(plain: str) -> List[str]:
    """Extract skills.
    
    Args:
        plain: Plain text content
        
    Returns:
        List of skills
    """
    skills = []
    
    # Find skills section
    skills_section = _extract_section(plain, ["skills", "technical skills", "technologies"])
    
    if skills_section:
        # Split by common delimiters
        skill_items = re.split(r'[,;•\n]', skills_section)
        
        for item in skill_items:
            item = item.strip()
            if item and len(item) > 2 and len(item) < 50:
                skills.append(item)
    
    return skills


def _extract_projects(plain: str) -> List[Dict[str, str]]:
    """Extract projects.
    
    Args:
        plain: Plain text content
        
    Returns:
        List of project entries
    """
    projects = []
    
    # Find projects section
    proj_section = _extract_section(plain, ["projects", "personal projects"])
    
    if proj_section:
        # Split by project entries
        entries = re.split(r'\n(?=[A-Z])', proj_section)
        
        for entry in entries:
            if entry.strip() and len(entry.strip()) > 20:
                projects.append({
                    "entry": entry.strip()
                })
    
    return projects


def _extract_section(text: str, section_names: List[str]) -> str:
    """Extract a section from resume text.
    
    Args:
        text: Resume text
        section_names: Possible section names
        
    Returns:
        Section content
    """
    for name in section_names:
        # Try to find section header
        pattern = rf'(?i)^.*{name}.*$'
        match = re.search(pattern, text, re.MULTILINE)
        
        if match:
            start = match.end()
            
            # Find next section or end
            next_section = re.search(
                r'\n[A-Z][A-Z\s]+\n',
                text[start:],
                re.MULTILINE
            )
            
            if next_section:
                end = start + next_section.start()
            else:
                end = len(text)
            
            return text[start:end].strip()
    
    return ""


def format_resume_for_context(resume_data: Dict[str, Any]) -> str:
    """Format parsed resume data for agent context.
    
    Args:
        resume_data: Parsed resume data
        
    Returns:
        Formatted resume string
    """
    sections = []
    
    # Name
    if resume_data.get("name"):
        sections.append(f"Candidate: {resume_data['name']}")
    
    # Contact
    if resume_data.get("contact"):
        contact_items = [f"{k}: {v}" for k, v in resume_data["contact"].items()]
        if contact_items:
            sections.append("Contact: " + ", ".join(contact_items))
    
    # Education
    if resume_data.get("education"):
        sections.append("\nEducation:")
        for edu in resume_data["education"]:
            sections.append(f"  • {edu['entry']}")
    
    # Experience
    if resume_data.get("experience"):
        sections.append("\nExperience:")
        for exp in resume_data["experience"]:
            sections.append(f"  • {exp['entry']}")
    
    # Skills
    if resume_data.get("skills"):
        sections.append("\nSkills:")
        sections.append(f"  {', '.join(resume_data['skills'])}")
    
    # Projects
    if resume_data.get("projects"):
        sections.append("\nProjects:")
        for proj in resume_data["projects"]:
            sections.append(f"  • {proj['entry']}")
    
    return "\n".join(sections)
