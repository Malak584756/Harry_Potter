from nicegui import ui, app
import random
import pickle
import numpy as np

with open("hogwarts_model.pkl", "rb") as f:
    log_reg = pickle.load(f)

with open("hogwarts_encoder.pkl", "rb") as f:
    le = pickle.load(f)

app.add_static_files('/static', './sounds')
app.add_static_files('/images', './images')

ui.add_head_html("""
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap" rel="stylesheet">
<style>
body {
    background: url('https://wallpapers.com/images/hd/hogwarts-background-nc443t2fdplc1idw.jpg') no-repeat center center fixed;
    background-size: cover;
    font-family: 'Cinzel', serif;
    color: white;
}
.btn {
    background: #f0d857;
    color: black;
    border-radius: 12px;
    padding: 14px;
    cursor: pointer;
    transition: 0.3s;
    font-family: 'Cinzel', serif;
    font-size: 18px;
    width: 100%;
    height: 60px;              
    display: flex;
    align-items: center;       
    justify-content: center;   
    text-align: center;
    margin-top: 10px;             
}
.btn:hover {
    background: #e6c84f;
    transform: scale(1.05);
}
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}
</style>
""")

ui.add_head_html("""
<audio id="bg-music" loop>
    <source src="/static/Hedwig's Theme.mp3" type="audio/mpeg">
</audio>
""")

