# 🏋️ HealthyFit — Next-Gen AI Healthcare Web Application

> A fully featured healthcare and fitness web application powered by Flask and multiple AI engines (Groq LLaMA, OpenAI GPT), featuring a medicine chatbot, AI report analyzer, bodyweight fitness planner, and a gym workout planner with live YouTube exercise tutorials.

---

## 📸 Preview

<table>
  <thead>
    <tr>
      <th>🤖 FitBuddy AI Chat</th>
      <th>🏋️ Gym Planner</th>
      <th>💊 Medicine Bot</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Premium chat UI with AI-powered fitness advice</td>
      <td>Daily muscle split with inline YouTube video embeds</td>
      <td>Groq-powered medicine info (uses, dosage, side effects)</td>
    </tr>
  </tbody>
</table>

---

## 🚀 Features

### 🤖 AI-Powered Tools

<table>
  <thead>
    <tr>
      <th>Feature</th>
      <th>Engine</th>
      <th>Capability</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>MedBot</strong></td>
      <td>Groq (LLaMA 3.3)</td>
      <td>Comprehensive medicine info — uses, dosage, side effects, precautions</td>
    </tr>
    <tr>
      <td><strong>FitBuddy AI</strong></td>
      <td>Groq (LLaMA 3.3)</td>
      <td>All-rounder fitness, nutrition, and health assistant</td>
    </tr>
    <tr>
      <td><strong>AI Report Analyzer</strong></td>
      <td>Groq (LLaMA 3.3)</td>
      <td>Upload images, PDFs, DOCX, or paste text for medical analysis</td>
    </tr>
    <tr>
      <td><strong>Gym Planner</strong></td>
      <td>Algorithmic</td>
      <td>Daily unique muscle-split plans with live YouTube video tutorials</td>
    </tr>
    <tr>
      <td><strong>Bodyweight Trainer</strong></td>
      <td>Algorithmic</td>
      <td>Personalized no-equipment workout plans based on fitness level</td>
    </tr>
  </tbody>
</table>

### 🏋️ Gym Planner Highlights
- **Daily unique muscle workouts** — every day targets a different muscle group
- **User-selectable exercises per day** — choose 1, 2, 3 or 4 exercises
- **9 muscle groups** — Chest, Back, Legs, Shoulders, Arms, **Triceps, Biceps, Abs, Glutes**
- **Multiple exercise variations** per muscle (3–4 variations each)
- **Inline YouTube video tutorials** — click "Watch Video" and the iframe loads right on the card

### 🔐 Authentication
- Session-based login/register with Flask-Login
- Password hashing with Werkzeug
- Protected routes — all AI tools require login

### 🎨 UI / UX
- Dark glassmorphism theme with 3D particle background (Three.js)
- Fully responsive (Bootstrap 5)
- Animated transitions and hover effects
- Light blue text color system for readability

---

## 🗂️ Project Structure

```
HealthyFit/
├── app.py                  # Main Flask application & all routes
├── config.py               # Environment variable bindings
├── forms.py                # WTForms form definitions
├── models.py               # SQLAlchemy database models
├── init_db.py              # Database initialization script
├── requirements.txt        # Python dependencies
├── .env                    # Secret keys & API keys (not committed)
│
├── utils/
│   ├── ocr_helper.py       # Image/PDF/DOCX text extraction
│   ├── medicine_db.py      # Local medicine database search
│   ├── report_analyzer.py  # Groq-powered medical report analysis
│   ├── fitness_planner.py  # Bodyweight workout plan generator
│   └── gym_planner.py      # Gym workout plan generator
│
├── templates/
│   ├── base.html           # Navigation & page skeleton
│   ├── index.html          # Landing page
│   ├── auth.html           # Login / Register
│   ├── dashboard.html      # User dashboard
│   ├── chatbot.html        # MedBot UI
│   ├── fitbuddy.html       # FitBuddy AI Chat UI
│   ├── report_analyzer.html
│   ├── fitness_trainer.html
│   ├── gym_trainer.html    # Gym planner form
│   ├── gym_plan.html       # Generated plan with video cards
│   └── profile.html
│
└── static/
    ├── css/style.css        # Custom dark theme styles
    ├── js/particles.js      # Three.js 3D background
    └── uploads/             # Uploaded report files
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/HealthyFit.git
cd HealthyFit
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///healthcare.db
OPENAI_API_KEY=your-openai-key
GROQ_API_KEY=your-groq-key
GOOGLE_API_KEY=your-google-key
HUGGINGFACE_API_KEY=your-hf-key
```

