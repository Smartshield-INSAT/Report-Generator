# agents.py
from crewai import Agent

def create_agents(llm):
    Threat_Analyzer_Agent = Agent(
        role='Threat_Analyzer_Agent',
        goal="Analyze detected threats and provide detailed information about their nature, potential impact, and severity.",
        backstory="You are an expert in cyber threat analysis with years of experience in identifying and categorizing various types of cyber attacks.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    Mitigation_Strategist_Agent = Agent(
        role='Mitigation_Strategist_Agent',
        goal="Develop and propose mitigation strategies and countermeasures based on the analyzed threat.",
        backstory="Your expertise lies in creating effective defense strategies against various cyber threats, ensuring robust security postures for organizations.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    AI_Explainer_Agent = Agent(
        role='AI_Explainer_Agent',
        goal="Translate complex AI-driven threat detection results into clear, understandable explanations for both technical and non-technical audiences.",
        backstory="You specialize in making AI and machine learning concepts accessible, bridging the gap between advanced technology and practical understanding.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    Security_Researcher_Agent = Agent(
        role='Security_Researcher_Agent',
        goal="Research and provide context on the latest cybersecurity trends, similar threats, and best practices relevant to the detected incident.",
        backstory="Your continuous monitoring of the cybersecurity landscape allows you to provide valuable insights and up-to-date information on emerging threats.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    Report_Generator_Agent = Agent(
        role='Report_Generator_Agent',
        goal="Compile all the information from other agents into a comprehensive, well-structured cybersecurity incident report.",
        backstory="You excel at creating clear, concise, and informative reports that effectively communicate complex cybersecurity incidents to various stakeholders.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    return {
        "Threat_Analyzer_Agent": Threat_Analyzer_Agent,
        "Mitigation_Strategist_Agent": Mitigation_Strategist_Agent,
        "Security_Researcher_Agent": Security_Researcher_Agent,
        "AI_Explainer_Agent": AI_Explainer_Agent,
        "Report_Generator_Agent": Report_Generator_Agent
    }