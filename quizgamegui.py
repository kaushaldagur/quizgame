import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        
        self.choice = 0
        self.score = 0
        self.high_score = 0
        self.username = ""
        self.password = ""
        self.registered_users = {}
        self.current_user = ""

        self.owner_username = "galgotias"
        self.owner_password = "@#12345"

        self.owner_questions_gk = []
        self.owner_questions_mr = []

        self.questions = []
        self.current_question_index = 0

        self.main_menu()

    def main_menu(self):
        self.clear_frame()
        tk.Label(self.root, text="[ QUIZ GAME ]", font=("Arial", 20)).pack(pady=20)
        tk.Button(self.root, text="OWNER", command=self.owner_login).pack(pady=10)
        tk.Button(self.root, text="Player", command=self.player_menu).pack(pady=10)

    def owner_login(self):
        self.clear_frame()
        tk.Label(self.root, text="[Login OWNER]", font=("Arial", 20)).pack(pady=20)
        username = simpledialog.askstring("Login", "Enter username:")
        password = simpledialog.askstring("Login", "Enter password:", show='*')
        self.login(username, password, owner=True)

    def player_menu(self):
        self.clear_frame()
        tk.Label(self.root, text="Player Menu", font=("Arial", 20)).pack(pady=20)
        tk.Button(self.root, text="Register", command=self.registration).pack(pady=10)
        tk.Button(self.root, text="Login and Play Game", command=self.player_login).pack(pady=10)
        tk.Button(self.root, text="Highscores", command=self.show_high_score).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def registration(self):
        self.clear_frame()
        tk.Label(self.root, text="Register", font=("Arial", 20)).pack(pady=20)
        if len(self.registered_users) >= 500:
            messagebox.showerror("Error", "Maximum number of registered users reached")
            self.main_menu()
        else:
            username = simpledialog.askstring("Register", "Enter a username:")
            if username in self.registered_users:
                messagebox.showerror("Error", "Username already exists")
                self.registration()
            else:
                password = simpledialog.askstring("Register", "Enter a password:", show='*')
                self.registered_users[username] = password
                messagebox.showinfo("Success", "Registration successful!")
                self.main_menu()

    def player_login(self):
        self.clear_frame()
        tk.Label(self.root, text="[Login page]", font=("Arial", 20)).pack(pady=20)
        if not self.registered_users:
            messagebox.showerror("Error", "Register first")
            self.registration()
        username = simpledialog.askstring("Login", "Enter username:")
        password = simpledialog.askstring("Login", "Enter password:", show='*')
        self.login(username, password)

    def login(self, username, password, owner=False):
        if owner and username == self.owner_username and password == self.owner_password:
            self.current_user = self.owner_username
            messagebox.showinfo("Welcome", f"Welcome, {self.current_user}!")
            self.owner_menu()
        elif username in self.registered_users and self.registered_users[username] == password:
            self.current_user = username
            messagebox.showinfo("Welcome", f"Welcome, {self.current_user}!")
            self.category_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password. Please try again.")
            self.main_menu()

    def owner_menu(self):
        self.clear_frame()
        tk.Label(self.root, text="Owner Menu", font=("Arial", 20)).pack(pady=20)
        tk.Button(self.root, text="Add Question", command=self.add_question).pack(pady=10)
        tk.Button(self.root, text="View Questions", command=self.view_questions).pack(pady=10)
        tk.Button(self.root, text="View Players", command=self.view_players).pack(pady=10)
        tk.Button(self.root, text="Main Menu", command=self.main_menu).pack(pady=10)

    def show_high_score(self):
        self.clear_frame()
        if self.score >= self.high_score:
            self.high_score = self.score
        tk.Label(self.root, text=f"Highscore of {self.current_user} is {self.high_score}", font=("Arial", 20)).pack(pady=20)
        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu).pack(pady=10)

    def add_question(self):
        category = simpledialog.askstring("Add Question", "Enter the category (gk/mr):").strip().lower()
        question_text = simpledialog.askstring("Add Question", "Enter the question:")
        choices = [simpledialog.askstring("Add Question", f"Enter choice {i + 1}:") for i in range(4)]
        correct_answer = simpledialog.askstring("Add Question", "Enter the correct choice (1-4):")
        question = {"question_text": question_text, "choices": choices, "correct_answer": correct_answer}
        if category == "gk":
            self.owner_questions_gk.append(question)
            messagebox.showinfo("Success", "GK question added successfully!")
        elif category == "mr":
            self.owner_questions_mr.append(question)
            messagebox.showinfo("Success", "MR question added successfully!")
        else:
            messagebox.showerror("Error", "Invalid category. Please try again.")
            self.add_question()
        self.owner_menu()

    def view_questions(self):
        category = simpledialog.askstring("View Questions", "Enter the category to view (gk/mr):").strip().lower()
        questions = self.owner_questions_gk if category == "gk" else self.owner_questions_mr if category == "mr" else None
        if questions is None:
            messagebox.showerror("Error", "Invalid category. Please try again.")
            self.view_questions()
        else:
            self.clear_frame()
            tk.Label(self.root, text=f"{category.upper()} Questions", font=("Arial", 20)).pack(pady=20)
            for idx, question in enumerate(questions, 1):
                self.display_question_info(idx, question)
            tk.Button(self.root, text="Back to Owner Menu", command=self.owner_menu).pack(pady=10)

    def display_question_info(self, idx, question):
        tk.Label(self.root, text=f"Question {idx}:", font=("Arial", 14)).pack(pady=5)
        tk.Label(self.root, text=question['question_text']).pack(pady=5)
        for choice in question['choices']:
            tk.Label(self.root, text=choice).pack()
        tk.Label(self.root, text=f"Correct Answer: {question['correct_answer']}", fg='green').pack(pady=5)

    def view_players(self):
        self.clear_frame()
        if not self.registered_users:
            tk.Label(self.root, text="NO USER REGISTERED YET !!", font=("Arial", 20)).pack(pady=20)
        else:
            tk.Label(self.root, text="Registered Players", font=("Arial", 20)).pack(pady=20)
            for username in self.registered_users:
                tk.Label(self.root, text=f"Username: {username}").pack()
        tk.Button(self.root, text="Back to Owner Menu", command=self.owner_menu).pack(pady=10)

    def category_menu(self):
        self.clear_frame()
        tk.Label(self.root, text="Choose any one category :", font=("Arial", 20)).pack(pady=20)
        tk.Button(self.root, text="General Knowledge", command=self.gk).pack(pady=10)
        tk.Button(self.root, text="Mathematical Reasoning", command=self.mr).pack(pady=10)

    def gk(self):
        self.quiz("gk")

    def mr(self):
        self.quiz("mr")

    def quiz(self, category):
        self.questions = self.generate_gk_questions() if category == "gk" else self.generate_mr_questions()
        random.shuffle(self.questions)
        self.score = 0
        self.current_question_index = 0
        self.display_next_question()

    def display_next_question(self):
        if self.current_question_index < len(self.questions):
            self.clear_frame()
            question = self.questions[self.current_question_index]
            self.display_question(question)
            user_answer = self.get_user_numeric_answer()
            if user_answer == 0:
                messagebox.showinfo("Score", f"Your score: {self.score}")
                self.show_high_score()
                return
            else:
                self.check_answer(user_answer, question['correct_answer'])
                self.current_question_index += 1
                self.display_next_question()
        else:
            messagebox.showinfo("Score", f"Your final score: {self.score}")
            self.show_high_score()

    def get_user_numeric_answer(self):
        return int(simpledialog.askstring("Answer", "Your answer (Enter 0 to exit):"))

    def display_question(self, question):
        tk.Label(self.root, text=question['question_text']).pack(pady=10)
        for choice in question['choices']:
            tk.Label(self.root, text=choice).pack()

    def check_answer(self, user_answer, correct_answer):
        if str(user_answer) == correct_answer:
            messagebox.showinfo("Correct", "Correct answer!")
            self.score += 1
        else:
            messagebox.showinfo("Wrong", f"Wrong answer! The correct answer was {correct_answer}")

    def generate_gk_questions(self):
        return [
            {"question_text": "What is the capital of France?", "choices": ["1. London", "2. Paris", "3. Berlin", "4. Madrid"], "correct_answer": "2"},
            {"question_text": "MS-Word is an example of _____", "choices": ["1) An operating system", "2) A processing device", "3) Application software", "4) An input device"], "correct_answer": "3"},
            {"question_text": "National Income estimates in India are prepared by", "choices": ["1) Planning Commission", "2) Reserve Bank of India", "3) Central statistical organisation", "4) Indian statistical Institute"], "correct_answer": "3"},
            {"question_text": "Ctrl, Shift and Alt are called .......... keys.", "choices": ["1) modifier", "2) function", "3) alphanumeric", "4) adjustment"], "correct_answer": "1"},
            {"question_text": "The staple food of the Vedic Aryan was", "choices": ["1) Barley and rice", "2) Milk and its products", "3) Rice and pulses", "4) Vegetables and fruits"], "correct_answer": "2"},
            {"question_text": "The tropic of cancer does not pass through which of these Indian states?", "choices": ["1) Madhya Pradesh", "2) West Bengal", "3) West Bengal", "4) Odisha"], "correct_answer": "4"},
            {"question_text": "Fathometer is used to measure", "choices": ["1) Earthquakes", "2) Rainfall", "3) Ocean depth", "4) Sound intensity"], "correct_answer": "3"},
            {"question_text": "A computer cannot 'boot' if it does not have the _____", "choices": ["1) Compiler", "2) Loader", "3) Operating system", "4) Assembler"], "correct_answer": "3"},
            {"question_text": "The purest form of iron is", "choices": ["1) Wrought iron", "2) Steel", "3) Pig iron", "4) Nickel steel"], "correct_answer": "1"},
            {"question_text": "The working principle of a washing machine is", "choices": ["1) Reverse osmosis", "2) Diffusion", "3) Centrifugation", "4) Dialysis"], "correct_answer": "3"},
            {"question_text": "Who is the author of the book 'Freedom Behind Bars'?", "choices":["1) Kiran Bedi", "2) Jawaharlal Nehru", "3) Sheikh Abdullah", "4) Nelson Mandela"], "correct_answer": "1"},
            {"question_text": "Which of the following is not an example of an Operating System?", "choices": ["1) Windows 98", "2) BSD Unix", "3) Microsoft Office XP", "4) Red Hat Linux"], "correct_answer": "3"},
            {"question_text": "Where is the Railway Staff College located?", "choices": ["1) Pune", "2) Delhi", "3) Vadodara", "4) Allahabad"], "correct_answer": "3"},
            {"question_text": "Which of the following is the smallest ocean of the world?", "choices": ["1) Indian Ocean", "2) Pacific Ocean", "3) Atlantic Ocean", "4) Arctic Ocean"], "correct_answer": "4"},
            {"question_text": "The hottest planet in the solar system?", "choices": ["1) Mercury", "2) Venus", "3) Mars", "4) Jupiter"], "correct_answer": "2"},
            {"question_text": "Where was the electricity supply first introduced in India-", "choices": ["1) Mumbai", "2) Dehradun", "3) Darjeeling", "4) Chennai"], "correct_answer": "3"},
            {"question_text": "Who was the first Indian to win the World Amateur Billiards title?", "choices": ["1) Geet Sethi", "2) Wilson Jones", "3) Michael Ferreira", "4) Manoj Kothari"], "correct_answer": "2"},
            {"question_text": "Which of the following substance is obtained by the fractional distillation of air?", "choices": ["1) Argon", "2) Neon", "3) Liquid Oxygen", "4) All of the above"], "correct_answer": "4"},
            {"question_text": "Golf player Vijay Singh belongs to which country?", "choices": ["1) USA", "2) Fiji", "3) India", "4) UK"], "correct_answer": "2"},
            {"question_text": "Which of the following is used in pencils?", "choices": ["1) Silicon", "2) Charcoal", "3) Phosphorous", "4) Graphite"], "correct_answer": "4"},
            {"question_text": "In a Database Management System (DBMS), the content and the location of the data is defined by the ………..", "choices": ["1) Multi Dimensional data", "2) Meta Data", "3) Sequence Data", "4) Sub Data"], "correct_answer": "2"},
            {"question_text": "Which of the following metals forms an amalgam with other metals?", "choices": ["1) Tin", "2) Mercury", "3) Lead", "4) Zinc"], "correct_answer": "2"},
            {"question_text": "RBI is also known as", "choices": ["1) Bankers of Banks", "2) Banker of Bank", "3) Bank of Banks", "4) All of the above"], "correct_answer": "4"},
            {"question_text": "The largest 4-digit number exactly divisible by 88 is:", "choices": ["1) 9944", "2) 9768", "3) 9988", "4) 8888"], "correct_answer": "1"},
            {"question_text": "Which of the following is a non-metal that remains liquid at room temperature?", "choices": ["1) Phosphorous", "2) Bromine", "3) Chlorine", "4) Helium"], "correct_answer": "2"},
            {"question_text": "What is the function of Firewall in Network?", "choices": ["1) The security of the network", "2) Monitoring", "3) Data Transmission", "4) Authentication"], "correct_answer": "1"},
            {"question_text": "What is the full form of IP?", "choices": ["1) Internet Provider", "2) Internet Protocol", "3) Internet Procedure", "4) Internet Processor"], "correct_answer": "2"},
            {"question_text": "The metal whose salts are sensitive to light is?", "choices": ["1) Zinc", "2) Silver", "3) Copper", "4) Aluminium"], "correct_answer": "2"},
            {"question_text": "Which of the following is used in beauty parlors for hair setting?", "choices": ["1) Chlorine", "2) Sulphur", "3) Phosphorous", "4) Silicon"], "correct_answer": "4"},
            {"question_text": "Who is the founder of Facebook?", "choices": ["1) Mark Zuckerberg", "2) Elon Musk", "3) Bill Gates", "4) Warren Buffet"], "correct_answer": "1"},
            {"question_text": "Which river is called the 'Sorrow of Bihar'?", "choices": ["1) Damodar", "2) Gandak", "3) Kosi", "4) Ghaghra"], "correct_answer": "3"},
            {"question_text": "The Indian to beat the computers in mathematical wizardry is", "choices": ["1) Ramanujam", "2) Rina Panigrahi", "3) Raja Ramanna", "4) Shakunthala Devi"], "correct_answer": "4"},
            {"question_text": "What is the full form of P.T. in P.T. Usha's name?", "choices": ["1) Pushpa Tehlan", "2) Prema Thomas", "3) Payyoli Tevaraparampil", "4) Padmini"], "correct_answer": "3"},
            {"question_text": "The book “Long Walk to Freedom” is the autobiography of?", "choices": ["1) Nelson Mandela", "2) Louis Fischer", "3) Mahatma Gandhi", "4) B. R. Ambedkar"], "correct_answer": "1"},
            {"question_text": "Which country is known as the “Land of the Rising Sun”?", "choices": ["1) New Zealand", "2) Fiji", "3) China", "4) Japan"], "correct_answer": "4"},
            {"question_text": "The first woman in space was", "choices": ["1) Valentina Tereshkova", "2) Sally Ride", "3) Naidia Comenci", "4) Tamara Press"], "correct_answer": "1"},
            {"question_text": "How many players are there on each side in a women's basketball game?", "choices": ["1) 6", "2) 8", "3) 5", "4) 7"], "correct_answer": "3"},
            {"question_text": "What was the first electronic computer in the world?", "choices": ["1) UNIVAC", "2) EDVAC", "3) ENIAC", "4) EDSAC"], "correct_answer": "3"},
            {"question_text": "'.MOV' extension refers usually to what kind of file?", "choices": ["1) Image file", "2) Animation/movie file", "3) Audio file", "4) MS Office document"], "correct_answer": "2"},
            {"question_text": "What do you call a computer on a network that requests files from another computer?", "choices": ["1) A client", "2) A host", "3) A router", "4) A web server"], "correct_answer": "1"},
            {"question_text": "The Battle of Plassey was fought in?", "choices": ["1) 1757", "2) 1782", "3) 1748", "4) 1764"], "correct_answer": "1"},
            {"question_text": "Oscar Awards are associated with", "choices": ["1) Literature", "2) Films", "3) Science", "4) Music"], "correct_answer": "2"},
            {"question_text": "The ratio of width of our National flag to its length is?", "choices": ["1) 3:5", "2) 2:3", "3) 2:4", "4) 3:4"], "correct_answer": "2"},
            {"question_text": "Which of the following is the capital of Arunachal Pradesh?", "choices": ["1) Itanagar", "2) Dispur", "3) Imphal", "4) Panaji"], "correct_answer": "1"},
            {"question_text": "The purest form of iron is", "choices": ["1) Wrought iron", "2) Steel", "3) Pig iron", "4) Nickel steel"], "correct_answer": "1"},
            {"question_text": "The World's Largest desert is", "choices": ["1) Thar", "2) Kalahari", "3) Sahara", "4) Sonoran"], "correct_answer": "3"},
            {"question_text": "Who invented the BALLPOINT PEN?", "choices": ["1) Biro Brothers", "2) Waterman Brothers", "3) Bicc Brothers", "4) Write Brothers"], "correct_answer": "1"},
            {"question_text": "In which year of First World War Germany declared war on Russia and France?", "choices": ["1) 1914", "2) 1915", "3) 1916", "4) 1917"], "correct_answer": "1"},
            {"question_text": "Which of the following is an example of a database management system?", "choices": ["1) MySQL", "2) MongoDB", "3) Oracle", "4) All of the above"], "correct_answer": "4"},
            {"question_text": "What is the National Name of Japan?", "choices": ["1) Polska", "2) Hellas", "3) Drukyul", "4) Nippon"], "correct_answer": "4"},
            {"question_text": "How many times has Brazil won the World Cup Football Championship?", "choices": ["1) Four times", "2) Two times", "3) Five times", "4) Three times"], "correct_answer": "3"},
            {"question_text": "In which year was Alaska sold to the U.S.?", "choices": ["1) 1867", "2) 1868", "3) 1856", "4) 1857"], "correct_answer": "1"},
            {"question_text": "Which of the following is the capital of Uttarakhand?", "choices": ["1) Dispur", "2) Dehradun", "3) Panaji", "4) Kolkata"], "correct_answer": "2"},
            {"question_text": "Where was the electricity supply first introduced in India?", "choices": ["1) Kolkata", "2) Darjeeling", "3) Mumbai", "4) Chennai"], "correct_answer": "2"},
        ] + self.owner_questions_gk

    def generate_mr_questions(self):
        return [
            {"question_text": "What will come in place of question mark (?) in the following series? 3, 5, 8, ?, 15, 21", "choices": ["1) 10", "2) 11", "3) 12", "4) 13"], "correct_answer": "2"},
            {"question_text": "If 'CAT' is coded as '3120', then 'DOG' is coded as?", "choices": ["1) 41715", "2) 41575", "3) 41705", "4) 41725"], "correct_answer": "3"},
            {"question_text": "What comes next in the series: 2, 6, 12, 20, ?", "choices": ["1) 28", "2) 30", "3) 32", "4) 36"], "correct_answer": "1"},
            {"question_text": "What will come in place of question mark (?) in the following series? 7, 14, 28, 56, ?", "choices": ["1) 72", "2) 112", "3) 96", "4) 84"], "correct_answer": "2"},
            {"question_text": "What is the missing number in the sequence: 1, 4, 9, 16, ?", "choices": ["1) 25", "2) 36", "3) 49", "4) 64"], "correct_answer": "1"},
            {"question_text": "Which number logically follows this series: 4, 6, 9, 6, 14, 6, ?", "choices": ["1) 17", "2) 19", "3) 20", "4) 21"], "correct_answer": "3"},
            {"question_text": "If 'BEHOLD' is coded as 'AFGKNC', how is 'ENGLISH' coded?", "choices": ["1) DMFHKRG", "2) FMOJRTK", "3) FNMHRTK", "4) FNKHRTK"], "correct_answer": "4"},
            {"question_text": "What comes next in the series: 1, 4, 8, 13, 19, ?", "choices": ["1) 26", "2) 25", "3) 27", "4) 24"], "correct_answer": "1"},
            {"question_text": "Which number should come next in the series: 2, 3, 5, 8, 12, ?", "choices": ["1) 17", "2) 18", "3) 19", "4) 20"], "correct_answer": "1"},
            {"question_text": "If 'CONDITION' is coded as 'XLMWRGMP', how is 'IMPORTANT' coded?", "choices": ["1) NROTVIYXM", "2) YMVXLIZGR", "3) XLIZGRNRO", "4) LIZGRXLIZ"], "correct_answer": "3"},
            {"question_text": "What will come in place of question mark (?) in the following series? 15, 31, 63, ?, 255", "choices": ["1) 129", "2) 127", "3) 125", "4) 123"], "correct_answer": "2"},
            {"question_text": "If 'MOBILE' is coded as 'OMFCKG', how is 'DEVICE' coded?", "choices": ["1) FGXKH", "2) FGBIKH", "3) FGYKGH", "4) FGIKGH"], "correct_answer": "4"},
            {"question_text": "Which number logically follows this series: 2, 5, 10, 17, 26, ?", "choices": ["1) 37", "2) 38", "3) 39", "4) 40"], "correct_answer": "1"},
            {"question_text": "If 'HOUSE' is coded as 'IPVRF', how is 'GRADE' coded?", "choices": ["1) FSBCD", "2) HSBCD", "3) HTBCD", "4) HSACC"], "correct_answer": "3"},
            {"question_text": "What comes next in the series: 2, 3, 6, 11, 18, ?", "choices": ["1) 28", "2) 27", "3) 26", "4) 29"], "correct_answer": "1"},
            {"question_text": "Which number should come next in the series: 1, 4, 9, 16, 25, ?", "choices": ["1) 36", "2) 37", "3) 38", "4) 39"], "correct_answer": "1"},
            {"question_text": "If 'TABLE' is coded as 'ZAMZN', how is 'CHAIR' coded?", "choices": ["1) IRLHM", "2) JSLIN", "3) ISLHM", "4) JSLHM"], "correct_answer": "4"},
            {"question_text": "What will come in place of question mark (?) in the following series? 12, 36, 108, ?, 972", "choices": ["1) 324", "2) 216", "3) 192", "4) 288"], "correct_answer": "1"},
            {"question_text": "If 'STAR' is coded as 'TUBS', how is 'MOON' coded?", "choices": ["1) NPPO", "2) NPOO", "3) NPQO", "4) NPRP"], "correct_answer": "1"},
            {"question_text": "Which number should come next in the series: 1, 3, 6, 10, 15, ?", "choices": ["1) 21", "2) 22", "3) 23", "4) 24"], "correct_answer": "1"},
            {"question_text": "If 'ENGLISH' is coded as 'FOHKSHI', how is 'MATHEMATICS' coded?", "choices": ["1) NBUFNFUOUDT", "2) NBUFNFUTODT", "3) NBUFNFUTODU", "4) NBUFNFOUODU"], "correct_answer": "2"},
            {"question_text": "What comes next in the series: 5, 12, 24, 43, ?", "choices": ["1) 69", "2) 57", "3) 59", "4) 66"], "correct_answer": "3"},
            {"question_text": "Which number logically follows this series: 4, 9, 16, 25, 36, ?", "choices": ["1) 49", "2) 50", "3) 51", "4) 52"], "correct_answer": "1"},
            {"question_text": "If 'DOCTOR' is coded as 'CQBNRM', how is 'NURSE' coded?", "choices": ["1) MVQSD", "2) MVQTDF", "3) MVQTC", "4) MVQTD"], "correct_answer": "1"},
            {"question_text": "Which number should come next in the series: 2, 6, 12, 20, 30, ?", "choices": ["1) 42", "2) 40", "3) 39", "4) 41"], "correct_answer": "1"},
            {"question_text": "If 'COMPUTER' is coded as 'FNORTCU', how is 'PRINTER' coded?", "choices": ["1) PRNTVIR", "2) PSNTIRV", "3) PRVTNSR", "4) PSNRITV"], "correct_answer": "2"},
            {"question_text": "What comes next in the series: 1, 2, 6, 24, ?", "choices": ["1) 72", "2) 120", "3) 36", "4) 48"],"correct_answer": "2"},
            {"question_text": "If 'CANDLE' is coded as 'DBOEND', how is 'LIGHT' coded?", "choices": ["1) KHKSU", "2) KHHST", "3) KHHSS", "4) KHHSTU"], "correct_answer": "3"},
            {"question_text": "Which number logically follows this series: 1, 1, 2, 6, 24, ?", "choices": ["1) 120", "2) 36", "3) 30", "4) 48"], "correct_answer": "1"},
            {"question_text": "If 'EXAM' is coded as 'FYBN', how is 'TEST' coded?", "choices": ["1) UFQU", "2) UFQV", "3) UFQR", "4) UFQP"], "correct_answer": "1"},
            {"question_text": "What comes next in the series: 2, 7, 14, 23, 34, ?", "choices": ["1) 47", "2) 45", "3) 44", "4) 48"], "correct_answer": "1"},
            {"question_text": "If 'SCHOOL' is coded as 'TRQNNK', how is 'UNIVERSITY' coded?", "choices": ["1) VNRJDWJSJV", "2) VNRJDWKSJW", "3) VNRJDWKSJV", "4) VNRJDWKSWJ"], "correct_answer": "3"},
            {"question_text": "What will come in place of question mark (?) in the following series? 5, 11, 23, 47, ?", "choices": ["1) 83", "2) 95", "3) 79", "4) 85"], "correct_answer": "3"},
            {"question_text": "What is the value of π?", "choices": ["1) 3.14", "2) 3.15", "3) 3.16", "4) 3.17"], "correct_answer": "1"},
            {"question_text": "What is the value of (2+3)*(4+5)?", "choices": ["1) 45", "2) 50", "3) 35", "4) 55"], "correct_answer": "3"},
            {"question_text": "What is the square root of 144?", "choices": ["1) 11", "2) 12", "3) 13", "4) 14"], "correct_answer": "2"},
            {"question_text": "What is 15% of 200?", "choices": ["1) 25", "2) 30", "3) 35", "4) 40"], "correct_answer": "2"},
            {"question_text": "What is the value of 3^3?", "choices": ["1) 9", "2) 18", "3) 27", "4) 36"], "correct_answer": "3"},
            {"question_text": "What is the value of 7*8?", "choices": ["1) 54", "2) 56", "3) 58", "4) 60"], "correct_answer": "2"},
            {"question_text": "What is 20% of 50?", "choices": ["1) 8", "2) 9", "3) 10", "4) 11"], "correct_answer": "3"},
            {"question_text": "What is the value of (4+5)*(6+7)?", "choices": ["1) 108", "2) 110", "3) 112", "4) 114"], "correct_answer": "3"},
            {"question_text": "What is the value of 9*9?", "choices": ["1) 80", "2) 81", "3) 82", "4) 83"], "correct_answer": "2"},
            {"question_text": "What is 10% of 500?", "choices": ["1) 50", "2) 55", "3) 60", "4) 65"], "correct_answer": "1"},
            {"question_text": "What is the value of 8/4?", "choices": ["1) 2", "2) 3", "3) 4", "4) 5"], "correct_answer": "1"},
            {"question_text": "What is the value of 7-5?", "choices": ["1) 1", "2) 2", "3) 3", "4) 4"], "correct_answer": "2"},
            {"question_text": "What is the value of 3+3?", "choices": ["1) 5", "2) 6", "3) 7", "4) 8"], "correct_answer": "2"},
            {"question_text": "What is the value of 100/4?", "choices": ["1) 20", "2) 25", "3) 30", "4) 35"], "correct_answer": "2"},
            {"question_text": "What is the value of 5*5?", "choices": ["1) 20", "2) 25", "3) 30", "4) 35"], "correct_answer": "2"},
            {"question_text": "What is the value of 2^4?", "choices": ["1) 8", "2) 16", "3) 32", "4) 64"], "correct_answer": "2"},
            {"question_text": "What is the value of 6*7?", "choices": ["1) 40", "2) 41", "3) 42", "4) 43"], "correct_answer": "3"},
            {"question_text": "What is the value of 12*12?", "choices": ["1) 142", "2) 143", "3) 144", "4) 145"], "correct_answer": "3"},
            {"question_text": "What is the value of 9/3?", "choices": ["1) 2", "2) 3", "3) 4", "4) 5"], "correct_answer": "2"},
            {"question_text": "What is the value of 7+5?", "choices": ["1) 10", "2) 11", "3) 12", "4) 13"], "correct_answer": "3"},
            {"question_text": "What is the value of 5-3?", "choices": ["1) 1", "2) 2", "3) 3", "4) 4"], "correct_answer": "2"},
            {"question_text": "What is the value of 2*2?", "choices": ["1) 3", "2) 4", "3) 5", "4) 6"], "correct_answer": "2"},
            {"question_text": "What is the value of 8*8?", "choices": ["1) 62", "2) 63", "3) 64", "4) 65"], "correct_answer": "3"},
            {"question_text": "What is the value of 15/3?", "choices": ["1) 3", "2) 4", "3) 5", "4) 6"], "correct_answer": "3"},
            {"question_text": "What is the value of 7+7?", "choices": ["1) 12", "2) 13", "3) 14", "4) 15"], "correct_answer": "3"},
            {"question_text": "What is the value of 9-6?", "choices": ["1) 1", "2) 2", "3) 3", "4) 4"], "correct_answer": "3"},
            {"question_text": "What is the value of 10*10?", "choices": ["1) 90", "2) 95", "3) 100", "4) 105"], "correct_answer": "3"},
            {"question_text": "What is the value of 25% of 200?", "choices": ["1) 40", "2) 45", "3) 50", "4) 55"], "correct_answer": "3"},
            {"question_text": "What is the value of 100*2?", "choices": ["1) 150", "2) 200", "3) 250", "4) 300"], "correct_answer": "2"},
            {"question_text": "What is the value of 10/2?", "choices": ["1) 3", "2) 4", "3) 5", "4) 6"], "correct_answer": "3"},
            {"question_text": "What is the value of 5+3?", "choices": ["1) 7", "2) 8", "3) 9", "4) 10"], "correct_answer": "2"},
            {"question_text": "What will come in place of question mark (?) in the following series? 3, 5, 8, ?, 15, 21", "choices": ["1) 10", "2) 11", "3) 12", "4) 13"], "correct_answer": "2"},
            {"question_text": "If 'CAT' is coded as '3120', then 'DOG' is coded as?", "choices": ["1) 41715", "2) 41575", "3) 41705", "4) 41725"], "correct_answer": "3"},
            {"question_text": "What comes next in the series: 2, 6, 12, 20, ?", "choices": ["1) 28", "2) 30", "3) 32", "4) 36"], "correct_answer": "1"},
            {"question_text": "What will come in place of question mark (?) in the following series? 7, 14, 28, 56, ?", "choices": ["1) 72", "2) 112", "3) 96", "4) 84"], "correct_answer": "2"},
            {"question_text": "What is the missing number in the sequence: 1, 4, 9, 16, ?", "choices": ["1) 25", "2) 36", "3) 49", "4) 64"], "correct_answer": "1"},
            {"question_text": "Which number logically follows this series: 4, 6, 9, 6, 14, 6, ?", "choices": ["1) 17", "2) 19", "3) 20", "4) 21"], "correct_answer": "3"},
            {"question_text": "If 'BEHOLD' is coded as 'AFGKNC', how is 'ENGLISH' coded?", "choices": ["1) DMFHKRG", "2) FMOJRTK", "3) FNMHRTK", "4) FNKHRTK"], "correct_answer": "4"},
            {"question_text": "What comes next in the series: 1, 4, 8, 13, 19, ?", "choices": ["1) 26", "2) 25", "3) 27", "4) 24"], "correct_answer": "1"},
            {"question_text": "Which number should come next in the series: 2, 3, 5, 8, 12, ?", "choices": ["1) 17", "2) 18", "3) 19", "4) 20"], "correct_answer": "1"},
            {"question_text": "If 'CONDITION' is coded as 'XLMWRGMP', how is 'IMPORTANT' coded?", "choices": ["1) NROTVIYXM", "2) YMVXLIZGR", "3) XLIZGRNRO", "4) LIZGRXLIZ"], "correct_answer": "3"},
            {"question_text": "What will come in place of question mark (?) in the following series? 15, 31, 63, ?, 255", "choices": ["1) 129", "2) 127", "3) 125", "4) 123"], "correct_answer": "2"},
            {"question_text": "If 'MOBILE' is coded as 'OMFCKG', how is 'DEVICE' coded?", "choices": ["1) FGXKH", "2) FGBIKH", "3) FGYKGH", "4) FGIKGH"], "correct_answer": "4"},
            {"question_text": "Which number logically follows this series: 2, 5, 10, 17, 26, ?", "choices": ["1) 37", "2) 38", "3) 39", "4) 40"], "correct_answer": "1"},
            {"question_text": "If 'HOUSE' is coded as 'IPVRF', how is 'GRADE' coded?", "choices": ["1) FSBCD", "2) HSBCD", "3) HTBCD", "4) HSACC"], "correct_answer": "3"},
            {"question_text": "What comes next in the series: 2, 3, 6, 11, 18, ?", "choices": ["1) 28", "2) 27", "3) 26", "4) 29"], "correct_answer": "1"},
            {"question_text": "Which number should come next in the series: 1, 4, 9, 16, 25, ?", "choices": ["1) 36", "2) 37", "3) 38", "4) 39"], "correct_answer": "1"},
            {"question_text": "If 'TABLE' is coded as 'ZAMZN', how is 'CHAIR' coded?", "choices": ["1) IRLHM", "2) JSLIN", "3) ISLHM", "4) JSLHM"], "correct_answer": "4"},
            {"question_text": "What will come in place of question mark (?) in the following series? 12, 36, 108, ?, 972", "choices": ["1) 324", "2) 216", "3) 192", "4) 288"], "correct_answer": "1"},
            {"question_text": "If 'FUN' is coded as '2171514', how is 'QUIZ' coded?", "choices": ["1) 177159", "2) 18192126", "3) 1817218", "4) 18201926"], "correct_answer": "2"},
        ] + self.owner_questions_mr

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = QuizGame(root)
    root.mainloop()
