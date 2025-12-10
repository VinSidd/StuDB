#this is a quiz game
import random 
logged = True  
student_name = ""

def take_quiz():
    score = 0
    print("Welcome to the quiz game!\n")
    print("You will be asked 5 questions.")
    print("For each correct answer, you will earn 1 point.\n")
    print("Let's begin!\n")
    questions = {
        "In which year was the Indian Constitution adopted by the Constituent Assembly?": "1949",
        "Who is considered the chief architect of the Indian Constitution?": "Dr. B.R.Ambedkar" or "B.R.Ambedkar",
        "The concept of a federal system with a strong center was inspired by the constitution of which country?": "Canada",
        "Who was the first President of India?": "Dr. Rajendra Prasad" or "Rajendra Prasad",
        "Who is the first Prime Minister of India?": "Pandit Jawaharlal Nehru" or "Jawaharlal Nehru"
    }
    question_list = list(questions.keys())
    random.shuffle(question_list)
    for i in range(5):
        print(f"Question {i+1}: {question_list[i]}")
        answer = input("Your answer: ")
        if answer.strip().lower() == questions[question_list[i]].strip().lower():
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong! The correct answer is: {questions[question_list[i]]}\n")
    print(f"Your final score is: {score}/5\n")
    if score == 5:
        print("Excellent! You got all questions right!\n")
    elif score >= 3:
        print("Good job! You did well.\n")
    else:
        print("Better luck next time!\n")
    import finalproject
    finalproject.logged = logged
    finalproject.student_name = student_name
    finalproject.home()
        