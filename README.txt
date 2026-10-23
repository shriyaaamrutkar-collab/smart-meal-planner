SMARTMEAL — CLEAN OFFLINE VERSION

Requirements: Python 3.12 recommended.

Windows setup:
1. Extract this ZIP.
2. Open the inner smartmeal folder in VS Code.
3. Open Terminal in that folder.
4. Create an environment: py -3.12 -m venv .venv
5. Activate it in PowerShell:
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
6. Install packages: python -m pip install -r requirements.txt
7. Start the app: python -m streamlit run app.py

SmartMeal runs locally and uses rule-based logic, not AI or external AI APIs.
Step entries are manual. Health notes are general food-planning information, not medical advice. Follow your clinician's instructions for disease-specific restrictions.
