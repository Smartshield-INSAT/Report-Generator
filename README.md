# Smartshield Report Generator

This repository implements a Cybersecurity Threat agentic workflow that generates a report for cybersecurity professionals using the CrewAI framework and Streamlit for the user interface. The agents helps analyze detected cybersecurity threats by providing detailed analysis, forensic investigation, mitigation strategies, and generating comprehensive reports.

## Features

- Threat analysis using multiple AI agents
- CSV data upload for threat information
- Integration with Groq API for language model processing
- Customizable model selection
- Comprehensive report generation

## Prerequisites

- Python 3.7+
- Groq API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Smartshield-INSAT/Report-Generator.git
   cd Report-Generator
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your Groq API key:
   ```
   GROQ_API_KEY = your_groq_api_key_here
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Use the interface to:
   - Select a language model
   - Input a description of the detected threat
   - Upload a CSV file containing threat data
   - View the analysis and generated report

## Project Structure

- `app.py`: Main Streamlit application
- `agents.py`: Defines the AI agents used in the analysis
- `tasks.py`: Defines the tasks performed by the agents
- `requirements.txt`: Lists all Python dependencies

## Agents

The project uses the following AI agents:

1. Threat Analyzer Agent
2. Mitigation Strategist Agent
3. AI Explainer Agent
4. Security Researcher Agent
5. Report Generator Agent

Each agent has a specific role in analyzing and responding to the detected threat.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Used Tools and Frameworks

- CrewAI framework
- Streamlit
- Groq API
