from google import generativeai as genai
import random


#function to score how good the answer is for that question
def getscore(question, answer):
    info = f"""
You are an interview expert but be a little free not toooo strict. A user was asked the following interview question:

Question: {question}

Their answer was: "{answer}"

Please do the following:
1. Rate the answer from 1 to 10 based on relevance, clarity, and depth.
2. Provide detailed feedback on how the answer can be improved in a single line.
Respond in the format:
1.  **Rating:** <score>/10
2.  **Feedback:** <your feedback here>
"""
    response = model.generate_content(info)
    text = response.text.strip()

    lines = text.split("\n")
    score = -1
    feedback = "Feedback not found"

    for line in lines:
        if "**Rating:**" in line:
            try:
                score = int(line.split("**Rating:**")[1].split("/")[0].strip())
            except:
                score = -1
        elif "**Feedback:**" in line:
            feedback = line.split("**Feedback:**")[1].strip()

    return [score, feedback]


#funnction to give the final feedback on how his interview was and what are the suggestions
def finalsummary(a):
    info=f"""
you are given a list of feedback you need to summarise it and give a ultimate feedback in 5-6 ultimate points
feedback={a}"""
    response=model.generate_content(info)
    return response.text


#GPT model build
genai.configure(api_key="AIzaSyCPVOJc8Z1rpADgDF7oYoq5vhypJ0xiMWM")
model=genai.GenerativeModel("gemini-2.0-flash")


#give user option so that he can select from those
field=input("Please enter your field out of the given options \n" 
"1.web development\n" 
"2.devops\n"
"3.cybersecurity\n"
"4.ai\n"
"5.ml\n"
"6.mobile development\n"
"7.uiux\n"
"8.data analytics\n" 
"9.data scientist\n"
"10.prompt engineering\n").lower()


#question to select from the field the user selected 
imp_questions_map = {
    "general": [
        "What is the difference between a stack and a queue?",
        "Explain how a hash table works.",
        "What are the four principles of Object-Oriented Programming?",
        "What is a deadlock in operating systems? How can it be prevented?",
        "Explain the difference between processes and threads.",
        "What is a race condition? How do you avoid it?",
        "What is virtual memory? How does it work?",
        "How does a compiler work?",
        "What is the difference between TCP and UDP?",
        "Explain the concept of normalization in databases."
    ],
    "web development": [
        "What is the difference between HTML and XHTML?",
        "Explain how RESTful APIs work.",
        "What are the advantages of using React over plain JavaScript?",
        "How does the virtual DOM improve performance?",
        "What are HTTP methods? Explain each.",
        "What is the difference between sessionStorage and localStorage?",
        "What is CORS and how do you handle it?",
        "Explain the box model in CSS.",
        "What is responsive design?",
        "What is the difference between SQL and NoSQL databases?"
    ],
    "devops": [
        "What is CI/CD and why is it important?",
        "Explain the concept of Infrastructure as Code.",
        "What is Docker and how is it different from a virtual machine?",
        "What are containers and how do they help in deployment?",
        "What is Kubernetes used for?",
        "How do you monitor applications in production?",
        "What is the role of Jenkins in DevOps?",
        "What are some popular logging tools?",
        "Explain blue-green deployment.",
        "What is Ansible used for?"
    ],
    "cybersecurity": [
        "What is the difference between symmetric and asymmetric encryption?",
        "What is SQL injection and how do you prevent it?",
        "What are some common types of malware?",
        "What is the CIA triad?",
        "What is multi-factor authentication?",
        "What are firewalls and how do they work?",
        "Explain HTTPS and how it secures data.",
        "What is penetration testing?",
        "How do you secure an API?",
        "What are some best practices for password security?"
    ],
    "ai": [
        "What is the difference between AI, ML, and Deep Learning?",
        "Explain a neural network and how it learns.",
        "What is gradient descent?",
        "What is the role of activation functions in neural networks?",
        "Explain supervised vs. unsupervised learning.",
        "What is backpropagation?",
        "What is overfitting and how do you avoid it?",
        "What is transfer learning?",
        "What are some common use-cases of AI?",
        "How do you evaluate a classification model?"
    ],
    "ml": [
        "What is supervised learning? Give an example.",
        "What is the difference between classification and regression?",
        "How does linear regression work?",
        "What are decision trees and how do they work?",
        "What is overfitting vs underfitting?",
        "Explain cross-validation and its importance.",
        "What is regularization in machine learning?",
        "What is the difference between bagging and boosting?",
        "What is the role of a cost function?",
        "How do you handle missing data in ML datasets?"
    ],
    "mobile development": [
        "What is the difference between native and hybrid apps?",
        "Explain the lifecycle of an Android activity.",
        "What is Flutter and why use it?",
        "How do you handle data persistence in mobile apps?",
        "What is MVVM architecture?",
        "Explain push notifications and how they work.",
        "What are the limitations of mobile development?",
        "How do you optimize performance in mobile apps?",
        "What is the role of App Store Optimization (ASO)?",
        "Explain the concept of responsive design in mobile."
    ],
    "uiux": [
        "What is the difference between UI and UX?",
        "What are some principles of good UX design?",
        "What is a user journey?",
        "How do you conduct user testing?",
        "What tools do you use for UI/UX design?",
        "What is wireframing?",
        "How do you design for accessibility?",
        "What is the role of prototyping?",
        "Explain the concept of design thinking.",
        "How do you collect and incorporate user feedback?"
    ],
    "data analytics": [
        "What is the difference between descriptive and inferential statistics?",
        "What are some common data cleaning techniques?",
        "Explain how to deal with missing data.",
        "What is the role of data visualization?",
        "What is a pivot table?",
        "What are outliers and how do you handle them?",
        "Explain correlation vs causation.",
        "What are some commonly used data analytics tools?",
        "How do you handle large datasets efficiently?",
        "What is ETL and how does it work?"
    ],
    "data scientist": [
        "What is the difference between supervised and unsupervised learning?",
        "Explain bias-variance tradeoff in machine learning.",
        "How do you handle imbalanced datasets?",
        "What are precision, recall, and F1-score? Why are they important?",
        "Describe a machine learning project you've worked on.",
        "What is feature engineering? Give examples.",
        "How do you select important variables in a dataset?",
        "Explain overfitting and how to prevent it.",
        "What’s the difference between bagging and boosting?",
        "Describe the steps in a typical machine learning pipeline."
    ],
    "prompt engineering": [
        "What is prompt engineering and why is it important?",
        "How do temperature and top_p affect model output in LLMs?",
        "How do you write a good system prompt for a chatbot?",
        "What are the risks of prompt injection attacks?",
        "What is chain-of-thought prompting?",
        "How does few-shot prompting improve performance?",
        "What are embeddings, and how are they used in retrieval-augmented generation?",
        "What are the limitations of prompt-based techniques?",
        "Explain the role of role-based prompts in function calling.",
        "How would you structure a prompt to summarize a large document accurately?"
    ]
}


#model train and evaluation
if field not in imp_questions_map.keys():
    print("Field not found")
else:
    imp_questions=random.sample(imp_questions_map[field],10)
    imp_questions+=random.sample(imp_questions_map['general'],5)
    score=[]
    feedback=[]
    for i in imp_questions:
        #print the question for the user to read
        ans="Input answer from the user through their voice or speach"
        result=getscore(i,ans)
        score.append(result[0])
        feedback.append(result[1])
    summary=finalsummary(feedback)
    #show the user his score and suggestion he can improve in the feedback page
