import streamlit as st

from config import APP_NAME, APP_TAGLINE, OPENAI_API_KEY
from prompts import get_system_prompt
from services.llm_service import generate_response


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_title" not in st.session_state:
    st.session_state.chat_title = "New Chat"


# =========================================================
# SMALL + SAFE CSS
# =========================================================

st.markdown(
    """
<style>

/* Main readable width */
.block-container {
    max-width: 960px;
    padding-top: 1.2rem;
    padding-bottom: 7rem;
}

/* Hide unnecessary Streamlit footer/menu */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    border-right: 1px solid #E4E7EC;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    min-height: 42px;
    font-weight: 600;
}

/* Chat messages */
div[data-testid="stChatMessage"] {
    border-radius: 14px;
    padding: 0.35rem 0.25rem;
}

/* Make long content wrap properly */
div[data-testid="stChatMessageContent"] {
    line-height: 1.7;
    overflow-wrap: anywhere;
    word-break: break-word;
}

/* Code blocks inside long answers */
div[data-testid="stChatMessageContent"] pre {
    overflow-x: auto;
    max-width: 100%;
}

/* Composer */
div[data-testid="stChatInput"] {
    max-width: 960px;
    margin: auto;
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    # -----------------------------------------------------
    # BRAND
    # -----------------------------------------------------

    brand_col1, brand_col2 = st.columns(
        [1, 4],
        vertical_alignment="center"
    )

    with brand_col1:
        st.markdown(
            """
            <div style="
                width:42px;
                height:42px;
                border-radius:12px;
                background:linear-gradient(135deg,#635BFF,#8B5CF6);
                color:white;
                display:flex;
                align-items:center;
                justify-content:center;
                font-weight:700;
                font-size:14px;
            ">
                AV
            </div>
            """,
            unsafe_allow_html=True
        )

    with brand_col2:
        st.markdown("### Aivora AI")
        st.caption("Multi-Role AI Assistant")

    st.write("")

    # -----------------------------------------------------
    # NEW CHAT
    # -----------------------------------------------------

    if st.button(
        "＋ New Chat",
        use_container_width=True,
        type="primary"
    ):
        st.session_state.messages = []
        st.session_state.chat_title = "New Chat"
        st.rerun()

    st.divider()

    # -----------------------------------------------------
    # ASSISTANT MODE
    # -----------------------------------------------------

    assistant_mode = st.selectbox(
        "Assistant Mode",
        [
            "General Assistant",
            "AI Tutor",
            "Health Education",
            "Research Assistant",
            "Marketing Assistant",
            "Coding Assistant",
            "Politics & Civic Information",
        ]
    )

    mode_descriptions = {
        "General Assistant":
            "Everyday questions, writing and general help.",

        "AI Tutor":
            "Learn AI from beginner to advanced.",

        "Health Education":
            "General educational healthcare information.",

        "Research Assistant":
            "Research, methodology and academic support.",

        "Marketing Assistant":
            "Branding, strategy and creative marketing.",

        "Coding Assistant":
            "Programming, debugging and technical help.",

        "Politics & Civic Information":
            "Neutral and factual civic information.",
    }

    st.caption(
        mode_descriptions[assistant_mode]
    )

    # -----------------------------------------------------
    # SETTINGS
    # -----------------------------------------------------

    with st.expander(
        "Response Settings",
        expanded=False
    ):

        response_style = st.selectbox(
            "Style",
            [
                "Concise",
                "Balanced",
                "Detailed"
            ],
            index=1
        )

        response_length = st.selectbox(
            "Length",
            [
                "Short",
                "Medium",
                "Long"
            ],
            index=1
        )

        language = st.selectbox(
            "Language",
            [
                "Auto Detect",
                "English",
                "Urdu",
                "Roman Urdu",
                "Arabic"
            ]
        )

        creativity = st.slider(
            "Creativity",
            0.0,
            1.0,
            0.5,
            0.1
        )

        max_output_tokens = st.slider(
            "Maximum Output Tokens",
            min_value=200,
            max_value=4000,
            value=1200,
            step=200
        )

    st.divider()

    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    if OPENAI_API_KEY:
        st.success(
            "API Ready",
            icon=None
        )
    else:
        st.error(
            "API key missing",
            icon=None
        )

    # -----------------------------------------------------
    # CLEAR
    # -----------------------------------------------------

    if st.button(
        "Clear Conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.session_state.chat_title = "New Chat"
        st.rerun()


# =========================================================
# MAIN HEADER
# =========================================================

top_left, top_right = st.columns(
    [7, 1],
    vertical_alignment="center"
)

with top_left:

    if st.session_state.chat_title == "New Chat":
        st.markdown("### Aivora AI")
    else:
        st.markdown(
            f"### {st.session_state.chat_title}"
        )

    st.caption(
        f"{assistant_mode} · {APP_TAGLINE}"
    )


with top_right:

    if OPENAI_API_KEY:
        st.caption("● Online")
    else:
        st.caption("● Offline")


st.divider()


# =========================================================
# EMPTY STATE
# =========================================================

if not st.session_state.messages:

    st.write("")
    st.write("")

    st.markdown(
        "<h1 style='text-align:center;'>How can I help you today?</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            text-align:center;
            color:#667085;
            font-size:16px;
            margin-bottom:30px;
        ">
            Ask anything, paste a detailed prompt,
            or choose a specialized assistant mode.
        </p>
        """,
        unsafe_allow_html=True
    )

    suggestion_col1, suggestion_col2 = st.columns(2)

    with suggestion_col1:

        explain_button = st.button(
            "Learn a new concept",
            use_container_width=True
        )

        research_button = st.button(
            "Work on research",
            use_container_width=True
        )

    with suggestion_col2:

        coding_button = st.button(
            "Solve a coding problem",
            use_container_width=True
        )

        marketing_button = st.button(
            "Develop a marketing idea",
            use_container_width=True
        )

else:

    explain_button = False
    research_button = False
    coding_button = False
    marketing_button = False


# =========================================================
# CHAT HISTORY DISPLAY
# =========================================================

for message in st.session_state.messages:

    avatar = None

    if message["role"] == "assistant":
        avatar = "🤖"

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.markdown(
            message["content"]
        )


# =========================================================
# SUGGESTION BUTTON LOGIC
# =========================================================

suggested_prompt = None

if explain_button:

    suggested_prompt = (
        "Teach me a useful concept in simple language."
    )

elif research_button:

    suggested_prompt = (
        "Help me structure an academic research study."
    )

elif coding_button:

    suggested_prompt = (
        "Help me solve a coding problem step by step."
    )

elif marketing_button:

    suggested_prompt = (
        "Help me develop a professional marketing idea."
    )


# =========================================================
# USER INPUT
# =========================================================

typed_prompt = st.chat_input(
    "Message Aivora AI..."
)

user_prompt = (
    suggested_prompt
    or typed_prompt
)


# =========================================================
# PROCESS CHAT
# =========================================================

if user_prompt:

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    if not st.session_state.messages:

        short_title = (
            user_prompt
            .replace("\n", " ")
            .strip()
        )

        if len(short_title) > 42:
            short_title = (
                short_title[:42]
                + "..."
            )

        st.session_state.chat_title = (
            short_title
        )


    # -----------------------------------------------------
    # SAVE USER MESSAGE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )


    # -----------------------------------------------------
    # SHOW USER MESSAGE
    # -----------------------------------------------------

    with st.chat_message("user"):
        st.markdown(user_prompt)


    # -----------------------------------------------------
    # SYSTEM PROMPT
    # -----------------------------------------------------

    base_system_prompt = (
        get_system_prompt(
            assistant_mode
        )
    )


    # -----------------------------------------------------
    # DYNAMIC RESPONSE RULES
    # -----------------------------------------------------

    preference_prompt = f"""
CURRENT USER PREFERENCES

Response style:
{response_style}

Preferred response length:
{response_length}

Language setting:
{language}

Creativity setting:
{creativity}


CONVERSATION RULES

- Treat this conversation as continuous.
- Use previous messages to interpret the current message.
- Understand incomplete follow-up phrases from context.
- Resolve pronouns such as he, she, it, they, this and that.
- Resolve short replies such as stats, details, more, why, where,
  btao, batao, haan, yes, continue and go ahead from recent context.
- Do not ask the user to repeat information already available.
- If you previously offered additional information and the user says
  yes, haan, batao, continue or similar wording, continue that offer.
- Ask for clarification only if the meaning genuinely cannot be inferred.


LONG PROMPT RULES

- Read the entire user message before answering.
- Long prompts may contain multiple paragraphs or multiple tasks.
- Preserve all important constraints in the user's prompt.
- Do not ignore instructions appearing near the end of a long prompt.
- If several tasks are requested, address them in a logical order.
- When useful, structure long responses with headings and sections.


LANGUAGE RULE

If Language is Auto Detect:
respond naturally in the language/style used by the user.

For Roman Urdu:
understand informal spelling and common typing mistakes.


Apply these preferences without overriding the selected assistant's
role, factual-accuracy requirements or safety boundaries.
"""


    final_system_prompt = (
        base_system_prompt
        + "\n\n"
        + preference_prompt
    )


    # =====================================================
    # CONTEXT MANAGEMENT
    # =====================================================

    context_messages = (
        st.session_state.messages[-20:]
    )


    # =====================================================
    # API CALL
    # =====================================================

    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        with st.spinner(
            "Aivora is thinking..."
        ):

            assistant_response = (
                generate_response(
                    final_system_prompt,
                    context_messages,
                    max_output_tokens=(
                        max_output_tokens
                    ),
                )
            )

        st.markdown(
            assistant_response
        )


    # =====================================================
    # SAVE RESPONSE
    # =====================================================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response
        }
    )

    st.rerun()