import re

def extract_keywords(text):
    # Simple keyword extraction (can be improved)
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    return set(words)

def main():
    print("===== Resume Keyword Matcher =====\n")
    
    print("Paste your Resume text (press Enter twice when done):")
    resume_lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        resume_lines.append(line)
    resume = " ".join(resume_lines)

    print("\nPaste Job Description (press Enter twice when done):")
    jd_lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        jd_lines.append(line)
    job_desc = " ".join(jd_lines)

    resume_keywords = extract_keywords(resume)
    jd_keywords = extract_keywords(job_desc)

    matched = resume_keywords & jd_keywords
    missing = jd_keywords - resume_keywords

    print("\n===== Results =====")
    print(f"Matched Keywords ({len(matched)}):")
    print(", ".join(sorted(matched)[:30]))

    print(f"\nMissing Keywords ({len(missing)}):")
    print(", ".join(sorted(missing)[:30]))

    match_percent = (len(matched) / len(jd_keywords)) * 100 if jd_keywords else 0
    print(f"\nMatch Score: {match_percent:.1f}%")

if __name__ == "__main__":
    main()
