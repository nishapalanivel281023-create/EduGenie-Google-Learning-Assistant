# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant built around FastAPI and a simple HTML/CSS/JavaScript frontend.

## Features

- Q&A — `/qa`
- Beginner-friendly explanations — `/explain`
- Three-question MCQ quiz generation — `/quiz`
- Educational summarization — `/summarize`
- Beginner-to-advanced learning paths — `/learn/recommendations`
- Health check — `/health`

The project follows the supplied documentation's module structure. Gemini handles the cloud AI features. The LaMini-Flan-T5 explanation model is available as an optional local mode.

## Project structure

```text
EduGenie/
├── main.py
├── gemini_client.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── tests/
    └── test_api.py
```

## 1. Install Python

Use Python 3.10 or newer.

Check:

```bash
python --version
```

On some systems the command is:

```bash
python3 --version
```

## 2. Open the project in VS Code

Open the `EduGenie` folder in VS Code.

## 3. Create a virtual environment

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

When activated, your terminal should show something like `(.venv)`.

## 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Configure Gemini

Create a file named `.env` in the project root.

Copy the contents of `.env.example` into it and replace:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

with your own Gemini API key.

Do not commit `.env` to Git. It is already excluded by `.gitignore`.

The default model is:

```text
GEMINI_MODEL=gemini-2.5-flash
```

If that model is not available for your API account, change the value to a model available to your account.

## 6. Start EduGenie

Run:

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## 7. Test each feature

### Q&A

Choose `Ask a Question` and enter:

```text
What is photosynthesis?
```

### Explanation

Choose `Explain a Topic`:

```text
Explain recursion for a beginner.
```

### Quiz

Choose `Generate Quiz` and paste:

```text
Python is a high-level programming language. It is widely used in
web development, automation, data analysis, and artificial intelligence.
```

EduGenie returns exactly three MCQs with four options each.

### Summary

Paste a longer educational passage.

### Learning path

Enter:

```text
SQL from beginner to advanced
```

## 8. Run automated tests

With the virtual environment active:

```bash
pytest
```

The tests check that the FastAPI app starts, the home page loads, the health endpoint works, and validation rejects an empty question.

## 9. API documentation

FastAPI automatically provides:

```text
http://127.0.0.1:8000/docs
```

and:

```text
http://127.0.0.1:8000/redoc
```

You can test the endpoints directly from Swagger UI.

## Optional: local LaMini explanation model

The supplied project documentation specifies LaMini-Flan-T5-783M for the explanation module.

To use it locally, change `.env`:

```text
USE_LOCAL_EXPLAINER=true
LOCAL_EXPLAINER_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

The first explanation request may download the model from Hugging Face and can require significant disk space/RAM. If the local model cannot load, EduGenie automatically falls back to Gemini.

For the simplest first run, keep:

```text
USE_LOCAL_EXPLAINER=false
```

## Troubleshooting

### `GEMINI_API_KEY is missing`

Make sure `.env` is in the same folder as `main.py` and contains a valid key.

### `ModuleNotFoundError`

Make sure the virtual environment is active, then run:

```bash
pip install -r requirements.txt
```

### Port 8000 is busy

Run:

```bash
uvicorn main:app --reload --port 8001
```

Then open:

```text
http://127.0.0.1:8001
```

### Gemini request/model error

Check the API key and the value of `GEMINI_MODEL`. The model must be available to your Gemini API account.

### Local LaMini is slow

That is expected on CPU-only hardware. Keep `USE_LOCAL_EXPLAINER=false` to use Gemini for explanations.

## Security notes

- Never put the Gemini API key in HTML or JavaScript.
- Keep the key in `.env`.
- `.env` is ignored by Git.
- For production, add authentication, rate limiting, request logging, monitoring, and stronger input/output controls.

## Architecture

```text
Browser
   |
   | POST JSON
   v
FastAPI
   |
   +--> Q&A ------------> Gemini
   |
   +--> Explanation ----> LaMini (optional) -> Gemini fallback
   |
   +--> Quiz -----------> Gemini JSON
   |
   +--> Summary --------> Gemini
   |
   +--> Learning Path --> Gemini
```
