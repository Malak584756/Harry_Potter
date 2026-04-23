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
        "question_ar": "ظهر كائن ملعون في الممر؛ ما هي حركتك القادمة؟",
        "options": {
            "Use a dark detection spell to identify it": "Dark Arts Knowledge",
            "Cast a precise defensive counter": "Dueling Skills",
            "Distract it with a creative illusion": "Creativity",
            "Make a solid plan to catch him": "Intelligence"
        },
        "options_ar": {
            "استخدام تعويذة كشف الظلام لتحديده": "Dark Arts Knowledge",
            "إلقاء تعويذة دفاعية دقيقة": "Dueling Skills",
            "تشتيته بوهم سحري مبتكر": "Creativity",
            "وضع خطة محكمة للإمساك به": "Intelligence"
        }
    },
    {
        "question": "A Bludger goes out of control during practice; how do you react?",
        "question_ar": "خرجت كرة 'بلودجر' عن السيطرة أثناء التدريب؛ كيف ستتصرف؟",
        "options": {
            "Intercept it mid‑air with a clean maneuver": "Quidditch Skills",
            "Blast it away using a spell": "Dark Arts Knowledge",
            "Create a magical lure to redirect it": "Creativity",
            "Dash forward to shield a teammate from its path": "Bravery"
        },
        "options_ar": {
            "اعتراضها في الهواء بحركة طيران بارعة": "Quidditch Skills",
            "تفجيرها بعيداً باستخدام تعويذة": "Dark Arts Knowledge",
            "ابتكار وسيلة جذب سحرية لتغيير مسارها": "Creativity",
            "الاندفاع للأمام لحماية زميلك من طريقها": "Bravery"
        }
    },
    {
        "question": "A forbidden spellbook locks itself magically; what do you do?",
        "question_ar": "كتاب تعاويذ محرم أغلق نفسه سحرياً؛ ماذا ستفعل؟",
        "options": {
            "Decode the dark runes on its cover": "Dark Arts Knowledge",
            "Force it open with a controlled strike": "Dueling Skills",
            "Craft an unusual unlocking technique": "Creativity",
            "Examine the mechanism carefully": "Intelligence"
        },
        "options_ar": {
            "فك رموز الظلام المنقوشة على غلافه": "Dark Arts Knowledge",
            "فتحه بالقوة بضربة سحرية محكمة": "Dueling Skills",
            "ابتكار تقنية غير تقليدية لفك القفل": "Creativity",
            "فحص آلية القفل بعناية وذكاء": "Intelligence"
        }
    },
    {
        "question": "During a duel, your opponent suddenly vanishes in smoke; what's your response?",
        "question_ar": "أثناء مبارزة، اختفى خصمك فجأة في وسط الدخان؛ ما هو رد فعلك؟",
        "options": {
            "Use dark sensing magic to track him": "Dark Arts Knowledge",
            "Prepare a defensive stance instantly": "Dueling Skills",
            "Create a creative trap spell": "Creativity",
            "Call for backup in case it’s serious": "Loyalty"
        },
        "options_ar": {
            "استخدام سحر استشعار الظلام لتتبعه": "Dark Arts Knowledge",
            "اتخاذ وضعية دفاعية فورية": "Dueling Skills",
            "ابتكار فخ سحري مفاجئ": "Creativity",
            "طلب الدعم في حال كان الأمر خطيراً": "Loyalty"
        }
    },
    {
        "question": "You must retrieve a magical item floating high above a cliff.",
        "question_ar": "يجب عليك استعادة غرض سحري يطفو عالياً فوق منحدر صخري.",
        "options": {
            "Fly up with perfect balance": "Quidditch Skills",
            "Shoot a precise spell to lower it": "Dark Arts Knowledge",
            "Build a creative floating platform": "Creativity",
            "Study the wind pattern first": "Intelligence"
        },
        "options_ar": {
            "الطيران للأعلى بتوازن مثالي": "Quidditch Skills",
            "إطلاق تعويذة دقيقة لإنزاله": "Dark Arts Knowledge",
            "بناء منصة طافية مبتكرة": "Creativity",
            "دراسة أنماط الرياح أولاً": "Intelligence"
        }
    },
    {
        "question": "You encounter ancient dark symbols carved into stone.",
        "question_ar": "واجهت رموزاً مظلمة قديمة محفورة في الحجر.",
        "options": {
            "Interpret the symbols’ origins": "Dark Arts Knowledge",
            "Blast the stone open to break the enchantment": "Dueling Skills",
            "Sketch a creative counter‑pattern": "Creativity",
            "Take notes for later research": "Intelligence"
        },
        "options_ar": {
            "تفسير أصول الرموز وتاريخها": "Dark Arts Knowledge",
            "تفجير الحجر لكسر السحر": "Dueling Skills",
            "رسم نمط مضاد ومبتكر": "Creativity",
            "تدوين ملاحظات للبحث اللاحق": "Intelligence"
        }
    },
    {
        "question": "You’re challenged to design a new magical combat spell.",
        "question_ar": "تم تحديك لتصميم تعويذة قتالية سحرية جديدة.",
        "options": {
            "Combine shadow magic with power": "Dark Arts Knowledge",
            "Make a fast duel‑focused strike spell": "Dueling Skills",
            "Invent a creative multidirectional effect": "Creativity",
            "Design a spell to gain recognition": "Ambition"
        },
        "options_ar": {
            "دمج سحر الظلال مع القوة": "Dark Arts Knowledge",
            "صنع تعويذة ضربة سريعة للمبارزات": "Dueling Skills",
            "اختراع تأثير مبتكر متعدد الاتجاهات": "Creativity",
            "تصميم تعويذة تجلب لك التقدير والشهرة": "Ambition"
        }
    },
    {
        "question": "A broom malfunction happens mid‑air; how do you fix it?",
        "question_ar": "حدث عطل في مكنستك وأنت في الهواء؛ كيف ستصلحه؟",
        "options": {
            "Stabilize yourself with expert flying": "Quidditch Skills",
            "Force‑cast a repairing spell": "Dueling Skills",
            "Modify the broom using a creative charm": "Creativity",
            "Land and analyze it calmly": "Intelligence"
        },
        "options_ar": {
            "تثبيت نفسك بمهارات طيران احترافية": "Quidditch Skills",
            "إلقاء تعويذة إصلاح قوية": "Dueling Skills",
            "تعديل المكنسة بسحر ابتكاري": "Creativity",
            "الهبوط وتحليل المشكلة بهدوء": "Intelligence"
        }
    },
    {
        "question": "Quidditch Tryouts begin; what's your move?",
        "question_ar": "بدأت تجارب أداء الكويدتش؛ ما هي خطتك؟",
        "options": {
            "Show perfect broom control": "Quidditch Skills",
            "Step forward bravely": "Bravery",
            "Suggest a warm‑up plan": "Intelligence",
            "Encourage teammates": "Loyalty"
        },
        "options_ar": {
            "إظهار تحكم مثالي بالمكنسة": "Quidditch Skills",
            "التقدم بشجاعة وثقة": "Bravery",
            "اقتراح خطة للإحماء": "Intelligence",
            "تشجيع زملائك في الفريق": "Loyalty"
        }
    },
    {
        "question": "Wind becomes very strong mid‑match; what do you do?",
        "question_ar": "أصبحت الرياح قوية جداً في منتصف المباراة؛ ماذا ستفعل؟",
        "options": {
            "Adjust your flying angle": "Quidditch Skills",
            "Hold firm and push through": "Bravery",
            "Analyze wind direction": "Intelligence",
            "Use a light defensive spell to stabilize your broom against the gusts": "Dueling Skills"
        },
        "options_ar": {
            "تعديل زاوية طيرانك لتناسب الرياح": "Quidditch Skills",
            "الثبات والاندفاع بقوة": "Bravery",
            "تحليل اتجاه الرياح بدقة": "Intelligence",
            "استخدام تعويذة دفاعية لتثبيت المكنسة": "Dueling Skills"
        }
    },
    {
        "question": "During class, a dangerous spell goes wrong; your reaction?",
        "question_ar": "أثناء الفصل، فشلت تعويذة خطيرة؛ ما هو رد فعلك؟",
        "options": {
            "Rush forward to shield others": "Bravery",
            "Help your partner recover": "Loyalty",
            "Step in to impress the professor": "Ambition",
            "Use swift broom movement to avoid the blast": "Quidditch Skills"
        },
        "options_ar": {
            "الاندفاع للأمام لحماية الآخرين": "Bravery",
            "مساعدة شريكك على التعافي": "Loyalty",
            "التدخل لإبهار البروفيسور": "Ambition",
            "استخدام حركة طيران سريعة لتجنب الانفجار": "Quidditch Skills"
        }
    },
    {
        "question": "A loud scream echoes from the Forbidden Forest; what do you do?",
        "question_ar": "دوى صراخ عالٍ من الغابة المحرمة؛ ماذا ستفعل؟",
        "options": {
            "Run toward the sound to help": "Bravery",
            "Go call others for support": "Loyalty",
            "Investigate hoping to prove yourself": "Ambition",
            "Scout the area quickly from above": "Quidditch Skills"
        },
        "options_ar": {
            "الركض نحو الصوت للمساعدة": "Bravery",
            "الذهاب لاستدعاء الآخرين للدعم": "Loyalty",
            "التحقيق في الأمر على أمل إثبات نفسك": "Ambition",
            "استكشاف المنطقة بسرعة من الأعلى": "Quidditch Skills"
        }
    },
    {
        "question": "You see a first-year student being bullied.",
        "question_ar": "رأيت طالباً في السنة الأولى يتعرض للمضايقة.",
        "options": {
            "Step in directly to stop it": "Bravery",
            "Stay with the student until they're okay": "Loyalty",
            "Use the situation to show leadership": "Ambition",
            "Distract the bullies with a quick broom maneuver": "Quidditch Skills"
        },
        "options_ar": {
            "التدخل مباشرة لإيقاف الأمر": "Bravery",
            "البقاء مع الطالب حتى يطمئن": "Loyalty",
            "استغلال الموقف لإظهار قيادتك": "Ambition",
            "تشتيت المتنمرين بحركة مكنسة سريعة": "Quidditch Skills"
        }
    },
    { 
        "question": "Defense Against the Dark Arts lesson begins, your move?",
        "question_ar": "بدأ درس الدفاع ضد فنون الظلام، ما هي حركتك؟",
        "options": {
            "Volunteer immediately": "Bravery",
            "Suggest a clever plan": "Intelligence",
            "Encourage your friend": "Loyalty",
            "Ask to use an advanced offensive spell": "Ambition"
        },
        "options_ar": {
            "التطوع فوراً للمشاركة": "Bravery",
            "اقتراح خطة ذكية للدرس": "Intelligence",
            "تشجيع صديقك على المشاركة": "Loyalty",
            "طلب استخدام تعويذة هجومية متقدمة": "Ambition"
        }
    },
    {
        "question": "Ravenclaw Tower Riddle appears, how do you solve it?",
        "question_ar": "ظهر لغز برج رافنكلو، كيف ستحله؟",
        "options": {
            "Solve it yourself": "Intelligence",
            "Invent a creative answer": "Creativity",
            "Use a spell to bypass the puzzle": "Ambition",
            "Stand your ground and attempt the riddle bravely": "Bravery"
        },
        "options_ar": {
            "حل اللغز بنفسك وبذكائك": "Intelligence",
            "ابتكار إجابة إبداعية خارج الصندوق": "Creativity",
            "استخدام تعويذة لتخطي اللغز": "Ambition",
            "الثبات ومحاولة حل اللغز بكل شجاعة": "Bravery"
        }
    },
    {
        "question": "Professor challenges you to handle a cursed artifact.",
        "question_ar": "البروفيسور يتحداك للتعامل مع أثر سحري ملعون.",
        "options": {
            "Step forward confidently": "Bravery",
            "Use a controlled disarming spell": "Dueling Skills",
            "Tap into forbidden knowledge to weaken it": "Dark Arts Knowledge",
            "Volunteer to show your skills": "Ambition"
        },
        "options_ar": {
            "التقدم للأمام بثقة": "Bravery",
            "استخدام تعويذة تجريد من السلاح محكمة": "Dueling Skills",
            "استغلال معرفتك بالفنون السوداء لإضعافه": "Dark Arts Knowledge",
            "التطوع لاستعراض مهاراتك الخاصة": "Ambition"
        }
    },
    {
        "question": "You find a ritual circle drawn on the floor.",
        "question_ar": "وجدت دائرة طقوس مرسومة على الأرض.",
        "options": {
            "Step inside to inspect it closely": "Bravery",
            "Disrupt the circle safely with a spell": "Dueling Skills",
            "Decode the runes using dark knowledge": "Dark Arts Knowledge",
            "Use the discovery to boost your reputation": "Ambition"
        },
        "options_ar": {
            "الدخول للداخل لفحصها عن قرب": "Bravery",
            "تعطيل الدائرة بأمان باستخدام تعويذة": "Dueling Skills",
            "فك الرموز باستخدام المعرفة المظلمة": "Dark Arts Knowledge",
            "استخدام الاكتشاف لتعزيز سمعتك": "Ambition"
        }
    },
    {
        "question": "Lead a Team: your decision?",
        "question_ar": "قيادة فريق: ما هو قرارك؟",
        "options": {
            "Accept with confidence": "Ambition",
            "Accept but with a careful plan": "Intelligence",
            "Refuse and nominate someone better": "Loyalty",
            "Accept because you're not afraid of responsibility": "Bravery"
        },
        "options_ar": {
            "القبول بثقة وطموح": "Ambition",
            "القبول ولكن مع وضع خطة حذرة": "Intelligence",
            "الرفض وترشيح شخص تراه أنسب": "Loyalty",
            "القبول لأنك لا تخشى المسؤولية": "Bravery"
        }
    },
    {
        "question": "Final Battle: your role?",
        "question_ar": "المعركة النهائية: ما هو دورك؟",
        "options": {
            "Fight at the front": "Bravery",
            "Think of a clever plan": "Intelligence",
            "Protect everyone around": "Loyalty",
            "Use your strongest spell no matter how dark": "Dark Arts Knowledge"
        },
        "options_ar": {
            "القتال في الخطوط الأمامية": "Bravery",
            "التفكير في خطة ذكية للنصر": "Intelligence",
            "حماية كل من حولك": "Loyalty",
            "استخدام أقوى تعاويذك مهما كانت مظلمة": "Dark Arts Knowledge"
        }
    },
    {
        "question": "You find an ancient wand with unstable energy.",
        "question_ar": "وجدت عصا قديمة ذات طاقة غير مستقرة.",
        "options": {
            "Use it to gain an edge": "Ambition",
            "Stabilize it with duel technique": "Dueling Skills",
            "Enhance it with a custom enchantment": "Creativity",
            "Test its energy mid‑air": "Quidditch Skills"
        },
        "options_ar": {
            "استخدامها للحصول على أفضلية": "Ambition",
            "تثبيت طاقتها بتقنية المبارزة": "Dueling Skills",
            "تحسينها بسحر مخصص ومبتكر": "Creativity",
            "اختبار طاقتها وأنت في الهواء": "Quidditch Skills"
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

question_images = [
    "/images/dobyy.png","/images/expresss.png","/images/golden_snitchh.png",
    "/images/volt.png","/images/hedwigg.png","/images/dragonn.png",
    "/images/hippogrifff.png","/images/phounixx.png",
]

random_quiz = []
current_q = 0
answers = {}  
current_lang = 'en'

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
            global random_quiz, current_q, answers, current_lang
            current_lang = 'en'
            current_q = 0
            answers.clear()
            random_quiz = quiz_pool.copy()
            random.shuffle(random_quiz)
            play_music()
            show_question()

        sort_hat.on("click", start_quiz)

def show_question():
    question_container.clear()
    global current_q, current_lang
    if current_q >= len(random_quiz):
        show_result(final=True)
        return

    q = random_quiz[current_q]

    with question_container:
        small_hat = ui.image("/images/sorting.png")\
            .classes("w-32 cursor-pointer animate-bounce")\
            .style("position: fixed; top:20px; right:20px; z-index:1000;")

        def try_show_result():
            if len(answers) >= 10:
                show_result(final=False, instant=True)
            else:
                ui.notify("Please answer at least 10 questions first.", color="red")

        small_hat.on("click", lambda e: try_show_result())
        lang_label = "🌐 English" if current_lang == 'ar' else "العربية 🌐"
        
        def toggle_lang():
            global current_lang
            current_lang = 'ar' if current_lang == 'en' else 'en'
            show_question()

        ui.button(lang_label, on_click=toggle_lang)\
            .classes("bg-blue-900 text-white text-xs mb-2 self-end shadow-md")\
            .style("border-radius: 8px; font-family: sans-serif;")

        if current_lang == 'ar':
            display_text = q.get("question_ar", q["question"])
            display_options = q.get("options_ar", q["options"])
            text_align = "right"
            direction = "rtl"
        else:
            display_text = q["question"]
            display_options = q["options"]
            text_align = "left"
            direction = "ltr"

        ui.label(f"Question {current_q+1}/{len(random_quiz)}").classes("text-lg text-yellow-200 mt-2")

        with ui.row().classes("w-full mt-4 items-center justify-between"):
            ui.label(display_text).classes("text-2xl flex-1").style(f"""
                background: rgba(0,0,0,0.5);
                padding: 12px;
                border-radius: 12px;
                text-align: {text_align};
                direction: {direction};
            """)
            ui.image(question_images[current_q % len(question_images)])\
                .style("width:140px; height:140px; animation:float 3s infinite;")

        options_list = list(display_options.items())
        random.shuffle(options_list)

        for text, trait in options_list:
            ui.button(text, on_click=lambda t=trait, q=q: select_fixed(q, t))\
                .classes("btn w-full mt-3")

def select_fixed(q, trait_choice):
    global current_q
    answers[q["question"]] = trait_choice 
    current_q += 1
    show_question()

def show_traits_analysis(scores):
    total_score = sum(scores.values())
    if total_score == 0: total_score = 1
    
    ui.label("✨ Your Magical Traits Analysis").classes("text-xl text-yellow-300 mt-6 mb-2 w-full text-center")
    
    with ui.grid(columns=2).classes('w-full gap-4 p-4').style("background: rgba(0,0,0,0.7); border-radius: 20px; border: 1px solid #f0d857;"):
        
        for trait in traits:
            percent = int(round((scores[trait] / total_score) * 100))
            
            with ui.column().classes('w-full items-center justify-center p-1'):
                ui.label(f"{trait.upper()}").classes("text-base text-yellow-500 font-bold mb-1")
                ui.label(f"{percent}%").classes("text-2xl text-white font-serif")

# Calculates scores and predicts the Hogwarts house
def show_result(final=True, instant=False):
    stop_music()
    question_container.clear()

    # Count scores for each trait
    scores = {t: 0 for t in traits}
    for q in random_quiz:
        trait_ans = answers.get(q["question"]) 
        if trait_ans:
            scores[trait_ans] += 1

    # Normalize scores
    for key, value in scores.items():
        if key == "Dueling Skills":
            scores[key] = max(0, min(10, value))
        else:
            scores[key] = max(1, min(10, value))

    # Predict house
    features = np.array([[scores[t] for t in traits]])
    pred = log_reg.predict(features)
    best_house = le.inverse_transform(pred)[0]

    # instanr result (small hat)
    if instant:
        with question_container:
            ui.label("🎩 Your House is...")\
                .classes("text-3xl text-yellow-300 mt-6 text-center")

            ui.image(house_images[best_house]) \
            .classes("w-64 mx-auto mt-4 drop-shadow-[0_0_10px_rgba(240,216,87,0.4)]")

            ui.run_javascript(
                f"var audio = new Audio('{house_sounds[best_house]}'); audio.play();"
            )
            show_traits_analysis(scores)

            ui.button("Restart", on_click=restart)\
                .classes("btn mt-6")

    # NORMAL END → BIG HAT FIRST
    else:
        with question_container:
            ui.label("🎩 The Sorting Hat is ready...")\
                .classes("text-3xl text-yellow-300 text-center mt-6")

            big_hat = ui.image("/images/sorting.png")\
                .classes("w-80 mx-auto mt-10 cursor-pointer animate-bounce")

            ui.label("Click the hat to reveal your house...")\
                .classes("text-white text-center mt-4")

            def reveal_result(e):
                question_container.clear()

                with question_container:
                    ui.label("🎩 Your House is...")\
                        .classes("text-3xl text-yellow-300 mt-6 text-center")

                    ui.image(house_images[best_house]) \
                    .classes("w-64 mx-auto mt-4 drop-shadow-[0_0_10px_rgba(240,216,87,0.4)]")

                    ui.run_javascript(
                        f"var audio = new Audio('{house_sounds[best_house]}'); audio.play();"
                    )
                    show_traits_analysis(scores)

                    ui.button("Restart", on_click=restart)\
                        .classes("btn mt-6")

            big_hat.on("click", reveal_result)

    big_hat.on("click", reveal_result)
def restart():
    start_screen()

start_screen()
ui.run(host='0.0.0.0', port=8080)