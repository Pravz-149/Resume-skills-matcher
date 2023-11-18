from utils import extract_text_from_pdf_or_doc,extract_text_from_url,preprocess_text,reorder_skills
from utils import sort_skills_by_pos,capitalize_words,calculate_tfidf_similarity_cached,calculate_bow
from utils import remove_links_async,extract_text_with_spaces,calculate_similarity,calculate_word_similarity
from utils import preprocess_job_descriptions

def main():
    # Take input for the PDF file path
    doc = input("Enter the PDF file path: ")
    # doc = 'Pravallika Molleti.pdf'
    # Take input for the URL
    url = input("Enter the URL: ")
    # url = 'https://www.linkedin.com/jobs/collections/recommended/?currentJobId=3703879688'

    #Extracting the text from doc and url
    resume_text = extract_text_from_pdf_or_doc(doc)
    job_name, job_description = extract_text_from_url(url)

    #Preprocessing the data feom pdf and url
    resume_text = preprocess_text(resume_text)
    job_description = preprocess_text(job_description)

    matching_skills = []
    non_matching_skills = []

    # Split the job description and resume text into sets of skills
    jd_skills = set(job_description.split())
    resume_skills = set(resume_text.split())

    # Find matching skills(skills present in both sets) and non-matching skills(skills in the job description that are not in the resume)
    matching_skills = jd_skills.intersection(resume_skills)
    non_matching_skills = jd_skills.difference(resume_skills)

    # Convert matching and non-matching skills back to lists and remove duplicates
    matching_skills = list(set(matching_skills))
    non_matching_skills = list(set(non_matching_skills))

    # Reorder matching and recommended skills by tf_idf scores 
    ordered_matching_skills = reorder_skills(matching_skills,url)
    ordered_recommended_skills = reorder_skills(non_matching_skills,url)

    # Sorting the top skills by pos and tfidf
    top_10_matching_skills = sort_skills_by_pos(ordered_matching_skills)
    top_10_recommended_skills = sort_skills_by_pos(ordered_recommended_skills[:30])[:10]
    more_recommended_skills = list(set(ordered_recommended_skills) - set(top_10_recommended_skills))

    return {
        'Matching Skills': capitalize_words(top_10_matching_skills),
        'Recommended Skills': capitalize_words(top_10_recommended_skills),
        "More Recommended Skills": capitalize_words(more_recommended_skills)
    }

if __name__ == "__main__":
    result = main()
    print(result)

  