quiz_pool = [
{
        "question": "A cursed creature appears in the hallway; what’s your move?",
        "options": {
            "Use a dark detection spell to identify it": "Dark Arts Knowledge",
            "Cast a precise defensive counter": "Dueling Skills",
            "Distract it with a creative illusion": "Creativity",
            "Make a solid plan to catch him": "Intelligence"
        }
    },

{
	"question": "A Bludger goes out of control during practice; how do you react?",
        "options": {
            "Intercept it mid‑air with a clean maneuver": "Quidditch Skills",
            "Blast it away using a spell": "Dark Arts Knowledge",
            "Create a magical lure to redirect it": "Creativity",
            "Dash forward to shield a teammate from its path": "Bravery"
        }
    },
{    
	"question": "A forbidden spellbook locks itself magically; what do you do?",
        "options": {
            "Decode the dark runes on its cover": "Dark Arts Knowledge",
            "Force it open with a controlled strike": "Dueling Skills",
            "Craft an unusual unlocking technique": "Creativity",
            "Examine the mechanism carefully": "Intelligence"
        }
    },
{
	"question": "During a duel, your opponent suddenly vanishes in smoke; what's your response?",
        "options": {
            "Use dark sensing magic to track him": "Dark Arts Knowledge",
            "Prepare a defensive stance instantly": "Dueling Skills",
            "Create a creative trap spell": "Creativity",
            "Call for backup in case it’s serious": "Loyalty"
        }
    },
{
        "question": "You must retrieve a magical item floating high above a cliff.",
        "options": {
            "Fly up with perfect balance": "Quidditch Skills",
            "Shoot a precise spell to lower it": "Dark Arts Knowledge",
            "Build a creative floating platform": "Creativity",
            "Study the wind pattern first": "Intelligence"
        }
    },
{
        "question": "You encounter ancient dark symbols carved into stone.",
        "options": {
            "Interpret the symbols’ origins": "Dark Arts Knowledge",
            "Blast the stone open to break the enchantment": "Dueling Skills",
            "Sketch a creative counter‑pattern": "Creativity",
            "Take notes for later research": "Intelligence"
        }
    },
{
        "question": "You’re challenged to design a new magical combat spell.",
        "options": {
            "Combine shadow magic with power": "Dark Arts Knowledge",
            "Make a fast duel‑focused strike spell": "Dueling Skills",
            "Invent a creative multidirectional effect": "Creativity",
            "Design a spell to gain recognition": "Ambition"
        }
    },
{
        "question": "A broom malfunction happens mid‑air; how do you fix it?",
        "options": {
            "Stabilize yourself with expert flying": "Quidditch Skills",
            "Force‑cast a repairing spell": "Dueling Skills",
            "Modify the broom using a creative charm": "Creativity",
            "Land and analyze it calmly": "Intelligence"
        }
    },
{
        "question": "Quidditch Tryouts begin; what's your move?",
        "options": {
            "Show perfect broom control": "Quidditch Skills",
            "Step forward bravely": "Bravery",
            "Suggest a warm‑up plan": "Intelligence",
            "Encourage teammates": "Loyalty"
        }
    },
{
        "question": "Wind becomes very strong mid‑match; what do you do?",
        "options": {
            "Adjust your flying angle": "Quidditch Skills",
            "Hold firm and push through": "Bravery",
            "Analyze wind direction": "Intelligence",
            "Use a light defensive spell to stabilize your broom against the gusts": "Dueling Skills"
        }
    },
{
        "question": "During class, a dangerous spell goes wrong; your reaction?",
        "options": {
            "Rush forward to shield others": "Bravery",
            "Help your partner recover": "Loyalty",
            "Step in to impress the professor": "Ambition",
            "Use swift broom movement to avoid the blast": "Quidditch Skills"
        }
    },
{
        "question": "A loud scream echoes from the Forbidden Forest; what do you do?",
        "options": {
            "Run toward the sound to help": "Bravery",
            "Go call others for support": "Loyalty",
            "Investigate hoping to prove yourself": "Ambition",
            "Scout the area quickly from above": "Quidditch Skills"
        }
    },
{
        "question": "You see a first-year student being bullied.",
        "options": {
            "Step in directly to stop it": "Bravery",
            "Stay with the student until they're okay": "Loyalty",
            "Use the situation to show leadership": "Ambition",
            "Distract the bullies with a quick broom maneuver": "Quidditch Skills"
        }
    },
{ 
	"question": "Defense Against the Dark Arts lesson begins, your move?",
          "options": {
            "Volunteer immediately": "Bravery",
            "Suggest a clever plan": "Intelligence",
            "Encourage your friend": "Loyalty",
            "Ask to use an advanced offensive spell": "Ambition"
          }
    },
{
	"question": "Ravenclaw Tower Riddle appears, how do you solve it?",
    	"options": {
 	    "Solve it yourself": "Intelligence",
               "Invent a creative answer": "Creativity",
               "Use a spell to bypass the puzzle": "Ambition",
               "Stand your ground and attempt the riddle bravely": "Bravery"
          }
    },

{
        "question": "Professor challenges you to handle a cursed artifact.",
        "options": {
            "Step forward confidently": "Bravery",
            "Use a controlled disarming spell": "Dueling Skills",
            "Tap into forbidden knowledge to weaken it": "Dark Arts Knowledge",
            "Volunteer to show your skills": "Ambition"
        }
    },

{
        "question": "You find a ritual circle drawn on the floor.",
        "options": {
            "Step inside to inspect it closely": "Bravery",
            "Disrupt the circle safely with a spell": "Dueling Skills",
            "Decode the runes using dark knowledge": "Dark Arts Knowledge",
            "Use the discovery to boost your reputation": "Ambition"
        }
    },
{
	"question": "Lead a Team: your decision?",
         "options": {
             "Accept with confidence": "Ambition",
             "Accept but with a careful plan": "Intelligence",
             "Refuse and nominate someone better": "Loyalty",
             "Accept because you're not afraid of responsibility": "Bravery"
         }
    },
{
	"question": "Final Battle: your role?",
        "options": {
             "Fight at the front": "Bravery",
             "Think of a clever plan": "Intelligence",
             "Protect everyone around": "Loyalty",
             "Use your strongest spell no matter how dark": "Dark Arts Knowledge"
        }
    },

{
        "question": "You find an ancient wand with unstable energy.",
        "options": {
            "Use it to gain an edge": "Ambition",
            "Stabilize it with duel technique": "Dueling Skills",
            "Enhance it with a custom enchantment": "Creativity",
            "Test its energy mid‑air": "Quidditch Skills"
        }
    },

]

traits = ["Bravery","Intelligence","Loyalty","Ambition","Dark Arts Knowledge","Quidditch Skills","Dueling Skills","Creativity"]

house_sounds = {
    "Gryffindor": "/static/gryffindor.mp3",
    "Slytherin": "/static/slytherin.mp3",
    "Hufflepuff": "/static/hufflepuff.mp3",
    "Ravenclaw": "/static/ravenclaw.mp3"
}

house_images = {
    "Gryffindor": "/images/gryffindor.png",
    "Slytherin": "/images/slytherin.png",
    "Hufflepuff": "/images/hufflepuff.png",
    "Ravenclaw": "/images/ravenclaw.png"
}

house_tips = {
    "Gryffindor": "Ahh… daring, nerve, and chivalry!",
    "Slytherin": "Cunning and ambition… I see greatness!",
    "Ravenclaw": "A sharp mind… thirst for knowledge!",
    "Hufflepuff": "Loyal and true… a kind heart!"
}

question_images = [
    "/images/dobyy.png","/images/expresss.png","/images/golden_snitchh.png",
    "/images/volt.png","/images/hedwigg.png","/images/dragonn.png",
    "/images/hippogrifff.png","/images/phounixx.png",
]

