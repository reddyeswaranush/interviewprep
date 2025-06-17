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
    "Tell me about yourself.",
    "What are your strengths and weaknesses?",
    "How do you handle stress or pressure?",
    "Describe a time when you worked in a team.",
    "How do you manage your time and prioritize tasks?",
    "Why do you want to join this company?",
    "Where do you see yourself in 5 years?",
    "Describe a challenge or conflict you faced and how you dealt with it.",
    "What motivates you to do your best?",
    "How do you handle feedback and criticism?",
    "Tell me about a time you took initiative.",
    "How do you stay organized during busy schedules?",
    "What do you do when you face a task you don’t know how to solve?",
    "Tell me about a mistake you made and what you learned from it.",
    "Have you ever led a project or team? What was your experience?",
    "How do you manage deadlines when working on multiple tasks?",
    "Why should we hire you?",
    "Tell me about a time you failed. How did you respond?",
    "How do you approach learning something new?",
    "What do you know about our company?",
    "How do you balance quality and speed in your work?",
    "Describe a time when you had to make a difficult decision.",
    "How do you communicate in a remote or hybrid work environment?",
    "What kind of work culture are you most comfortable in?",
    "Do you prefer working independently or in a team? Why?"
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
        "What is the difference between SQL and NoSQL databases?",
        "What are web sockets and when are they used?",
        "What is a service worker in PWA?",
        "What is lazy loading and why is it useful?",
        "Difference between GET and POST requests?",
        "How does server-side rendering differ from client-side rendering?",
        "What is Next.js and how is it different from React?",
        "What is a CDN and how does it help?",
        "What is HTTPS and why is it important?",
        "Explain the concept of middleware in Express.js.",
        "What is an ORM and why use it?",
        "Explain MVC architecture.",
        "What is the difference between PUT and PATCH requests?",
        "What is GraphQL and how does it compare to REST?",
        "How do cookies and sessions work?",
        "What is JWT and how is it used in authentication?"
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
        "What is Ansible used for?",
        "What is Terraform and how is it used?",
        "What is a build pipeline?",
        "What is Helm in Kubernetes?",
        "What is a rolling update in deployments?",
        "Explain canary deployments.",
        "What is load balancing and how does it work?",
        "What is the difference between horizontal and vertical scaling?",
        "What are artifacts in a CI/CD pipeline?",
        "What is the use of Prometheus and Grafana?",
        "What is a reverse proxy?",
        "How do you ensure zero-downtime deployments?",
        "Explain the role of GitOps.",
        "What are secrets management tools?",
        "What is the purpose of using NGINX in DevOps?",
        "What is a container registry?"
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
        "What are some best practices for password security?",
        "What is phishing and how can it be prevented?",
        "What is social engineering?",
        "What is a DDoS attack?",
        "What are intrusion detection systems?",
        "What is a VPN and how does it work?",
        "What is data encryption at rest vs in transit?",
        "What is a zero-day vulnerability?",
        "Explain role-based access control (RBAC).",
        "What is a digital certificate?",
        "How does a public key infrastructure (PKI) work?",
        "What is a man-in-the-middle attack?",
        "What are honeypots in cybersecurity?",
        "Explain sandboxing in malware analysis.",
        "What are security patches?",
        "What is OWASP Top 10?"
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
        "How do you evaluate a classification model?",
        "What is reinforcement learning?",
        "What is an autoencoder?",
        "Explain convolutional neural networks (CNNs).",
        "What are recurrent neural networks (RNNs)?",
        "What is a transformer model?",
        "What is attention mechanism in NLP?",
        "What is the Turing test?",
        "What are generative adversarial networks (GANs)?",
        "What is the bias-variance tradeoff?",
        "What is explainable AI (XAI)?",
        "How do you train a deep learning model?",
        "What is early stopping in training?",
        "What are hyperparameters?",
        "What is a confusion matrix?",
        "What is the role of regularization in deep learning?"
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
        "How do you handle missing data in ML datasets?",
        "What is the k-nearest neighbors (KNN) algorithm?",
        "What is support vector machine (SVM)?",
        "What is Naive Bayes algorithm?",
        "What is logistic regression?",
        "What is feature scaling and why is it needed?",
        "What is principal component analysis (PCA)?",
        "What is model drift?",
        "How do you tune hyperparameters?",
        "What is grid search and random search?",
        "What are ensemble models?",
        "What is a confusion matrix and what do its values represent?",
        "How do you balance an imbalanced dataset?",
        "What is precision-recall tradeoff?",
        "What is ROC-AUC score?",
        "What is the purpose of stratified sampling?"
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
        "Explain the concept of responsive design in mobile.",
        "What is the difference between Android and iOS development?",
        "What is React Native and how does it work?",
        "How do you handle offline mode in apps?",
        "What is a RecyclerView?",
        "Explain intents in Android.",
        "What is dependency injection in Android?",
        "What are permissions in mobile apps?",
        "How do you debug a mobile app?",
        "What is Jetpack Compose?",
        "How is state management handled in Flutter?",
        "What is a storyboard in iOS?",
        "What are background services?",
        "How do you handle API calls in mobile apps?",
        "What is the difference between LiveData and Flow?",
        "How do you publish an app to Google Play Store?"
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
        "How do you collect and incorporate user feedback?",
        "What is the importance of consistency in UI design?",
        "What is heuristic evaluation?",
        "What is the role of typography in UI?",
        "What are color theory principles?",
        "How does UX impact business goals?",
        "What is A/B testing in UI/UX?",
        "What is microcopy and why is it important?",
        "Explain responsive vs adaptive design.",
        "What is a user persona?",
        "What is interaction design?",
        "What is a high-fidelity vs low-fidelity prototype?",
        "How do you measure UX success?",
        "What is card sorting?",
        "What are accessibility standards (WCAG)?",
        "What is the role of animation in UI?"
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
        "What is ETL and how does it work?",
        "What is a histogram and when is it used?",
        "What is data wrangling?",
        "What is the difference between mean, median, and mode?",
        "What is standard deviation and variance?",
        "What is a box plot?",
        "What is a time series analysis?",
        "What is the difference between R and Python for analytics?",
        "What is the use of SQL in data analytics?",
        "How do dashboards help in analytics?",
        "What is cohort analysis?",
        "What is hypothesis testing?",
        "What are confidence intervals?",
        "How do you avoid bias in analytics?",
        "What is the purpose of a heatmap?",
        "What is a funnel analysis?"
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
        "Describe the steps in a typical machine learning pipeline.",
        "What tools do you use as a data scientist?",
        "What is dimensionality reduction?",
        "How do you evaluate regression models?",
        "What is the difference between ROC and PR curves?",
        "What is model interpretability?",
        "How do you deploy a machine learning model?",
        "What is a recommendation system?",
        "How do you deal with outliers?",
        "What is SMOTE?",
        "What is A/B testing in data science?",
        "How do you build a data pipeline?",
        "What are data lakes and data warehouses?",
        "What is a baseline model?",
        "How do you perform EDA (Exploratory Data Analysis)?",
        "What is clustering and what are its applications?"
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
        "How would you structure a prompt to summarize a large document accurately?",
        "What is zero-shot learning in prompt design?",
        "What is in-context learning?",
        "What is semantic search and how is it used with LLMs?",
        "How do you evaluate the output of an LLM?",
        "What is hallucination in LLMs?",
        "What are guardrails in LLM applications?",
        "What is prompt chaining?",
        "How do you personalize prompts for users?",
        "What are system vs user prompts?",
        "What is instruction tuning?",
        "How do you manage memory in prompt-based agents?",
        "What is RAG (retrieval-augmented generation)?",
        "What is the difference between deterministic and probabilistic LLM output?",
        "How do prompts interact with tools in agent systems?",
        "How do you test prompt robustness?"
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
