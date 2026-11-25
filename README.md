
# InsureDesk AI 🛡️

### Intelligent Insurance Complaint Investigation and Customer Support Platform

InsureDesk AI is an AI-powered insurance support platform that helps investigate customer complaints, retrieve relevant policy information, generate investigation reports, and create support tickets automatically.

The project combines Google Gemini with LangGraph to demonstrate an AI-assisted insurance complaint investigation workflow.

## 🚀 Features

- **AI Complaint Investigation:** Uses Google Gemini to analyze customer complaints.
- **Customer Information Lookup:** Retrieves customer and policy details from SQLite.
- **Policy Information Retrieval:** Uses keyword-based matching to find relevant policy sections.
- **Workflow Orchestration:** Uses LangGraph to coordinate customer lookup, AI investigation, and ticket creation.
- **Automatic Ticket Creation:** Stores complaint details, category, priority, and investigation report.
- **Dashboard:** Displays ticket statistics and recent customer complaints.
- **Ticket Management:** Displays previously created support tickets.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Google Gemini | AI-powered investigation |
| LangGraph | Workflow orchestration |
| Streamlit | User interface |
| SQLite | Database |
| python-dotenv | Environment configuration |

## 🏗️ System Architecture

```text
Customer Complaint
        |
        v
Customer Lookup
        |
        v
Policy Information Retrieval
        |
        v
Google Gemini Investigation
        |
        v
Investigation Report
        |
        v
Ticket Classification
        |
        v
SQLite Ticket Storage
        |
        v
Streamlit Dashboard
```

## 📁 Project Structure

```text
InsureDesk-AI/
│
├── app.py
├── agents.py
├── workflow.py
├── database.py
├── policy_data.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Sanika36/InsureDesk-AI.git
cd InsureDesk-AI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Gemini API Key

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

Never upload your `.env` file or expose your API key.

### 6. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal.

## 🧪 Sample Demonstration

The project includes synthetic customer and insurance policy records for demonstration.

Example complaint:

"My health insurance premium increased from 12000 to 16000. Please investigate."

The system retrieves relevant policy information, generates an AI investigation report, identifies whether human escalation is required, and creates a support ticket.

## ⚠️ Current Limitations

- Uses synthetic demonstration customer and policy records.
- Policy retrieval uses keyword matching rather than vector-based semantic search.
- Ticket classification and priority assignment use rule-based logic.
- Does not connect to real insurance company systems.
- AI-generated findings require human verification.

This project is a prototype for demonstrating AI-assisted insurance operations. It does not make binding insurance or claim decisions.

## 🔮 Future Enhancements

- Semantic policy retrieval using vector databases.
- PDF policy document processing.
- User authentication and role-based access.
- Advanced ticket filtering and status management.
- Integration with real insurance APIs.
- Improved automated testing and monitoring.

## 👩‍💻 Author

**Sanika Naringe**

GitHub: https://github.com/Sanika36

---

*Built as an academic project to explore AI-assisted insurance complaint investigation and workflow automation.*
