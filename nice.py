from nicegui import ui, app
import random

app.add_static_files('/static', './sounds')
# ===============================
# BACKGROUND + FONT
# ===============================
ui.add_head_html("""
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap" rel="stylesheet">
<style>
body {
    background: url('https://wallpapers.com/images/hd/hogwarts-background-nc443t2fdplc1idw.jpg') no-repeat center center fixed;
    background-size: cover;
    font-family: 'Cinzel', serif;
    color: black;
    font-size: 24px;             
}
.card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 20px;
    margin-top: 20px;
}
.btn {
    background: #f0d857;
    color: black;
    border-radius: 10px;
    padding: 10px;
    width: 100%;
    cursor: pointer;
    transition: background 0.3s;
    font-family: 'Cinzel', serif;
    font-size: 20px;             
}
.btn:hover {
    background: #e6c84f;
}
</style>
""")


ui.add_head_html("""
<audio id="bg-music" loop>
    <source src="/static/Hedwig's Theme.mp3" type="audio/mpeg">
</audio>
""")

ui.add_head_html("""
<style>
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}
</style>
""")

# ===============================
# HEADER + START QUIZ
# ===============================
ui.label("🏰 Hogwarts Sorting Ceremony").classes("text-4xl text-yellow-300 text-center")
ui.label("✨ The Sorting Hat will decide your destiny...").classes("text-white text-center")

