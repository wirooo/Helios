from pdfminer.high_level import *

def match_keywords(resume_link):
    resume_data = extract_text(resume_link)
    keywords = []

    with open("static/keywords.txt") as keywordsfile:
     for line in keywordsfile:
          if line != "":
             keywords.append(line.rstrip('\n'))

    matched = []

    for kwd in keywords:
        if kwd in resume_data:
            matched.append(kwd)

    return matched
