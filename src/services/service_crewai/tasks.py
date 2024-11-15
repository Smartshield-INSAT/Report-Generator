from crewai import Task

def create_tasks(agents, detected_threat, threat_data):
    task_analyze_threat = Task(
        description=f"""
        Analyze the detected threat: {detected_threat}
        Threat Data: {threat_data}

        1. Define the threat and Classify it.
        2. Evaluate impact on confidentiality, integrity, and availability.
        3. Identify key indicators in the data.

        Use only the provided data.
        """,
        agent=agents["Threat_Analyzer_Agent"],
        expected_output="""
        - Threat Definition and classification.
        - Impact assessment.
        - Key indicators from the data.
        """
    )

    task_develop_mitigation = Task(
        description=f"""
        Develop a mitigation plan for the threat: {detected_threat}

        1. Provide short-term and long-term mitigation steps.
        2. Create a concise incident response playbook.

        Ensure all recommendations are very specific to this threat.
        """,
        agent=agents["Mitigation_Strategist_Agent"],
        expected_output="""
        - Short-term and long-term mitigation steps
        - Incident response playbook (bullet points)
        - Justification for each major recommendation
        """,
        context=[task_analyze_threat]
    )

    task_generate_report = Task(
        description=f"""
        Create a comprehensive incident report for: {detected_threat} based on the analysis and mitigation plan.
        Ensure consistency across sections.
        """,
        agent=agents["Report_Generator_Agent"],
        expected_output="""
        A structured report with:
        1. Executive Summary
        2. Threat Analysis
        3. Impact Assessment
        4. Mitigation Strategy
        5. Conclusions

        The report should be factual, consistent, and actionable.
        """,
        context=[task_analyze_threat, task_develop_mitigation]
    )

    return [
        task_analyze_threat,
        task_develop_mitigation,
        task_generate_report
    ]