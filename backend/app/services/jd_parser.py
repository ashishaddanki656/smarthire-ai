"""
JD (Job Description) Parser service.
Extracts structured information from job descriptions using regex and NLP patterns.
"""

import re
from typing import Dict, List, Optional
from app.utils.logger import get_logger

logger = get_logger("JDParser")


class JDParser:
    """
    Parses job descriptions and extracts key information:
    - Role/Title
    - Required skills
    - Experience level
    - Education level
    - Seniority level
    - Certifications
    """

    # Common tech skills to extract
    TECH_SKILLS = [
        "Python", "Java", "JavaScript", "TypeScript", "Go", "Rust", "C++", "C#",
        "FastAPI", "Django", "Flask", "Spring", "React", "Vue", "Angular",
        "Docker", "Kubernetes", "AWS", "GCP", "Azure", "Terraform",
        "PostgreSQL", "MongoDB", "Redis", "MySQL", "Cassandra",
        "GraphQL", "REST", "gRPC", "Microservices", "Serverless",
        "Machine Learning", "TensorFlow", "PyTorch", "Keras", "Pandas", "NumPy",
        "SQL", "NoSQL", "RDBMS", "Elasticsearch", "Apache", "Spark",
        "Git", "Jenkins", "GitLab", "CI/CD", "DevOps", "Linux", "Windows"
    ]

    # Seniority levels
    SENIORITY_KEYWORDS = {
        "Junior": ["junior", "entry-level", "0-2 years", "fresher"],
        "Mid": ["mid-level", "3-5 years", "intermediate"],
        "Senior": ["senior", "5+ years", "lead", "principal", "expert"],
        "Manager": ["manager", "lead", "director", "head"]
    }

    # Education levels
    EDUCATION_KEYWORDS = {
        "High School": ["high school", "12th", "secondary"],
        "Diploma": ["diploma", "certification"],
        "BTech": ["btech", "b.tech", "bachelor", "engineering"],
        "Master": ["master", "m.tech", "mtech", "mba"],
        "PhD": ["phd", "doctorate", "doctoral"]
    }

    @staticmethod
    def parse_jd(jd_text: str) -> Dict:
        """Parse job description and extract structured information."""
        try:
            logger.info("Starting JD parsing...")

            role = JDParser._extract_role(jd_text)
            skills = JDParser._extract_skills(jd_text)
            experience = JDParser._extract_experience(jd_text)
            education = JDParser._extract_education(jd_text)
            seniority = JDParser._extract_seniority(jd_text)
            certifications = JDParser._extract_certifications(jd_text)

            parsed_jd = {
                "role": role,
                "skills": skills,
                "experience": experience,
                "education": education,
                "seniority": seniority,
                "certifications": certifications
            }

            logger.info(f"JD parsing completed. Found {len(skills)} skills")
            return parsed_jd

        except Exception as e:
            logger.error(f"Error parsing JD: {str(e)}")
            raise

    @staticmethod
    def _extract_role(jd_text: str) -> str:
        """Extract job role/title from JD."""
        patterns = [
            r"(?:Position|Role|Title):\s*([^\n]+)",
            r"^([^,\n]*?(?:Engineer|Developer|Manager|Analyst|Specialist)[^,\n]*)",
        ]

        for pattern in patterns:
            match = re.search(pattern, jd_text, re.IGNORECASE | re.MULTILINE)
            if match:
                role = match.group(1).strip()
                logger.debug(f"Extracted role: {role}")
                return role

        first_line = jd_text.split('\n')[0].strip()
        if len(first_line) > 10:
            return first_line[:100]

        return "Backend Engineer"

    @staticmethod
    def _extract_skills(jd_text: str) -> List[str]:
        """Extract technical skills from JD."""
        skills = []
        jd_lower = jd_text.lower()

        for skill in JDParser.TECH_SKILLS:
            if skill.lower() in jd_lower:
                skills.append(skill)

        logger.debug(f"Extracted skills: {skills}")
        return list(set(skills))

    @staticmethod
    def _extract_experience(jd_text: str) -> int:
        """Extract years of experience required."""
        if not jd_text or not jd_text.strip():
            return 0

        patterns = [
            r"(\d+)\+\s*(?:years|yrs)",
            r"(\d+)\s*[-]\s*(\d+)\s*(?:years|yrs)",
            r"(\d+)\s*(?:years|yrs).*?(?:experience|exp)",
            r"(?:experience|exp).*?(\d+)\s*(?:years|yrs)",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, jd_text, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], tuple):
                    exp = int(matches[0][0])
                else:
                    exp = int(matches[0])
                logger.debug(f"Extracted experience: {exp} years")
                return exp

        logger.debug("Experience not found, defaulting to 3")
        return 3

    @staticmethod
    def _extract_education(jd_text: str) -> str:
        """Extract education level required."""
        jd_lower = jd_text.lower()

        for education, keywords in JDParser.EDUCATION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in jd_lower:
                    logger.debug(f"Extracted education: {education}")
                    return education

        logger.debug("Education not found, defaulting to BTech")
        return "BTech"

    @staticmethod
    def _extract_seniority(jd_text: str) -> str:
        """Extract seniority level."""
        jd_lower = jd_text.lower()

        for seniority, keywords in JDParser.SENIORITY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in jd_lower:
                    logger.debug(f"Extracted seniority: {seniority}")
                    return seniority

        logger.debug("Seniority not found, defaulting to Mid")
        return "Mid"

    @staticmethod
    def _extract_certifications(jd_text: str) -> List[str]:
        """Extract required certifications."""
        certifications = []
        cert_patterns = [
            r"(?:AWS|GCP|Azure) Certified[^,\n]*",
            r"Kubernetes.*?certification",
            r"Docker.*?certification",
        ]

        for pattern in cert_patterns:
            matches = re.findall(pattern, jd_text, re.IGNORECASE)
            certifications.extend(matches)

        logger.debug(f"Extracted certifications: {certifications}")
        return certifications


def parse_jd(jd_text: str) -> Dict:
    """Parse job description text."""
    return JDParser.parse_jd(jd_text)