# ===============================
# DATA
# ===============================
quiz_pool = [
    {"question": "You enter the Dark Corridor… what do you do?",
     "options": {
         "Bring someone you trust": "Loyalty",
         "Open the door immediately": "Bravery",
         "Listen and analyze the sound": "Intelligence",
         "Use a risky spell": "DarkArts"
     }},
    {"question": "Defense Against the Dark Arts lesson begins, your move?",
     "options": {
         "Volunteer immediately": "Bravery",
         "Suggest a clever plan": "Intelligence",
         "Encourage your friend": "Loyalty",
         "Ask to use an advanced offensive spell": "Ambition"
     }},
    {"question": "Ravenclaw Tower Riddle appears, how do you solve it?",
     "options": {
         "Solve it yourself": "Intelligence",
         "Invent a creative answer": "Creativity",
         "Use a spell to bypass the puzzle": "Ambition",
         "Ask for help from someone who knows riddles": "Loyalty"
     }},
    {"question": "Quidditch Team Selection: what's your role?",
     "options": {
         "Play immediately": "Bravery",
         "Play skillfully": "Quidditch",
         "Nominate another player": "Loyalty",
         "Play to prove yourself": "Ambition"
     }},
    {"question": "You find a Forbidden Book in the Library, what do you do?",
     "options": {
         "Open it no matter what": "Ambition",
         "Solve its magical chains": "Intelligence",
         "Report it to the librarian": "Loyalty",
         "Use it to experiment with a spell": "DarkArts"
     }},
    {"question": "A student is struggling in class, how do you help?",
     "options": {
         "Teach step by step until they succeed": "Loyalty",
         "Give a creative example": "Creativity",
         "Show your skills to the teacher": "Ambition",
         "Encourage them to try again": "Bravery"
     }},
    {"question": "Chamber of Secrets encounter: a giant serpent appears, what's your move?",
     "options": {
         "Face the giant serpent": "Bravery",
         "Study the symbols": "Intelligence",
         "Bring a team": "Loyalty",
         "Speak Parseltongue": "DarkArts"
     }},
    {"question": "Dueling Practice: your strategy?",
     "options": {
         "Fast attack": "Dueling",
         "Smart defense": "Intelligence",
         "Protect the team": "Loyalty",
         "Use an impressive style": "Creativity"
     }},
    {"question": "Invent a New Spell: your approach?",
     "options": {
         "Create a completely new spell": "Creativity",
         "Create a powerful offensive spell": "DarkArts",
         "Create a spell useful for everyone": "Loyalty",
         "Create a complex, clever spell": "Intelligence"
     }},
    {"question": "Forbidden Forest Creature: how do you act?",
     "options": {
         "Try to heal it": "Loyalty",
         "Observe it from afar": "Intelligence",
         "Escape and warn the castle": "Bravery",
         "Experiment with a dark healing spell": "DarkArts"
     }},
    {"question": "Lead a Team: your decision?",
     "options": {
         "Accept with confidence": "Ambition",
         "Accept but with a careful plan": "Intelligence",
         "Refuse and nominate someone better": "Loyalty",
         "Accept because you're not afraid of responsibility": "Bravery"
     }},
    {"question": "Sudden Attack Spell: how do you react?",
     "options": {
         "Protect a friend": "Loyalty",
         "Block immediately": "Dueling",
         "Analyze the opponent": "Intelligence",
         "Counterattack with a strong spell": "Ambition"
     }},
    {"question": "Mysterious Chest in the dungeon, what do you do?",
     "options": {
         "Open it immediately": "Bravery",
         "Analyze the music": "Intelligence",
         "Bring someone with you": "Loyalty",
         "Bind it to mysterious spells": "DarkArts"
     }},
    {"question": "Choosing a Broom: which do you pick?",
     "options": {
         "The fastest broom": "Ambition",
         "Balanced and safe broom": "Intelligence",
         "Broom that helps the team": "Loyalty",
         "Broom that fits your creative style": "Quidditch"
     }},
    {"question": "Rumor of Danger: what's your move?",
     "options": {
         "Go check it yourself": "Bravery",
         "Gather information first": "Intelligence",
         "Reassure your friends": "Loyalty",
         "Take advantage of the chaos": "Ambition"
     }},
    {"question": "Forbidden Spells: what do you do?",
     "options": {
         "Study the dark spells": "DarkArts",
         "Analyze them later": "Intelligence",
         "Lock the room and prevent access": "Loyalty",
         "Use one to test your power": "Ambition"
     }},
    {"question": "Friend in Trouble: how do you act?",
     "options": {
         "Help immediately": "Loyalty",
         "Think before acting": "Intelligence",
         "Help and take the opportunity to show yourself": "Ambition",
         "Encourage them to face the problem bravely": "Bravery"
     }},
    {"question": "Secret Mission: your approach?",
     "options": {
         "Accept immediately": "Bravery",
         "Ask lots of questions first": "Intelligence",
         "Take a friend with you": "Loyalty",
         "Use the mission for fame or advancement": "Ambition"
     }},
    {"question": "Quidditch Practice: how do you play?",
     "options": {
         "Try risky move immediately": "Bravery",
         "Execute skillfully": "Quidditch",
         "Suggest a creative adjustment": "Creativity",
         "Refuse because it's not useful": "Loyalty"
     }},
    {"question": "Final Battle: your role?",
     "options": {
         "Fight at the front": "Bravery",
         "Think of a clever plan": "Intelligence",
         "Protect everyone around": "Loyalty",
         "Use your strongest spell no matter how dark": "DarkArts"
     }}
]

traits = ["Bravery","Intelligence","Loyalty","Ambition","Creativity","Dueling","DarkArts","Quidditch"]

houses = {
    "Gryffindor": ["Bravery", "Dueling"],
    "Ravenclaw": ["Intelligence", "Creativity"],
    "Hufflepuff": ["Loyalty"],
    "Slytherin": ["Ambition", "DarkArts"]
}

house_emojis = {"Gryffindor":"🦁","Ravenclaw":"🦅","Hufflepuff":"🦡","Slytherin":"🐍"}
house_colors = {"Gryffindor":"#740001", "Ravenclaw":"#0E1A40", "Hufflepuff":"#FFD800", "Slytherin":"#1A472A"}

# ===============================
# QUIZ STATE
# ===============================
num_questions = 10
random_quiz = []
current_q = 0
answers = {}

# ===============================
# UI CONTAINER
# ===============================
question_container = ui.column().classes("items-center justify-center w-full max-w-xl mx-auto")

# ===============================
# FUNCTION TO stop MUSIC 
# ===============================
def stop_music():
    ui.run_javascript("""
        var audio = document.getElementById('bg-music');
        if (audio) {
            audio.pause();
            audio.currentTime = 0;
        }
    """)