### 5. Initialize the database
```bash
python init_db.py
```

### 6. Run the app
```bash
python app.py
```

Open your browser at **http://127.0.0.1:5000**

---

## 🔑 API Keys Required

<table>
  <thead>
    <tr>
      <th>Service</th>
      <th>Purpose</th>
      <th>Get Key</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Groq</strong></td>
      <td>MedBot, FitBuddy, Report Analyzer</td>
      <td><a href="https://console.groq.com">console.groq.com</a></td>
    </tr>
    <tr>
      <td><strong>OpenAI</strong></td>
      <td>Optional fallback for MedBot</td>
      <td><a href="https://platform.openai.com">platform.openai.com</a></td>
    </tr>
    <tr>
      <td><strong>YouTube Data API</strong></td>
      <td>Exercise video tutorials</td>
      <td><a href="https://console.cloud.google.com">console.cloud.google.com</a></td>
    </tr>
  </tbody>
</table>

> 💡 Groq's free tier is generous — it's the primary engine powering all AI features.

---

## 🗃️ Database Models

<table>
  <thead>
    <tr>
      <th>Model</th>
      <th>Fields</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><code>User</code></td><td>id, email, name, password_hash, age, weight, target_weight, body_structure</td></tr>
    <tr><td><code>Medicine</code></td><td>id, name, uses, dosage, side_effects, precautions</td></tr>
    <tr><td><code>Exercise</code></td><td>id, name, muscle_group, equipment, sets_reps, posture_tips</td></tr>
    <tr><td><code>FitnessPlan</code></td><td>id, user_id, plan_json, created_at</td></tr>
    <tr><td><code>GymPlan</code></td><td>id, user_id, plan_json, created_at</td></tr>
    <tr><td><code>Report</code></td><td>id, user_id, filename, analysis_json, created_at</td></tr>
  </tbody>
</table>

---

## 🧩 Key Routes

<table>
  <thead>
    <tr>
      <th>Route</th>
      <th>Method</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><code>/</code></td><td>GET</td><td>Landing page</td></tr>
    <tr><td><code>/login</code></td><td>GET/POST</td><td>User login</td></tr>
    <tr><td><code>/register</code></td><td>GET/POST</td><td>User registration</td></tr>
    <tr><td><code>/dashboard</code></td><td>GET</td><td>User dashboard</td></tr>
    <tr><td><code>/chatbot</code></td><td>GET</td><td>MedBot UI</td></tr>
    <tr><td><code>/chatbot/api</code></td><td>POST</td><td>Groq medicine info API</td></tr>
    <tr><td><code>/fitbuddy</code></td><td>GET</td><td>FitBuddy chat UI</td></tr>
    <tr><td><code>/fitbuddy/api</code></td><td>POST</td><td>Groq fitness chat API</td></tr>
    <tr><td><code>/report-analyzer</code></td><td>GET/POST</td><td>Upload &amp; analyze medical reports</td></tr>
    <tr><td><code>/fitness-trainer</code></td><td>GET/POST</td><td>Generate bodyweight plan</td></tr>
    <tr><td><code>/gym-trainer</code></td><td>GET/POST</td><td>Generate gym plan</td></tr>
    <tr><td><code>/api/exercise/video/&lt;name&gt;</code></td><td>GET</td><td>Fetch YouTube video ID for exercise</td></tr>
  </tbody>
</table>

---

## 📦 Dependencies

```
Flask              Flask-SQLAlchemy     Flask-Login
Flask-WTF          groq                 openai
pytesseract        PyPDF2               python-docx
pdfplumber         python-dotenv        requests
Pillow             anthropic
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 🛡️ Security Notes

- All API keys are loaded from `.env` — **never commit `.env` to version control**
- Passwords are hashed using `werkzeug.security`
- File uploads are validated and size-limited to 16MB
- All AI tool routes are protected with `@login_required`

---

## 🧪 Testing Checklist

| Feature | Test | Expected Result |
|---|---|---|
| Auth | Register + Login | Redirects to dashboard |
| MedBot | Search "Aspirin" | Returns uses, dosage, side effects |
| FitBuddy | Ask "Best leg workout?" | AI responds with exercises |
| Analyzer | Paste medical text | Returns AI summary + recommendation |
| Gym Planner | Select muscles, generate | Plan with Watch Video cards |
| Bodyweight | Select fitness level | Workout plan generated |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m "Add my feature"`
4. Push to branch: `git push origin feature/my-feature`
5. Submit a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

Built with ❤️ using Flask, Groq AI, and Bootstrap 5.
