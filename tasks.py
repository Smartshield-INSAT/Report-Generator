from crewai import Task

def create_tasks(agents, detected_threat, threat_data):
    task_analyze_threat = Task(
        description=f"""
        Analyze the detected threat: {detected_threat} using provided threat data.

        **Threat Detection Data:** {threat_data}

        1. **Classify the threat** using frameworks like MITRE ATT&CK.  
        2. **Evaluate severity** with metrics based on data insights.  
        3. **Impact Assessment:** Assess the impact on confidentiality, integrity, and availability.  
        4. **Data Analysis:** 
           - Identify key indicators leading to detection.
           - Verify reliability and confidence of detection.
           - Detect patterns hinting at attacker tactics or persistence mechanisms.
        5. **Verify Detection:** Identify false positives (if any) using evidence from the data.

        **Expected Output:**  
        A precise threat analysis focused on taxonomy, severity, and impact with supporting evidence from the provided data.
        """,
        agent=agents["Threat_Analyzer_Agent"],
        expected_output="A concise threat analysis with taxonomy, severity, and impact validated through provided data."
    )

    task_develop_mitigation = Task(
        description=f"""
        Develop a mitigation plan based on the analysis of {detected_threat}.

        **Input Data:** {threat_data}  

        1. **Immediate Containment:** Suggest quick actions to limit impact.  
        2. **Mitigation Plan:**  
           - **Short-term:** Tactical responses to limit further damage.  
           - **Medium-term:** Strategic improvements to existing defenses.  
           - **Long-term:** Architectural changes for future resilience.  
        3. **Security Controls:** Reference NIST SP 800-53 or CIS Controls.  
        4. **Incident Response:** Create a playbook specific to the threat scenario.  
        5. **Threat Hunting:** Define procedures to detect any persistence or lateral movement.

        **Expected Output:**  
        A prioritized, actionable mitigation strategy aligned with the analysis and based on industry standards.
        """,
        agent=agents["Mitigation_Strategist_Agent"],
        expected_output="A focused mitigation strategy with actionable, prioritized recommendations."
    )

    task_research_context = Task(
        description=f"""
        Research the broader threat landscape for {detected_threat}.  

        1. **Threat Actors:** Identify any groups using similar tactics.  
        2. **Relevant Campaigns:** Investigate campaigns related to this threat.  
        3. **Zero-day Vulnerabilities:** Check for new vulnerabilities related to the threat.  
        4. **Incident Reports:** Summarize recent incidents with similar threats.  
        5. **Defensive Strategies:** Research defensive measures against this type of threat.  
        6. **Compliance:** Analyze potential regulatory implications.

        **Expected Output:**  
        A brief threat intelligence report situating the detected threat within the broader cybersecurity landscape.
        """,
        agent=agents["Security_Researcher_Agent"],
        expected_output="A concise threat intelligence briefing with relevant actors, incidents, and defensive strategies."
    )

    task_explain_ai_detection = Task(
        description=f"""
        Explain the AI-driven detection process for {detected_threat}.  

        **Detection Data:** {threat_data}  

        1. **Model Architecture:** Brief on the algorithms and model used.  
        2. **Feature Analysis:** Explain which features in {threat_data} were most influential.  
        3. **Decision Process:**  
           - Key decision points and confidence scores.  
           - Thresholds or ensemble techniques applied.  
        4. **Limitations:** Highlight any biases or blind spots in the detection system.  
        5. **Performance Comparison:** Compare AI with traditional detection methods.  
        6. **Improvements:** Suggest data or methods to enhance detection further.

        **Expected Output:**  
        A clear explanation of the detection process focused on the role of data and model architecture.
        """,
        agent=agents["AI_Explainer_Agent"],
        expected_output="A technical but clear explanation of the AI detection process using the provided threat data."
    )

    task_generate_report = Task(
        description=f"""
        Generate a professional incident report for {detected_threat}.

        **Data-Driven Inputs:** {threat_data}  

        1. **Executive Summary:** Overview of the threat, impact, and recommendations.  
        2. **Threat Analysis:** Key insights from the threat analysis.  
        3. **Impact Assessment:** Current and potential business impacts.  
        4. **Mitigation Strategy:** Key elements from the proposed strategy.  
        5. **Threat Intelligence:** Broader threat landscape insights.  
        6. **Lessons Learned:** Key takeaways and future improvements.  
        7. **Appendices:** Logs, IOCs, and AI detection details.

        **Expected Output:**  
        A concise, professional report for executive audiences, based on structured data analysis and findings.
        """,
        agent=agents["Report_Generator_Agent"],
        expected_output="An executive-level incident report summarizing all aspects of the threat and mitigation efforts."
    )

    return [
        task_analyze_threat,
        task_develop_mitigation,
        task_research_context,
        task_explain_ai_detection,
        task_generate_report
    ]