# ===============================
# SELECT NUMBER OF QUESTIONS 
# ===============================
def ask_number_of_questions():
    question_container.clear()
    with question_container:
        ui.label("🎲 How many questions do you want to answer?").classes("text-white text-xl")
        
        num_slider = ui.slider(min=8, max=20, value=10).props('label-always')
        
        num_slider.on("update:modelValue")
        
        def start_quiz():
            global num_questions, random_quiz
            num_questions = int(num_slider.value)
            random_quiz = random.sample(quiz_pool, num_questions)

            ui.run_javascript("""
                 var audio = document.getElementById('bg-music');
                if (audio) {
                audio.currentTime = 0;
                audio.volume = 1;
                audio.play();
                 }
                 """)
            show_question()
        
        ui.button("Start Quiz ✨", on_click=start_quiz).classes("btn mt-4 text-lg font-bold")

# ===============================
# IMAGES FOR QUESTIONS
# ===============================
question_images = [
    r"images\dobyy.png",
    r"images\expresss.png",
    r"images\golden_snitchh.png",
    r"images\volt.png",
    r"images\hedwigg.png",
    r"images\hippogrifff.png",
    r"images\wand.png",
    r"images\dragonn.png",
    r"images\phounixx.png",
    r"images\basilisk.png",
    r"images\broomstick.png",
]

prev_img = None
def get_random_image():
    global prev_img
    img = random.choice(question_images)
    while img == prev_img:  
        img = random.choice(question_images)
    prev_img = img
    return img

# ===============================
# SHOW QUESTION WITH IMAGE
# ===============================
def show_question():
    question_container.clear()
    global current_q

    if current_q >= len(random_quiz):
        show_result()
        return

    q = random_quiz[current_q]

    with question_container:
        ui.label(f"Question {current_q + 1}/{len(random_quiz)}").classes("text-white text-lg")

        img_path = question_images[current_q % len(question_images)]
        
        with ui.row().style("align-items: flex-start; gap: 20px; margin-top:10px;"):
            ui.label(q["question"]).classes("text-white text-2xl").style("max-width:70%")
            ui.image(img_path).style(
                "width:150px; height:150px; object-fit:cover; animation: float 3s ease-in-out infinite;"
            )

        def select(choice):
            global current_q
            answers[current_q] = choice
            current_q += 1
            show_question()

        for option in q["options"].keys():
            ui.button(option, on_click=lambda o=option: select(o)).classes("btn mt-2")

def show_result():

    stop_music()

    question_container.clear()
    scores = {t: 0 for t in traits}

    for i, q in enumerate(random_quiz):
        ans = answers.get(i)
        if ans is not None:
            trait = q["options"][ans]
            if trait in scores:
                scores[trait] += 1

    house_scores = {h: sum(scores.get(t, 0) for t in traits_list) for h, traits_list in houses.items()}
    best_house = max(house_scores, key=house_scores.get)

    house_sounds = {
        "Gryffindor": r"/static/gryffindor.mp3",
        "Slytherin": r"/static/slytherin.mp3",
        "Hufflepuff": r"/static/hufflepuff.mp3",
        "Ravenclaw": r"/static/ravenclaw.mp3"
    }

    with question_container:
        ui.label("✨ Your Destiny ✨").classes("text-3xl text-yellow-300 mb-4")

        sorting_hat_image = ui.image(r"images\sorting.png").classes("w-64 cursor-pointer")

        house_audio = {house: ui.audio(path, autoplay=False).style("display:none;") 
                       for house, path in house_sounds.items()}

        revealed = {"done": False}

        def reveal_house(e):
            if revealed["done"]:
                return  
            revealed["done"] = True

            ui.run_javascript(f"""
                var audio = new Audio('{house_sounds[best_house]}');
                audio.play();
                """)

            ui.label(f"🏠 You belong to {best_house}!").classes("text-2xl text-white mt-4")

            sorting_hat_image.classes("animate-bounce")

            ui.button("Restart", on_click=restart).classes("btn mt-4")

        sorting_hat_image.on("click", reveal_house)

def restart():
    global current_q, answers, random_quiz
    current_q = 0
    answers = {}
    random_quiz = []
    ask_number_of_questions()

ask_number_of_questions()

ui.run()