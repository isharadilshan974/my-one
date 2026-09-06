
import streamlit as st
from pathlib import Path
from datetime import date, datetime, timedelta
import json, random, math

# ============================================================
# MY ONE — FINAL / PERSONAL LIFE OPERATING SYSTEM
# Local-first • No cloud account required • JSON persistence
# ============================================================

st.set_page_config(
    page_title="MY ONE — Life Operating System",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = Path("my_one_data.json")

DEFAULT = {
    "profile": {
        "name": "Ishara",
        "why": "One day, make Amma & Thaththa proud.",
        "north_star": "Become a highly capable software engineer, build financial freedom, and live with purpose.",
        "income_goal": 100000,
    },
    "tasks": [
        {"title":"Deep Work — Software Engineering", "area":"Career", "priority":"High", "done":False, "date":""},
        {"title":"30 min English practice", "area":"Learning", "priority":"Medium", "done":False, "date":""},
        {"title":"Review today's money", "area":"Money", "priority":"High", "done":False, "date":""},
        {"title":"Plan tomorrow", "area":"Life", "priority":"Medium", "done":False, "date":""},
    ],
    "habits": [
        {"name":"Deep Work / Study","streak":0,"checks":[],"target":5},
        {"name":"English","streak":0,"checks":[],"target":7},
        {"name":"Exercise / Walk","streak":0,"checks":[],"target":5},
        {"name":"Money check","streak":0,"checks":[],"target":7},
        {"name":"Sleep on time","streak":0,"checks":[],"target":5},
    ],
    "goals": [
        {"title":"Master Software Engineering foundations","area":"Career","deadline":"2027-01-01","progress":25},
        {"title":"Build portfolio + serious projects","area":"Career","deadline":"2027-06-30","progress":15},
        {"title":"Build emergency savings","area":"Money","deadline":"2027-12-31","progress":10},
        {"title":"Increase earning power","area":"Money","deadline":"2028-12-31","progress":5},
        {"title":"Build long-term financial freedom","area":"Life","deadline":"2030-12-31","progress":3},
    ],
    "skills": [
        {"name":"Python","level":8},
        {"name":"HTML / CSS / JavaScript","level":8},
        {"name":"SQL / Databases","level":3},
        {"name":"Git / GitHub","level":2},
        {"name":"Software Engineering","level":5},
        {"name":"English Communication","level":20},
    ],
    "transactions": [],
    "journal": [],
    "wins": [],
    "focus_sessions": [],
    "achievements": [],
    "scores": [],
    "profile_setup": False,
}

def deep_copy(x):
    return json.loads(json.dumps(x))

def load_data():
    if DATA_FILE.exists():
        try:
            loaded = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            base = deep_copy(DEFAULT)
            # Keep new fields when opening an older MY ONE file.
            for k, v in loaded.items():
                base[k] = v
            return base
        except Exception:
            pass
    return deep_copy(DEFAULT)

if "data" not in st.session_state:
    st.session_state.data = load_data()

d = st.session_state.data
TODAY = date.today().isoformat()

def save():
    DATA_FILE.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")

def rerun():
    save()
    st.rerun()

def xp_total():
    task_xp = sum(25 for x in d["tasks"] if x.get("done"))
    habit_xp = sum(10 * int(x.get("streak", 0)) for x in d["habits"])
    goal_xp = sum(max(0, int(x.get("progress", 0))) // 10 * 5 for x in d["goals"])
    focus_xp = sum(10 for x in d["focus_sessions"])
    return task_xp + habit_xp + goal_xp + focus_xp

def level_info():
    xp = xp_total()
    level = 1 + xp // 250
    current = xp % 250
    return level, current, 250

def completion():
    if not d["tasks"]:
        return 0
    return round(sum(1 for x in d["tasks"] if x.get("done")) / len(d["tasks"]) * 100)

def money():
    inc = sum(float(x["amount"]) for x in d["transactions"] if x["type"] == "Income")
    exp = sum(float(x["amount"]) for x in d["transactions"] if x["type"] == "Expense")
    return inc, exp, inc-exp

def habit_today(h):
    return TODAY in h.get("checks", [])

def achievement_list():
    done_tasks = sum(1 for x in d["tasks"] if x.get("done"))
    wins = len(d["wins"])
    focus = len(d["focus_sessions"])
    avg_skill = sum(x["level"] for x in d["skills"]) / max(1, len(d["skills"]))
    goals_done = sum(1 for x in d["goals"] if x.get("progress",0) >= 100)
    return [
        ("⚡ First Win", done_tasks >= 1, "Complete your first mission"),
        ("🔥 Mission Maker", done_tasks >= 5, "Complete 5 missions"),
        ("🏆 10 Wins", wins >= 10, "Record 10 wins"),
        ("🧠 Skill Builder", avg_skill >= 25, "Reach 25% average skill level"),
        ("🎯 Goal Crusher", goals_done >= 1, "Complete a goal"),
        ("⏱️ Deep Worker", focus >= 5, "Finish 5 focus sessions"),
        ("💎 Level 5", level_info()[0] >= 5, "Reach Level 5"),
    ]

QUOTES = [
    "Your future is built on ordinary days when nobody is watching.",
    "Don't wait for motivation. Build a system that works without it.",
    "Small progress repeated for years becomes a different life.",
    "Learn → Build → Earn → Save → Grow → Give.",
    "Your current income is a starting point, not your identity.",
    "You do not need a perfect day. You need one honest step forward.",
]

# ============================================================
# PREMIUM UI
# ============================================================
st.markdown("""
<style>
* { box-sizing:border-box; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background:#05070d !important; color:#f7f9ff !important;
}
.stApp {
    background:
      radial-gradient(circle at 12% -5%, rgba(124,92,255,.25), transparent 28%),
      radial-gradient(circle at 92% 8%, rgba(0,212,255,.12), transparent 24%),
      linear-gradient(145deg,#05070d,#090d18 50%,#05070d) !important;
}
header[data-testid="stHeader"] { background:transparent !important; }
[data-testid="stToolbar"] { visibility:hidden; }
.block-container { max-width:1500px; padding-top:1.2rem; padding-bottom:4rem; }
section[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#0b1020,#070a12) !important;
    border-right:1px solid rgba(255,255,255,.08);
}
section[data-testid="stSidebar"] * { color:#f4f7fb !important; }
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * { color:#8f9bb0 !important; }
.stApp [data-testid="stMarkdownContainer"] { color:#f4f7fb !important; }
.stApp [data-testid="stCaptionContainer"], .stApp [data-testid="stCaptionContainer"] * { color:#9ca8bb !important; }

.hero {
  position:relative; overflow:hidden; padding:30px; border-radius:30px;
  border:1px solid rgba(255,255,255,.10);
  background:
    linear-gradient(135deg,rgba(124,92,255,.25),rgba(0,212,255,.07) 48%,rgba(35,209,139,.07)),
    rgba(12,16,28,.88);
  box-shadow:0 25px 100px rgba(0,0,0,.30);
  animation:rise .55s ease both;
}
.hero:before {
  content:""; position:absolute; width:260px;height:260px;right:-80px;top:-120px;
  border-radius:50%; background:rgba(124,92,255,.18); filter:blur(5px);
  animation:float 7s ease-in-out infinite;
}
.hero:after {
  content:""; position:absolute; width:180px;height:180px;left:48%;bottom:-140px;
  border-radius:50%; background:rgba(0,212,255,.09); filter:blur(8px);
}
@keyframes rise {from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
@keyframes float {0%,100%{transform:translate(0,0)}50%{transform:translate(-18px,18px)}}
@keyframes glow {0%,100%{opacity:.6}50%{opacity:1}}
.card {
  background:rgba(14,19,32,.86); border:1px solid rgba(255,255,255,.09);
  border-radius:21px; padding:20px; margin:8px 0;
  box-shadow:0 15px 50px rgba(0,0,0,.16); animation:rise .45s ease both;
}
.card:hover { border-color:rgba(124,92,255,.32); }
.pill {
  display:inline-block; padding:6px 11px; border-radius:999px;
  background:rgba(124,92,255,.13); color:#cfc5ff !important; font-size:12px; font-weight:800;
}
.good { color:#62e6ad !important; }
.gold { color:#ffd46a !important; }
.muted { color:#9ca8bb !important; font-size:13px; }
.big { font-size:34px; font-weight:900; letter-spacing:-1px; }
.section-title { margin-top:18px; }
.quote {
  padding:20px 22px; border-radius:18px; border-left:4px solid #7c5cff;
  background:rgba(124,92,255,.07); font-size:18px; line-height:1.5;
}
.meter { height:10px; background:#1c2435; border-radius:99px; overflow:hidden; }
.meter > div { height:100%; border-radius:99px; background:linear-gradient(90deg,#7c5cff,#00d4ff,#23d18b); }
.timeline { position:relative; padding-left:28px; }
.timeline:before { content:"";position:absolute;left:7px;top:3px;bottom:3px;width:2px;background:linear-gradient(#7c5cff,#00d4ff,transparent); }
.node { position:relative; margin:0 0 22px; }
.node:before { content:"";position:absolute;left:-26px;top:5px;width:11px;height:11px;border-radius:50%;background:#7c5cff;box-shadow:0 0 18px #7c5cff;animation:glow 2s infinite; }
.stButton>button {
    background:#151c2d !important; color:#f7f9ff !important;
    border:1px solid rgba(255,255,255,.12) !important;
    border-radius:13px !important; min-height:42px; font-weight:750 !important;
}
.stButton>button:hover { background:#202b48 !important; border-color:#7c5cff !important; }
.stTextInput input,.stTextArea textarea,.stNumberInput input,.stDateInput input {
    background:#0d1422 !important; color:#fff !important; border-color:rgba(255,255,255,.13) !important;
}
.stSelectbox div[data-baseweb="select"] > div {
    background:#0d1422 !important; color:#fff !important; border-color:rgba(255,255,255,.13) !important;
}
.stMultiSelect div[data-baseweb="select"] > div { background:#0d1422 !important;color:#fff !important; }
[data-testid="stMetric"] {
    background:rgba(14,19,32,.88) !important; border:1px solid rgba(255,255,255,.09);
    border-radius:17px; padding:15px;
}
[data-testid="stMetricLabel"],[data-testid="stMetricLabel"] * {color:#aab5c8 !important;}
[data-testid="stMetricValue"],[data-testid="stMetricValue"] * {color:#f7f9ff !important;}
.stProgress > div > div > div { background:linear-gradient(90deg,#7c5cff,#00d4ff) !important; }
div[data-testid="stCheckbox"] label,div[data-testid="stCheckbox"] label p {color:#f7f9ff !important;}
.stTabs [data-baseweb="tab"] { color:#aab5c8 !important; }
.stTabs [aria-selected="true"] { color:#fff !important; }
div[data-testid="stFileUploader"] { color:#f7f9ff !important; }
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
lvl, lvl_xp, lvl_cap = level_info()
with st.sidebar:
    st.markdown("## 🔥 MY ONE")
    st.caption("YOUR PERSONAL LIFE OPERATING SYSTEM")
    nav = st.radio("COMMAND", [
        "🚀 Command Center",
        "📅 Today",
        "🎯 Goals & Roadmap",
        "🧠 Skills & Career",
        "💰 Money Engine",
        "⏱️ Focus Mode",
        "❤️ Mindset & Journal",
        "📊 Life Analytics",
        "⚙️ Settings",
    ])
    st.divider()
    st.markdown(f"### {d['profile']['name']}")
    st.caption(d["profile"]["why"])
    st.progress(min(1, lvl_xp/lvl_cap))
    st.markdown(f"**LEVEL {lvl}** · {lvl_xp}/{lvl_cap} XP")
    st.markdown("---")
    st.markdown("**THE ONE RULE**")
    st.caption("Every day, move at least one important thing forward.")
    st.markdown('<div style="color:#7c5cff;font-weight:800;animation:glow 2s infinite">● SYSTEM ONLINE</div>', unsafe_allow_html=True)

# ============================================================
# COMMAND CENTER
# ============================================================
if nav == "🚀 Command Center":
    st.markdown(f"""
    <div class="hero">
      <span class="pill">MY ONE • LIFE OS</span>
      <h1 style="font-size:42px;margin:10px 0 5px;">Welcome back, {d['profile']['name']} 👋</h1>
      <div style="font-size:17px;color:#c8d2e4;max-width:900px;">{d['profile']['north_star']}</div>
      <br><b style="color:#ffd46a;">🔥 LEVEL {lvl}</b> &nbsp; <span class="muted">{xp_total()} XP earned</span>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.markdown(f'<div class="quote">🔥 {random.choice(QUOTES)}</div>', unsafe_allow_html=True)

    inc, exp, net = money()
    c = st.columns(6)
    c[0].metric("Today", f"{completion()}%")
    c[1].metric("Level", lvl)
    c[2].metric("XP", xp_total())
    c[3].metric("Income", f"Rs. {inc:,.0f}")
    c[4].metric("Expenses", f"Rs. {exp:,.0f}")
    c[5].metric("Net", f"Rs. {net:,.0f}")

    st.markdown("### ⚡ The 4 engines")
    cols = st.columns(4)
    engines = [
        ("🧠","LEARN","Build rare, valuable skills."),
        ("💻","BUILD","Turn knowledge into projects."),
        ("💰","EARN","Increase your value and income."),
        ("❤️","LIVE","Protect health, family and character."),
    ]
    for col,(ic,title,sub) in zip(cols,engines):
        col.markdown(f'<div class="card"><div style="font-size:30px">{ic}</div><h3>{title}</h3><div class="muted">{sub}</div></div>',unsafe_allow_html=True)

    st.markdown("### 🎯 Today's ONE")
    pending = [x for x in d["tasks"] if not x.get("done")]
    if pending:
        important = next((x for x in pending if x.get("priority")=="High"), pending[0])
        st.markdown(f'<div class="card"><span class="pill">DO THIS FIRST</span><h2>{important["title"]}</h2><div class="muted">{important["area"]} • {important["priority"]} priority</div></div>',unsafe_allow_html=True)
    else:
        st.success("🔥 All missions complete. You won today. Protect the streak.")

    st.markdown("### 🗺️ Your long game")
    st.markdown("""
    <div class="timeline">
      <div class="node"><b>NOW → 2027 · FOUNDATION</b><br><span class="muted">HND • programming • English • Git • SQL • discipline • portfolio basics</span></div>
      <div class="node"><b>2027 → 2028 · EMPLOYABILITY</b><br><span class="muted">Real projects • internships/trainee roles • stronger CV • interviews</span></div>
      <div class="node"><b>2028 → 2030 · CAPABILITY + INCOME</b><br><span class="muted">Specialize • create more value • grow income • build capital responsibly</span></div>
      <div class="node"><b>2030+ · FREEDOM</b><br><span class="muted">Financial resilience • meaningful work • family goals • long-term compounding</span></div>
    </div>
    """,unsafe_allow_html=True)

    unlocked = [a for a,ok,_ in achievement_list() if ok]
    st.markdown(f"### 🏆 Achievements · {len(unlocked)}/{len(achievement_list())}")
    acols=st.columns(4)
    for col,(name,ok,desc) in zip(acols,achievement_list()[:4]):
        col.markdown(f'<div class="card"><div style="font-size:22px">{name.split(" ")[0]}</div><b>{"UNLOCKED" if ok else "LOCKED"}</b><div class="muted">{desc}</div></div>',unsafe_allow_html=True)

# ============================================================
# TODAY
# ============================================================
elif nav == "📅 Today":
    st.title("📅 Today — Win the Day")
    st.caption("The whole future is not today's job. Today's job is today's mission.")
    st.progress(completion()/100)
    st.write(f"**Mission completion: {completion()}%**")

    for i,t in enumerate(d["tasks"]):
        a,b,c=st.columns([.06,.72,.22])
        checked=a.checkbox("",value=t.get("done",False),key=f"task_{i}")
        b.markdown(f"**{t['title']}**  \n<span class='muted'>{t['area']} • {t['priority']} priority</span>",unsafe_allow_html=True)
        if c.button("🗑 Remove",key=f"del_{i}"):
            d["tasks"].pop(i); rerun()
        if checked != t.get("done",False):
            t["done"]=checked; rerun()

    with st.form("add_task"):
        st.markdown("### ➕ Add a mission")
        a,b,c=st.columns([.58,.20,.22])
        title=a.text_input("Mission")
        area=b.selectbox("Area",["Career","Learning","Money","Health","Life"])
        priority=c.selectbox("Priority",["High","Medium","Low"])
        if st.form_submit_button("Add Mission") and title.strip():
            d["tasks"].append({"title":title.strip(),"area":area,"priority":priority,"done":False,"date":TODAY})
            rerun()

    st.divider()
    st.markdown("### 🔥 Habit Streak Center")
    for i,h in enumerate(d["habits"]):
        a,b,c=st.columns([.52,.26,.22])
        a.markdown(f"**{h['name']}**  \n<span class='muted'>{h['streak']} day streak • target {h['target']}/week</span>",unsafe_allow_html=True)
        pct=min(100,round(h['streak']/max(1,h['target'])*100))
        b.progress(pct/100)
        if c.button("✓ Done" if not habit_today(h) else "↩ Undo",key=f"hb_{i}"):
            if habit_today(h):
                h["checks"].remove(TODAY); h["streak"]=max(0,h["streak"]-1)
            else:
                h["checks"].append(TODAY); h["streak"]+=1
            rerun()

# ============================================================
# GOALS
# ============================================================
elif nav == "🎯 Goals & Roadmap":
    st.title("🎯 Goals & Roadmap")
    st.caption("Dreams become real when they have a deadline, progress, and a next action.")
    for i,g in enumerate(d["goals"]):
        st.markdown(f"### {g['title']}")
        a,b=st.columns([.72,.28])
        new=a.slider("Progress",0,100,int(g["progress"]),key=f"goal_{i}",label_visibility="collapsed")
        b.markdown(f'<span class="pill">{g["area"]}</span><br><span class="muted">Target: {g["deadline"]}</span>',unsafe_allow_html=True)
        st.markdown(f'<div class="meter"><div style="width:{new}%"></div></div>',unsafe_allow_html=True)
        if new != g["progress"]:
            g["progress"]=new; save()

    st.divider()
    with st.form("new_goal"):
        st.subheader("➕ Add a goal")
        a,b,c=st.columns([.55,.20,.25])
        title=a.text_input("Goal")
        area=b.selectbox("Area",["Career","Money","Health","Learning","Life"])
        deadline=c.date_input("Deadline",date.today()+timedelta(days=365))
        if st.form_submit_button("Create Goal") and title.strip():
            d["goals"].append({"title":title.strip(),"area":area,"deadline":deadline.isoformat(),"progress":0})
            rerun()

# ============================================================
# SKILLS
# ============================================================
elif nav == "🧠 Skills & Career":
    st.title("🧠 Skill Tree — Build Your Earning Power")
    st.caption("The goal is not to know everything. Become unusually useful at valuable things.")
    for i,s in enumerate(d["skills"]):
        a,b=st.columns([.70,.30])
        a.markdown(f"**{s['name']}**")
        b.markdown(f"**{s['level']}%**")
        new=st.slider("",0,100,int(s["level"]),key=f"sk_{i}",label_visibility="collapsed")
        st.markdown(f'<div class="meter"><div style="width:{new}%"></div></div>',unsafe_allow_html=True)
        if new != s["level"]:
            s["level"]=new; save()

    st.divider()
    st.subheader("🗺️ Recommended career progression")
    roadmap=[
        ("01","FOUNDATION","Computer basics • logic • Python"),
        ("02","WEB","HTML • CSS • JavaScript • APIs"),
        ("03","DATA","SQL • databases • data handling"),
        ("04","ENGINEERING","Git • testing • clean code • architecture"),
        ("05","PROJECTS","Build real apps and publish them"),
        ("06","CAREER","CV • GitHub • portfolio • interviews"),
    ]
    cols=st.columns(3)
    for i,(n,title,desc) in enumerate(roadmap):
        cols[i%3].markdown(f'<div class="card"><span class="pill">{n}</span><h4>{title}</h4><div class="muted">{desc}</div></div>',unsafe_allow_html=True)

    st.info("Career rule: Learn one concept → build one small thing → document it → repeat.")

# ============================================================
# MONEY
# ============================================================
elif nav == "💰 Money Engine":
    st.title("💰 Money Engine")
    st.caption("Track → Control → Increase income → Build safety → Build capital.")
    inc,exp,net=money()
    c=st.columns(4)
    c[0].metric("Income",f"Rs. {inc:,.0f}")
    c[1].metric("Expenses",f"Rs. {exp:,.0f}")
    c[2].metric("Net",f"Rs. {net:,.0f}")
    c[3].metric("Income goal",f"Rs. {d['profile']['income_goal']:,.0f}")

    with st.form("money_form"):
        st.subheader("➕ Record money")
        a,b,c=st.columns([.18,.20,.62])
        typ=a.selectbox("Type",["Income","Expense"])
        amount=b.number_input("Amount (LKR)",min_value=0.0,step=500.0)
        note=c.text_input("Description")
        if st.form_submit_button("Save Transaction") and amount>0:
            d["transactions"].append({"date":TODAY,"type":typ,"amount":float(amount),"note":note})
            rerun()

    if d["transactions"]:
        st.subheader("Recent transactions")
        for x in reversed(d["transactions"][-15:]):
            sign="+" if x["type"]=="Income" else "-"
            st.write(f"**{x['date']}** · {x['type']} · {sign} Rs. {x['amount']:,.0f} · {x['note']}")

    st.divider()
    st.subheader("💎 Financial Freedom System")
    cols=st.columns(5)
    stages=[
        ("1","STABILITY","Know your cash flow"),
        ("2","SAFETY","Build emergency savings"),
        ("3","SKILL","Increase earning power"),
        ("4","CAPITAL","Save/invest responsibly"),
        ("5","FREEDOM","Build resilience over years"),
    ]
    for col,(n,t,sub) in zip(cols,stages):
        col.markdown(f'<div class="card"><span class="pill">{n}</span><h4>{t}</h4><div class="muted">{sub}</div></div>',unsafe_allow_html=True)
    st.warning("Financial sections are planning/education tools, not personalized financial advice. Never invest in something you don't understand.")

# ============================================================
# FOCUS
# ============================================================
elif nav == "⏱️ Focus Mode":
    st.title("⏱️ Focus Mode")
    st.caption("One screen. One task. No excuses.")
    st.markdown("""
    <div class="hero" style="text-align:center;">
      <div class="muted">DEEP WORK PROTOCOL</div>
      <div style="font-size:58px;font-weight:900;margin:15px;">25:00</div>
      <div class="pill">PHONE AWAY • ONE TASK • FULL FOCUS</div>
    </div>
    """,unsafe_allow_html=True)
    st.write("")
    a,b,c=st.columns(3)
    minutes=a.number_input("Session length (minutes)",min_value=5,max_value=180,value=25,step=5)
    task=b.text_input("Focus task","Software Engineering")
    if c.button("🚀 Start focus session"):
        st.session_state["focus_started"]=datetime.now().isoformat()
        st.session_state["focus_minutes"]=minutes
        st.success("Focus session started. Use a real timer on your phone/PC if you leave this page.")
    if st.button("🏁 Complete focus session"):
        d["focus_sessions"].append({"date":TODAY,"minutes":int(minutes),"task":task})
        rerun()
    st.metric("Completed focus sessions",len(d["focus_sessions"]))
    total_minutes=sum(int(x["minutes"]) for x in d["focus_sessions"])
    st.metric("Total focused minutes",total_minutes)

# ============================================================
# MINDSET
# ============================================================
elif nav == "❤️ Mindset & Journal":
    st.title("❤️ Mindset & Journal")
    st.markdown('<div class="quote">“One day, the people who believed in you will see what you built from the days nobody saw.”</div>',unsafe_allow_html=True)
    st.write("")
    with st.form("reflection"):
        mood=st.select_slider("Today feels",options=["😞","😕","😐","🙂","🔥"])
        win=st.text_input("🏆 One win")
        lesson=st.text_area("🧠 What did I learn?")
        tomorrow=st.text_area("🎯 Tomorrow's ONE important move")
        if st.form_submit_button("Save Reflection"):
            d["journal"].append({"date":TODAY,"mood":mood,"win":win,"lesson":lesson,"tomorrow":tomorrow})
            if win.strip(): d["wins"].append({"date":TODAY,"text":win.strip()})
            rerun()
    st.subheader("🏆 Your wins")
    if not d["wins"]:
        st.caption("Your first win is waiting. It can be small.")
    for w in reversed(d["wins"][-12:]):
        st.markdown(f'<div class="card">🏆 <b>{w["date"]}</b> — {w["text"]}</div>',unsafe_allow_html=True)

# ============================================================
# ANALYTICS
# ============================================================
elif nav == "📊 Life Analytics":
    st.title("📊 Life Analytics")
    st.caption("Measure what matters. Improve what you can control.")
    inc,exp,net=money()
    avg_skill=sum(x["level"] for x in d["skills"])/max(1,len(d["skills"]))
    goal_avg=sum(x["progress"] for x in d["goals"])/max(1,len(d["goals"]))
    habit_avg=sum(min(100,x["streak"]/max(1,x["target"])*100) for x in d["habits"])/max(1,len(d["habits"]))
    focus_hours=sum(int(x["minutes"]) for x in d["focus_sessions"])/60

    c=st.columns(5)
    c[0].metric("Mission",f"{completion()}%")
    c[1].metric("Skills",f"{avg_skill:.0f}%")
    c[2].metric("Goals",f"{goal_avg:.0f}%")
    c[3].metric("Habits",f"{habit_avg:.0f}%")
    c[4].metric("Focus",f"{focus_hours:.1f}h")

    st.subheader("🧭 Life Balance")
    balance={"Career":avg_skill,"Goals":goal_avg,"Habits":habit_avg,"Missions":completion()}
    for name,val in balance.items():
        st.markdown(f"**{name} — {val:.0f}%**")
        st.progress(max(0,min(1,val/100)))

    st.subheader("🏆 Achievement board")
    for name,ok,desc in achievement_list():
        st.markdown(f"{'🟢' if ok else '⚪'} **{name}** — {desc}")

    st.divider()
    st.subheader("📈 The numbers that actually matter")
    st.write(f"- **Total XP:** {xp_total():,}")
    st.write(f"- **Completed missions:** {sum(1 for x in d['tasks'] if x.get('done'))}")
    st.write(f"- **Recorded wins:** {len(d['wins'])}")
    st.write(f"- **Focus time:** {focus_hours:.1f} hours")
    st.write(f"- **Net tracked cash flow:** Rs. {net:,.0f}")

# ============================================================
# SETTINGS
# ============================================================
elif nav == "⚙️ Settings":
    st.title("⚙️ Settings")
    st.caption("Your data stays in your local MY ONE folder unless you export it.")
    p=d["profile"]
    name=st.text_input("Name",p["name"])
    why=st.text_input("My Why",p["why"])
    north=st.text_area("North Star",p["north_star"])
    income_goal=st.number_input("Monthly income target (LKR)",min_value=0.0,value=float(p["income_goal"]),step=5000.0)
    if st.button("💾 Save profile"):
        p.update({"name":name,"why":why,"north_star":north,"income_goal":income_goal})
        rerun()

    st.divider()
    st.subheader("💾 Backup & Restore")
    backup=json.dumps(d,indent=2,ensure_ascii=False)
    st.download_button("⬇️ Download MY ONE backup",data=backup,file_name=f"my_one_backup_{TODAY}.json",mime="application/json")
    up=st.file_uploader("Restore a MY ONE JSON backup",type=["json"])
    if up and st.button("♻️ Restore backup"):
        try:
            st.session_state.data=json.loads(up.read().decode("utf-8"))
            save()
            st.success("Backup restored successfully.")
            st.rerun()
        except Exception as e:
            st.error(f"Backup error: {e}")

    st.divider()
    st.subheader("🧹 Reset")
    st.warning("Reset deletes your current local MY ONE data and returns to starter data.")
    if st.button("Reset to starter data"):
        st.session_state.data=deep_copy(DEFAULT)
        save()
        st.success("MY ONE has been reset.")
        st.rerun()

st.markdown("---")
st.markdown(
    '<div style="text-align:center;color:#7d899e;font-size:12px;">'
    '🔥 MY ONE — Build the person who can build the life you want. '
    'Local-first • Your data • Your system • Your future'
    '</div>',
    unsafe_allow_html=True
)
