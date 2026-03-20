import os
from groq import Groq

def analyze_report_with_openai(text):
    # Function name retained for compatibility, but uses Groq internally
    groq_api_key = os.environ.get('GROQ_API_KEY')
    if not groq_api_key:
        return {
            'summary': 'Groq API key not configured.',
            'explanation': 'Please set the GROQ_API_KEY to enable the AI analyzer.',
            'recommendation': 'Unable to determine'
        }

    client = Groq(api_key=groq_api_key)
    
    prompt = f"""You are a helpful medical assistant. Analyze the following medical report text and provide:
    1. A concise summary in bullet points (plain language).
    2. An explanation of any medical terms.
    3. A recommendation: either "Consult a doctor" or "No immediate consultation needed" with a brief reason.

    Report text:
    {text[:4000]}  # Truncate to avoid token limits
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=600
        )
        content = response.choices[0].message.content
        lines = content.split('\n')
        summary = []
        explanation = []
        recommendation = "Unable to determine"
        current_section = None
        for line in lines:
            lower_line = line.lower()
            if 'summary' in lower_line:
                current_section = 'summary'
            elif 'explanation' in lower_line or 'medical term' in lower_line:
                current_section = 'explanation'
            elif 'recommendation' in lower_line:
                current_section = 'recommendation'
            elif line.strip() and current_section:
                if current_section == 'summary':
                    summary.append(line.strip())
                elif current_section == 'explanation':
                    explanation.append(line.strip())
                elif current_section == 'recommendation':
                    recommendation = line.strip()
        return {
            'summary': '\n'.join(summary) if summary else content,
            'explanation': '\n'.join(explanation) if explanation else 'No specific medical terms extracted.',
            'recommendation': recommendation if recommendation != "Unable to determine" else "Consult a doctor for interpretation."
        }
    except Exception as e:
        return {
            'summary': 'Error analyzing report.',
            'explanation': str(e),
            'recommendation': 'Please try again later.'
        }
