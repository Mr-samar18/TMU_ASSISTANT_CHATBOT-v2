import requests
import re

def strip_markdown(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'#{1,6}\s*', '', text)
    text = re.sub(r'`{1,3}(.*?)`{1,3}', r'\1', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def clean_response(text):
    """Remove gemma's annoying disclaimers and meta-comments."""
    # remove "Note: This is a summary..." lines
    lines = text.split('\n')
    clean = []
    skip_phrases = [
        "note:", "this is a summary", "please refer to",
        "may not be exhaustive", "original source",
        "i am an ai", "i'm an ai", "as an ai",
        "i don't have access", "i cannot provide",
        "please note that"
    ]
    for line in lines:
        line_lower = line.lower().strip()
        if any(phrase in line_lower for phrase in skip_phrases):
            continue
        clean.append(line)
    return '\n'.join(clean).strip()

def is_tmu_question(question):
    tmu_keywords = [
        "tmu", "teerthanker", "moradabad", "university",
        "bca", "mca", "btech", "b.tech", "mtech", "m.tech",
        "bba", "mba", "bcom", "mcom", "b.com", "m.com",
        "law", "llb", "pharmacy", "pharm", "nursing", "gnm", "anm",
        "medical", "mbbs", "dental", "bds", "agriculture", "agri",
        "hostel", "library", "wifi", "campus", "facilities",
        "placement", "placements", "recruitment", "package", "salary",
        "admission", "admissions", "apply", "eligibility", "fees",
        "fee", "scholarship", "course", "courses", "program", "programs",
        "semester", "duration", "syllabus", "subjects", "career",
        "college", "faculty", "department", "student", "campus life",
        "fest", "events", "clubs", "sports", "bams", "bums", "bpt",
        "bpharm", "dpharm", "mpharm", "animation", "ccsit", "phd",
        "data science", "ai ml", "cyber security", "blockchain",
        "cloud computing", "bsc", "compare", "difference", "better",
        "choose", "should i", "which is"
    ]
    question_lower = question.lower()
    return any(kw in question_lower for kw in tmu_keywords)

def ask_llama(question, context=""):
    try:
        tmu_related = is_tmu_question(question)

        if tmu_related:
            prompt = f"""You are a helpful assistant for TMU university. Answer the student's question using the information below.

{context}

Important rules:
- Give a direct clear answer only
- Do not add notes, disclaimers, or "this is a summary" messages
- Do not say "please refer to original source"
- Use plain text only, no asterisks or hashtags
- For comparisons show both sides clearly with fees, duration, careers
- Keep answer focused and useful

Question: {question}
Answer:"""

        else:
            prompt = f"""You are a helpful AI assistant. Answer this question clearly and directly.

Rules:
- Give a direct answer only
- Do not add disclaimers or notes
- Plain text only, no asterisks or hashtags
- Keep it concise and helpful

Question: {question}
Answer:"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma:2b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 400,
                    "top_p": 0.9,
                    "repeat_penalty": 1.2
                }
            },
            timeout=120
        )

        if response.status_code != 200:
            return "AI is currently unavailable. Please try again."

        result = response.json()
        answer = result.get("response", "").strip()

        if not answer:
            return "I could not generate an answer. Please visit https://www.tmu.ac.in"

        answer = strip_markdown(answer)
        answer = clean_response(answer)

        # remove prompt echoing
        if "Answer:" in answer:
            answer = answer.split("Answer:")[-1].strip()

        return answer

    except requests.exceptions.Timeout:
        return "Response is taking too long. Please try again."
    except requests.exceptions.ConnectionError:
        return "Cannot connect to AI. Make sure Ollama is running."
    except Exception as e:
        print(f"AI ERROR: {e}")
        return "AI is currently unavailable."