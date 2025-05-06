import random

class QuizManager:
    def __init__(self, num_questions=10):
        # Khởi tạo số câu hỏi và trạng thái quiz
        self.num_questions = num_questions
        self.questions = self.generate_questions()
        self.current_index = 0
        self.score = 0
        self.finished = False

    def generate_questions(self):
        # Tạo ra 10 câu hỏi ngẫu nhiên
        questions = []
        for _ in range(self.num_questions):
            op = random.choice(['+', '-', '*', '/'])

            if op == '/':
                b = random.randint(1, 9)  # Đảm bảo chia cho số không và chia hết
                a = b * random.randint(2, 10)
                question_text = f"{ a }   /   { b }"
                answer = a // b
            elif op == '+':
                a = random.randint(1, 99)
                b = random.randint(1, 99)
                question_text = f"{ a }   +   { b }"
                answer = a + b
            elif op == '-':
                a = random.randint(1, 99)
                b = random.randint(1, 99)
                if a < b:
                    a, b = b, a  # hoán đổi để a luôn >= b
                question_text = f"{a}   -   {b}"
                answer = a - b
            elif op == '*':
                a = random.randint(1, 9)
                b = random.randint(1, 9)
                question_text = f"{ a }   *   { b }"
                answer = a * b

            questions.append({
                "question": question_text,
                "answer": answer
            })

        return questions

    def get_current_question(self):
        # Lấy câu hỏi hiện tại
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    def submit_answer(self, user_input):
        # Kiểm tra câu trả lời
        question = self.get_current_question()
        if question and self.check_answer(user_input, question["answer"]):
            self.score += 1
            result = True
        else:
            result = False
        
        self.current_index += 1
        if self.current_index >= len(self.questions):
            self.finished = True

        return result

    def check_answer(self, user_input, correct_answer):
        # Kiểm tra đáp án người chơi nhập vào
        try:
            return int(user_input) == correct_answer
        except ValueError:
            return False

    def get_score(self):
        return self.score

    def is_finished(self):
        return self.finished

class QuizManager_for_finger:
    def __init__(self, num_questions=10):
        # Khởi tạo số câu hỏi và trạng thái quiz
        self.num_questions = num_questions
        self.questions = self.generate_questions_for_finger()
        self.current_index = 0
        self.score = 0
        self.finished = False

    def generate_questions_for_finger(self):
        questions = []
        while len(questions) < self.num_questions:
            op = random.choice(['+', '-', '*', '/'])

            if op == '+':
                a = random.randint(0, 9)
                b = random.randint(0, 9)
                result = a + b

            elif op == '-':
                a = random.randint(0, 9)
                b = random.randint(0, 9)
                if a < b:
                    a, b = b, a
                result = a - b

            elif op == '*':
                a = random.randint(0, 9)
                b = random.randint(0, 9)
                result = a * b

            elif op == '/':
                b = random.randint(1, 9)
                result = random.randint(0, 9)
                a = b * result  # đảm bảo chia hết
            else:
                continue

            # Đảm bảo kết quả chỉ là một chữ số
            if 0 <= result <= 9:
                if op == '/':
                    question_text = f"{a}   /   {b}"
                else:
                    question_text = f"{a}   {op}   {b}"
                questions.append({
                    "question": question_text,
                    "answer": result
                })

        return questions

    def get_current_question(self):
        # Lấy câu hỏi hiện tại
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    def submit_answer(self, user_input):
        # Kiểm tra câu trả lời
        question = self.get_current_question()
        if question and self.check_answer(user_input, question["answer"]):
            self.score += 1
            result = True
        else:
            result = False
        
        self.current_index += 1
        if self.current_index >= len(self.questions):
            self.finished = True

        return result

    def check_answer(self, user_input, correct_answer):
        # Kiểm tra đáp án người chơi nhập vào
        try:
            return int(user_input) == correct_answer
        except ValueError:
            return False

    def get_score(self):
        return self.score

    def is_finished(self):
        return self.finished
