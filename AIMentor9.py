# ✅ Full AI Mentor App - PART 1 (Base UI + Core Features + Realtime API Setup)
import os
import subprocess
import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# ✅ Load API Key
openrouter_api_key = st.secrets.get("OPENROUTER_API_KEY", None)
if not openrouter_api_key:
    from dotenv import load_dotenv
    load_dotenv()
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
if not openrouter_api_key:
    st.error("❌ OPENROUTER_API_KEY not found!")
    st.stop()

# ✅ Initialize Model
model = ChatOpenAI(
    model_name="mistralai/mistral-7b-instruct:free",
    temperature=0.5,
    max_tokens=300,
    openai_api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1"
)

# ✅ Page Setup
st.set_page_config(page_title="Quality Thought AI Mentor", page_icon="🧠", layout="wide")

# ✅ Theme Selector
with st.sidebar:
    st.markdown("### 🎨 Select Theme")
    selected_theme = st.selectbox(
        "Choose a style:",
        ["Light", "Dark", "Solarized", "Mint", "Coral"],
        index=0
    )
    st.markdown("---")

# ✅ Theme Styles Dictionary
themes = {
    "Light": {"bg": "#ffffff", "text": "#000000", "button": "#f0f0f0"},
    "Dark": {"bg": "#1e1e1e", "text": "#ffffff", "button": "#333333"},
    "Solarized": {"bg": "#fdf6e3", "text": "#657b83", "button": "#eee8d5"},
    "Mint": {"bg": "#eaffea", "text": "#004d00", "button": "#ccffcc"},
    "Coral": {"bg": "#fff0f0", "text": "#ff5e57", "button": "#ffd6d6"}
}
theme = themes[selected_theme]

# ✅ Inject Theme CSS
st.markdown(f"""
    <style>
    body, .main {{
        background-color: {theme['bg']};
        color: {theme['text']};
        font-family: 'Segoe UI', sans-serif;
    }}
    .stButton>button {{
        background-color: {theme['button']};
        color: {theme['text']};
        border-radius: 12px;
        font-size: 18px;
        padding: 10px;
        transition: 0.3s;
        width: 100%;
    }}
    .stButton>button:hover {{
        background-color: #8B0000 !important;
        color: white !important;
        transform: scale(1.03);
    }}
    .stTextInput>div>div>input, .stSelectbox>div>div>div>div {{
        background-color: {theme['button']};
        color: {theme['text']};
    }}
    .welcome-box {{
        background: linear-gradient(to right, #ffecd2, #fcb69f);
        padding: 20px;
        border-radius: 15px;
        animation: fadeIn 1.5s ease-in-out;
        text-align: center;
        color: black;
        margin-top: 0;
    }}
    @keyframes fadeIn {{ from {{opacity: 0;}} to {{opacity: 1;}} }}
    </style>
""", unsafe_allow_html=True)

# ✅ Welcome Box
st.markdown("""
<div class='welcome-box'>
    <h1>Welcome to Quality Thought AI Mentor 🧠</h1>
    <p>Your all-in-one AI mentor for Programming, Cloud, and Data Tech.</p>
</div>
""", unsafe_allow_html=True)

# ✅ Define Modules
modules = [
    ("Python", "🐍"), ("SQL", "📓"), ("Java", "☕"), ("C++", "💻"),
    ("JavaScript", "🔨"), ("HTML/CSS", "🌐"), ("TypeScript", "🟪"), ("Rust", "🦀"),
    ("Go", "🐹"), ("Kotlin", "🟩"), ("R Programming", "📊"),
    ("Numpy", "📐"), ("Pandas", "📊"), ("Scikit-learn", "🔬"),
    ("Statistics", "📈"), ("Machine Learning", "🤖"), ("Deep Learning", "🧠"),
    ("Data Structures", "📒"), ("Algorithms", "🔍"), ("System Design", "🏗️"),
    ("Linux", "🐧"), ("DevOps", "⚙️"), ("Git & GitHub", "🔧"),
    ("AWS", "☁️"), ("Azure", "🔷"), ("GCP", "☁️"), ("Terraform", "🌍"), ("Docker", "🐳"),
    ("HR Questions", "🧾"), ("Resume Tips", "📄"), ("Behavioral Rounds", "🧠"),
    ("Interview Prep", "🎯")
]

# ✅ Session State Init
if 'mentor_type' not in st.session_state:
    st.session_state.mentor_type = None
    st.session_state.code_input = ""

# ✅ Sidebar for Module Selection
st.sidebar.title("📚 Select a Module")
for module, emoji in modules:
    if st.sidebar.button(f"{emoji} {module}"):
        st.session_state.mentor_type = module
        st.session_state.code_input = ""