random_quiz = []
current_q = 0
answers = {}  

question_container = ui.column().classes("items-center w-full max-w-xl mx-auto")

# Plays the background music (Hedwig Theme)
def play_music():
    ui.run_javascript("""
        var audio = document.getElementById('bg-music');
        if(audio){ audio.play(); audio.volume=0.5; }
    """)

# Stops the music and resets it to the beginning
def stop_music():
    ui.run_javascript("""
        var audio = document.getElementById('bg-music');
        if(audio){ audio.pause(); audio.currentTime=0; }
    """)

# Preloads images in the background for faster performance
def preload_images():
    images_to_preload = question_images + list(house_images.values()) + ["/images/sorting.png"]
    images_js_array = str(images_to_preload).replace("'", '"')
    ui.run_javascript(f"""
        var images = {images_js_array};
        images.forEach(src => {{ var img = new Image(); img.src = src; }});
    """)

ui.timer(0, preload_images, once=True)

# Clicking the hat starts the quiz
def start_screen():
    question_container.clear()
    with question_container:
        ui.label("🏰 Hogwarts Sorting Ceremony").classes("text-5xl text-yellow-300 text-center")
        ui.label("✨ Click the Sorting Hat to start the quiz...").classes("text-white text-center mt-2")
        sort_hat = ui.image("/images/sorting.png").classes("w-64 cursor-pointer animate-bounce mt-6")

        def start_quiz(e):
            global random_quiz, current_q, answers
            current_q = 0
            answers.clear()
            random_quiz = quiz_pool.copy()
            random.shuffle(random_quiz)
            play_music()
            show_question()

        sort_hat.on("click", start_quiz)

def show_question():
    # Displays the current question and its options
    question_container.clear()
    global current_q

    # If all questions are answered → show final result
    if current_q >= len(random_quiz):
        show_result(final=True)
        return

    q = random_quiz[current_q]

    with question_container:
        # Small sorting hat (allows early result after 10 answers)
        small_hat = ui.image("/images/sorting.png")\
            .classes("w-32 cursor-pointer animate-bounce")\
            .style("position: fixed; top:20px; right:20px; z-index:1000;")

        # Prevent showing result before answering at least 10 questions
        def try_show_result():
            if len(answers) >= 10:
                show_result(final=False)
            else:
                ui.notify("Please answer at least 10 questions first.", color="red")

        small_hat.on("click", lambda e: try_show_result())

        ui.label(f"Question {current_q+1}/{len(random_quiz)}").classes("text-lg text-yellow-200 mt-2")

        with ui.row().classes("w-full mt-4 items-center justify-between"):
            ui.label(q["question"]).classes("text-2xl flex-1")\
                .style("""
                    background: rgba(0,0,0,0.5);
                    padding: 12px;
                    border-radius: 12px;
                """)
            ui.image(question_images[current_q % len(question_images)])\
                .style("width:140px; height:140px; animation:float 3s infinite;")

        options = list(q["options"].keys())
        random.shuffle(options)

        for option in options:
            ui.button(option, on_click=lambda o=option, q=q: select(q, o))\
                .classes("btn w-full mt-3")

# Stores the user's answer and moves to the next question
def select(q, choice):
    global current_q
    answers[q["question"]] = choice 
    current_q += 1
    show_question()

# Calculates scores and predicts the Hogwarts house
def show_result(final=True):
    stop_music()
    question_container.clear()

    # Count scores for each trait
    scores = {t: 0 for t in traits}
    for q in random_quiz:
        ans = answers.get(q["question"])
        if ans:
            scores[q["options"][ans]] += 1

    # Normalize scores to range 1–10
    for key, value in scores.items():
        if key == "Dueling Skills":
            scores[key] = max(0, min(10, value))
        else:
            scores[key] = max(1, min(10, value))   

    # Predict the house
    features = np.array([[scores[t] for t in traits]])
    pred = log_reg.predict(features)
    best_house = le.inverse_transform(pred)[0]
    print(best_house)

    # Display  result
    with question_container:
        ui.label("🎩 Your House is...").classes("text-3xl text-yellow-300 mt-6")
        ui.image(house_images[best_house]).classes("w-64 mx-auto mt-4")
        ui.label(house_tips[best_house]).classes("text-xl text-yellow-200 mt-4 text-center")

        ui.run_javascript(f"var audio = new Audio('{house_sounds[best_house]}'); audio.play();")
        ui.button("Restart", on_click=restart).classes("btn mt-4")
def restart():
    start_screen()

start_screen()
ui.run(host='0.0.0.0', port=8080)