# AI-Powered-Automatic-Test-Case-Creation


# 🧪 Automatic Test Case Generation using chat GPT and Streamlit Interface

A powerful Streamlit-based application that automatically generates **unit test cases** from user-uploaded code files using **LLMs (OpenAI / Gemini)**. Supports multiple file formats and user authentication with persistent test history.

---

## 🚀 Features

- ✅ Upload code files (`.py`, `.txt`, `.docx`, `.pdf`)
- 🤖 Auto-generate test cases using LLMs (OpenAI or Gemini 1.5 Flash)
- 🔒 User signup/login system
- 🧠 Chat-based interface (optional)
- 🗂️ Persistent user-wise storage of test cases
- 📄 View and download test cases
- 🌍 Optional multilingual support

---

## 🧰 Prerequisites

| Tool/Library         | Purpose                         |
|----------------------|----------------------------------|
| Python ≥ 3.10        | Core runtime                     |
| pip                  | Python package manager           |
| Git                  | Version control                  |
| FFmpeg (Optional)    | Video frame extraction           |
| Tesseract OCR        | Image-to-text (optional)         |
| OpenAI/Gemini API    | LLM backend                      |
| virtualenv (optional)| Recommended for isolation        |

---

## 📦 Installation

1. **Clone the Repository**
```bash
git clone https://github.com/your-username/test_case_generator.git
cd test_case_generator
```

2. **Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

3. **Install Requirements**
```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file at the root of the project:

```env
OPENAI_API_KEY=your_openai_api_key_here
# or
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 🧪 Running the App

```bash
streamlit run app.py
```

### 📋 UI Navigation

- **Signup/Login** – User registration and authentication
- **Dashboard** – Welcome message and user info
- **Upload a Program** – Upload code and generate test cases
- **View Test Cases** – See your generated tests

---

## 🗂 Folder Structure

```plaintext
test_case_generator/
│
├── app.py                    # Main Streamlit app
├── requirements.txt          # Python dependencies
├── .env                      # API keys
├── data.json                 # User + test case data
│
├── modules/
│   ├── file_parser.py        # File/text extraction logic
│   ├── code_analyzer.py      # LLM interaction + prompt logic
│   ├── test_storage.py       # Save/load test cases
│   └── user_auth.py          # Signup/login management
```

---

## 🧪 Sample Supported Inputs

| File Type | Function |
|-----------|----------|
| `.py`     | Python program input |
| `.txt`    | Plain code/script |
| `.docx`   | Word code file |
| `.pdf`    | Embedded code blocks |
| `.jpg/.png` | (Optional OCR support) |

---

## 📚 Example Programs

You can test the app with sample programs like:

- [x] Prime Number Checker
- [x] Find Greatest of Three Numbers
- [x] Two Sum Problem (JS style)

---

## 💡 Future Enhancements

- Export to `.docx` / `.json`
- Test execution engine
- Frontend unit test coverage metrics
- REST API version

---

## 👨‍💻 Contributing

1. Fork the repo
2. Create a new branch (`git checkout -b feature/feature-name`)
3. Commit your changes
4. Push to the branch (`git push origin feature-name`)
5. Open a pull request

---

## 📄 License

This project is licensed under MIT License.

---

## 🙏 Acknowledgements

This project wouldn't have been possible without the contributions and support from the following:

- **[OpenAI](https://openai.com/)** – For providing access to powerful language models like GPT-3.5 for generating high-quality test cases.
- **[Google Gemini](https://deepmind.google/technologies/gemini/)** – For offering multi-modal AI capabilities (used optionally).
- **[Streamlit](https://streamlit.io/)** – For the elegant and easy-to-use frontend framework enabling rapid web app development.
- **[FAISS](https://github.com/facebookresearch/faiss)** – For enabling efficient similarity search and retrieval for embedding chunks.
