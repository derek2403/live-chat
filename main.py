import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            data: dict = json.load(file)
        return data
    except FileNotFoundError:
        # If the file doesn't exist, return an empty dictionary
        return {}

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
        
def find_best_match(user_question: str, questions: list[str]) -> str|None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str|None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None  # Return None if question not found

def chatBot():
    knowledge_base = load_knowledge_base('knowledge_base.json')
    while True:
        user_input: str = input('You: ').lower()
        if user_input == "quit":
            break
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
        
        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or type "skip" to skip: ')
            
            if new_answer.lower() != 'skip':
                knowledge_base.setdefault('questions', []).append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you!')

if __name__ == '__main__':
    chatBot()