# ✅ Main Interaction Area
if st.session_state.mentor_type:
    st.subheader(f"{st.session_state.mentor_type} Mentor 🧠")

    experience = st.slider("Your experience (in years):", 0, 10, 1)
    lang = st.selectbox("Select Interface Language", ["English", "Telugu", "Hindi", "Tamil", "Kannada", "Malayalam"], index=0)

    default_templates = {
        "Python": "print('Hello, World!')",
        "Java": "public class Main { public static void main(String[] args) { System.out.println(\"Hello World\"); } }",
        "C++": "#include<iostream>\nusing namespace std;\nint main() { cout << \"Hello World\"; return 0; }",
        "SQL": "SELECT * FROM your_table;",
        "JavaScript": "console.log('Hello, World!');"
    }

    template = default_templates.get(st.session_state.mentor_type, "")
    code_area = st.text_area("Ask a question or write code to run:", value=st.session_state.code_input or template, height=150)
    st.session_state.code_input = code_area

    output_container = st.empty()

    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            f"You are a helpful and experienced {st.session_state.mentor_type.upper()} mentor assisting a user with {experience} years experience. Reply in {lang}."
        ),
        HumanMessagePromptTemplate.from_template("{question}")
    ])

    col1, col2, col3 = st.columns(3)

    # 🚀 Ask Mentor
    with col1:
        if st.button("🚀 Ask Mentor"):
            if code_area:
                try:
                    messages = prompt.format_messages(question=code_area)
                    response = model.invoke(messages)
                    output_container.markdown(f"**👤 You:** {code_area}")
                    output_container.markdown(f"**🧠 Mentor:** {response.content}")
                except Exception as e:
                    output_container.error(f"❌ Error: {str(e)}")
            else:
                output_container.warning("⚠️ Enter a question or code first.")

    # 💻 Run Code (for specific languages)
    with col2:
        if st.button("💻 Run Code"):
            if st.session_state.mentor_type in ["Python", "Java", "C++"] and code_area:
                try:
                    with open("temp_code.txt", "w") as f:
                        f.write(code_area)

                    if st.session_state.mentor_type == "Python":
                        result = subprocess.run(["python", "temp_code.txt"], capture_output=True, text=True)
                    elif st.session_state.mentor_type == "C++":
                        subprocess.run(["g++", "temp_code.txt", "-o", "temp.out"], check=True)
                        result = subprocess.run(["./temp.out"], capture_output=True, text=True)
                    elif st.session_state.mentor_type == "Java":
                        with open("Main.java", "w") as f:
                            f.write(code_area)
                        subprocess.run(["javac", "Main.java"], check=True)
                        result = subprocess.run(["java", "Main"], capture_output=True, text=True)

                    output_container.code(result.stdout or result.stderr)
                except Exception as e:
                    output_container.error(f"Code execution error: {str(e)}")
            else:
                output_container.warning("⚠️ Code execution is supported for Python, C++, Java only.")

    # 📥 Save Code
    with col3:
        if st.button("📥 Save Code"):
            with open(f"saved_code_{st.session_state.mentor_type}.txt", "w") as f:
                f.write(code_area)
            st.success("✅ Code saved successfully!")

    # Additional Tools with Realtime AI
    st.markdown("### 🔧 Extra Tools")
    tool_choice = st.selectbox("Choose AI Tool", [
        "Code Explainer", "Syntax Checker", "Interview Prep", "Resume Feedback", "Cheat Sheet Generator"
    ], index=0)

    tool_input = st.text_area("Enter your content or paste code/question here:", height=150)

    if st.button("🎯 Run Tool"):
        if tool_input:
            try:
                tool_prompt = ChatPromptTemplate.from_messages([
                    SystemMessagePromptTemplate.from_template(
                        f"You are a professional assistant for {tool_choice}. Provide accurate, clear, and brief output in {lang}."
                    ),
                    HumanMessagePromptTemplate.from_template("{question}")
                ])
                messages = tool_prompt.format_messages(question=tool_input)
                tool_result = model.invoke(messages)
                st.success(f"✅ {tool_choice} Result")
                st.markdown(f"**🧠 Output:**\n\n{tool_result.content}")
            except Exception as e:
                st.error(f"❌ Tool Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter something for the tool to work on.")

    # Footer
    st.markdown("""
    <div style='text-align: center; margin-top: 40px; font-size: 16px;'>
        <hr style='margin-top:30px;margin-bottom:10px;border:0;border-top:1px solid #ccc;' />
        <p>© Powered by Munesula Vamshi | Quality Thought AI Mentor | Realtime API Based</p>
    </div>
    """, unsafe_allow_html=True)
