from groq import Groq
import streamlit as st


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)


# ============================================================
# ANALYZE STARTUP
# ============================================================

def analyze_startup(
    startup_name,
    description,
    industry,
    business_model,
    target_market,
    budget,
    competition
):

    prompt = f"""
You are StartupSense AI, an expert startup advisor.

Analyze the following startup idea.

Startup Name:
{startup_name}

Description:
{description}

Industry:
{industry}

Business Model:
{business_model}

Target Customers:
{target_market}

Estimated Initial Budget:
₹{budget}

Competition Level:
{competition}/10


Provide a practical startup analysis.

Include:

1. Overall Startup Score out of 100
2. Market Potential
3. Key Strengths
4. Key Risks
5. Target Market Analysis
6. Business Model Analysis
7. Competition Analysis
8. Specific Recommendations
9. Final Verdict

Be realistic and critical.
Do not simply say the idea is good.
Point out weaknesses and possible problems.
Give practical recommendations for improving the idea.
"""


    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are StartupSense AI, "
                    "a practical startup advisor."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=2000
    )


    return response.choices[0].message.content