import streamlit as st
from pathlib import Path
from datetime import date, datetime, timedelta, timezone
import json, random, calendar

try:
    from supabase import create_client
except ImportError:
    create_client = None

st.set_page_config(page_title='MY ONE — Life OS', page_icon='🔥', layout='wide', initial_sidebar_state='expanded')
DATA_FILE = Path('my_one_data.json')
TODAY = date.today().isoformat()

DEFAULT = {
    'profile': {'name':'Ishara','why':'One day, make Amma & Thaththa proud.','north_star':'Become a highly capable software engineer, build financial freedom, and live with purpose.','income_goal':100000,'start_date':TODAY},
    'tasks': [
        {'id':'t1','title':'Deep Work — Software Engineering','area':'Career','priority':'High','done':False,'date':TODAY},
        {'id':'t2','title':'30 min English practice','area':'Learning','priority':'Medium','done':False,'date':TODAY},
        {'id':'t3','title':"Review today's money",'area':'Money','priority':'High','done':False,'date':TODAY},
        {'id':'t4','title':'Plan tomorrow','area':'Life','priority':'Medium','done':False,'date':TODAY},
    ],
    'habits': [
        {'id':'h1','name':'Deep Work / Study','checks':[],'target':5}, {'id':'h2','name':'English','checks':[],'target':7},
        {'id':'h3','name':'Exercise / Walk','checks':[],'target':5}, {'id':'h4','name':'Money check','checks':[],'target':7}, {'id':'h5','name':'Sleep on time','checks':[],'target':5}
    ],
    'goals': [
        {'id':'g1','title':'Master Software Engineering foundations','area':'Career','deadline':'2027-01-01','progress':25,'next_step':'Practice programming 5 days/week'},
        {'id':'g2','title':'Build portfolio + serious projects','area':'Career','deadline':'2027-06-30','progress':15,'next_step':'Ship one small project'},
        {'id':'g3','title':'Build emergency savings','area':'Money','deadline':'2027-12-31','progress':10,'next_step':'Track every expense'},
        {'id':'g4','title':'Increase earning power','area':'Money','deadline':'2028-12-31','progress':5,'next_step':'Build employable IT skills'},
        {'id':'g5','title':'Build long-term financial freedom','area':'Life','deadline':'2030-12-31','progress':3,'next_step':'Grow skills and capital responsibly'},
    ],
    'skills': [
        {'id':'s1','name':'Python','level':8,'category':'Programming'}, {'id':'s2','name':'HTML / CSS / JavaScript','level':8,'category':'Web'},
        {'id':'s3','name':'SQL / Databases','level':3,'category':'Data'}, {'id':'s4','name':'Git / GitHub','level':2,'category':'Engineering'},
        {'id':'s5','name':'Software Engineering','level':5,'category':'Engineering'}, {'id':'s6','name':'English Communication','level':20,'category':'Communication'},
    ],
    'transactions': [], 'journal': [], 'wins': [], 'focus_sessions': [], 'achievements': [], 'weekly_reviews': [], 'settings': {'currency':'LKR'},
}

def cp(x): return json.loads(json.dumps(x))
def merge(x):
    b=cp(DEFAULT)
    if isinstance(x,dict):
        for k,v in x.items(): b[k]=v
    return b

def uid(prefix): return f'{prefix}_{datetime.now().strftime("%Y%m%d%H%M%S%f")}'

def local_load():
    if DATA_FILE.exists():
        try: return merge(json.loads(DATA_FILE.read_text(encoding='utf-8')))
        except Exception: pass
    return cp(DEFAULT)

def get_client():
    if create_client is None: return None
    try:
        url=st.secrets.get('SUPABASE_URL'); key=st.secrets.get('SUPABASE_KEY')
        return create_client(url,key) if url and key else None
    except Exception: return None

supabase=get_client()
if 'auth_user' not in st.session_state: st.session_state.auth_user=None
if 'access_token' not in st.session_state: st.session_state.access_token=None
if 'refresh_token' not in st.session_state: st.session_state.refresh_token=None

if supabase:
    if st.session_state.access_token and st.session_state.refresh_token:
        try: supabase.auth.set_session(st.session_state.access_token, st.session_state.refresh_token)
        except Exception: pass
    if st.session_state.auth_user is None:
        try:
            s=getattr(supabase.auth.get_session(),'session',None)
            if s and getattr(s,'user',None):
                st.session_state.auth_user=s.user; st.session_state.access_token=s.access_token; st.session_state.refresh_token=s.refresh_token
        except Exception: pass
    if st.session_state.auth_user is None:
        try:
            u=getattr(supabase.auth.get_user(),'user',None)
            if u: st.session_state.auth_user=u
        except Exception: pass

if supabase and st.session_state.auth_user is None:
    st.markdown('''<div class="login-hero"><div class="eyebrow">MY ONE • LIFE OPERATING SYSTEM</div><h1>Build the life you want. One day at a time. 🔥</h1><p>Your goals, habits, money, skills and reflections — synced securely to your account.</p></div>''', unsafe_allow_html=True)
    a,b=st.tabs(['🔐 Login','✨ Create account'])
    with a:
        e=st.text_input('Email',key='le'); p=st.text_input('Password',type='password',key='lp')
        if st.button('🚀 Login to MY ONE',type='primary',use_container_width=True):
            try:
                r=supabase.auth.sign_in_with_password({'email':e,'password':p}); s=getattr(r,'session',None); u=getattr(r,'user',None)
                if s and u:
                    st.session_state.auth_user=u; st.session_state.access_token=s.access_token; st.session_state.refresh_token=s.refresh_token; st.rerun()
                else: st.error('Login failed. Check your email/password.')
            except Exception as ex: st.error(f'Login failed: {ex}')
    with b:
        e2=st.text_input('Email',key='se'); p2=st.text_input('Password (6+ characters)',type='password',key='sp')
        if st.button('✨ Create MY ONE account',use_container_width=True):
            try:
                r=supabase.auth.sign_up({'email':e2,'password':p2}); s=getattr(r,'session',None); u=getattr(r,'user',None)
                if s and u:
                    st.session_state.auth_user=u; st.session_state.access_token=s.access_token; st.session_state.refresh_token=s.refresh_token; st.rerun()
                else: st.success('Account created. Confirm your email if required, then log in.')
            except Exception as ex: st.error(f'Sign-up failed: {ex}')
    st.stop()

USER_ID=str(st.session_state.auth_user.id) if supabase and st.session_state.auth_user else None

def load_data():
    if supabase and USER_ID:
        try:
            rows=supabase.table('my_one_data').select('data').eq('user_id',USER_ID).execute().data
            if rows: return merge(rows[0].get('data',{}))
            x=cp(DEFAULT); supabase.table('my_one_data').insert({'user_id':USER_ID,'data':x}).execute(); return x
        except Exception: pass
    return local_load()

if 'data' not in st.session_state: st.session_state.data=load_data()
d=st.session_state.data

def save():
    DATA_FILE.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
    if supabase and USER_ID:
        try: supabase.table('my_one_data').upsert({'user_id':USER_ID,'data':d,'updated_at':datetime.now(timezone.utc).isoformat()}).execute()
        except Exception: pass

def rerun(): save(); st.rerun()

def money():
    inc=sum(float(x.get('amount',0)) for x in d['transactions'] if x.get('type')=='Income')
    exp=sum(float(x.get('amount',0)) for x in d['transactions'] if x.get('type')=='Expense')
    return inc,exp,inc-exp

def tasks_today(): return [x for x in d['tasks'] if not x.get('date') or x.get('date')==TODAY]
def completion():
    t=tasks_today(); return round(sum(x.get('done',False) for x in t)/len(t)*100) if t else 0

def xp_total():
    return sum(25 for x in d['tasks'] if x.get('done')) + sum(10*len(set(x.get('checks',[]))) for x in d['habits']) + sum((int(x.get('progress',0))//10)*5 for x in d['goals']) + sum(10 for _ in d['focus_sessions'])

def level(): return 1+xp_total()//250

def streak(h):
    checks=set(h.get('checks',[])); n=0; cur=date.today()
    while cur.isoformat() in checks: n+=1; cur-=timedelta(days=1)
    return n

def ach():
    done=sum(x.get('done',False) for x in d['tasks']); avg=sum(x.get('level',0) for x in d['skills'])/max(1,len(d['skills']))
    return [('⚡ First Mission',done>=1,'Complete one mission'),('🔥 5 Missions',done>=5,'Complete five missions'),('🏆 10 Wins',len(d['wins'])>=10,'Record ten wins'),('🧠 Skill Builder',avg>=25,'Reach 25% average skill'),('🎯 Goal Crusher',any(x.get('progress',0)>=100 for x in d['goals']),'Complete a goal'),('⏱️ Deep Worker',len(d['focus_sessions'])>=5,'Finish five focus sessions'),('💎 Level 5',level()>=5,'Reach level five')]

st.markdown('''
<style>
:root{--bg:#060913;--panel:#0e1525;--line:rgba(255,255,255,.09);--text:#f5f7fb;--muted:#9aa7bb;--a:#7c5cff;--b:#00d4ff;--g:#23d18b;--gold:#ffd166}
*{box-sizing:border-box} .stApp{background:radial-gradient(circle at 10% -10%,rgba(124,92,255,.23),transparent 28%),radial-gradient(circle at 100% 0%,rgba(0,212,255,.10),transparent 24%),linear-gradient(145deg,#060913,#0a0f1c 55%,#05070d)!important;color:var(--text)!important}
header{background:transparent!important}.block-container{max-width:1500px;padding-top:1rem;padding-bottom:5rem}.stMarkdown,.stMarkdown p,.stMarkdown li,label{color:var(--text)!important}.stCaption,.stCaption p{color:var(--muted)!important}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#0a1020,#070b14)!important;border-right:1px solid var(--line)}section[data-testid="stSidebar"] *{color:var(--text)!important}
.stButton>button{background:#151d30!important;color:#fff!important;border:1px solid rgba(255,255,255,.12)!important;border-radius:13px!important;font-weight:800!important;min-height:42px}.stButton>button:hover{background:#202b47!important;border-color:var(--a)!important}
.stTextInput input,.stTextArea textarea,.stNumberInput input,.stDateInput input{background:#0b1220!important;color:#fff!important;border-color:rgba(255,255,255,.13)!important}.stSelectbox div[data-baseweb="select"]>div,.stMultiSelect div[data-baseweb="select"]>div{background:#0b1220!important;color:#fff!important;border-color:rgba(255,255,255,.13)!important}
[data-testid="stMetric"]{background:rgba(14,21,37,.88)!important;border:1px solid var(--line);border-radius:18px;padding:15px}[data-testid="stMetricLabel"] *{color:var(--muted)!important}[data-testid="stMetricValue"] *{color:#fff!important}
.stProgress>div>div>div{background:linear-gradient(90deg,var(--a),var(--b),var(--g))!important}.stCheckbox label,.stCheckbox label p{color:#fff!important}.stTabs [data-baseweb="tab"]{color:#aab5c8!important}.stTabs [aria-selected="true"]{color:#fff!important}
.hero,.login-hero{padding:30px;border-radius:28px;border:1px solid var(--line);background:linear-gradient(135deg,rgba(124,92,255,.22),rgba(0,212,255,.06),rgba(35,209,139,.06)),rgba(12,17,30,.88);box-shadow:0 25px 100px rgba(0,0,0,.28)}.hero h1{font-size:42px;margin:8px 0}.login-hero h1{font-size:40px;margin:10px 0}.eyebrow,.pill{display:inline-block;padding:6px 11px;border-radius:999px;background:rgba(124,92,255,.14);color:#d8d0ff!important;font-size:12px;font-weight:900;letter-spacing:.5px}.card{background:rgba(14,21,37,.86);border:1px solid var(--line);border-radius:20px;padding:19px;margin:8px 0;box-shadow:0 14px 50px rgba(0,0,0,.15)}.muted{color:var(--muted)!important}.good{color:#62e6ad!important}.gold{color:var(--gold)!important}.big{font-size:34px;font-weight:950}.quote{padding:18px 21px;border-radius:18px;border-left:4px solid var(--a);background:rgba(124,92,255,.07);font-size:17px}.meter{height:10px;background:#1b2436;border-radius:99px;overflow:hidden}.meter>div{height:100%;background:linear-gradient(90deg,var(--a),var(--b),var(--g));border-radius:99px}.timeline{position:relative;padding-left:28px}.timeline:before{content:"";position:absolute;left:7px;top:3px;bottom:3px;width:2px;background:linear-gradient(var(--a),var(--b),transparent)}.node{position:relative;margin-bottom:22px}.node:before{content:"";position:absolute;left:-26px;top:5px;width:11px;height:11px;border-radius:50%;background:var(--a);box-shadow:0 0 18px var(--a)}footer{visibility:hidden}
</style>''',unsafe_allow_html=True)

lvl=level(); inc,exp,net=money()
with st.sidebar:
    st.markdown('## 🔥 MY ONE')
    st.caption('PERSONAL LIFE OPERATING SYSTEM')
    nav=st.radio('COMMAND',['🚀 Command Center','📅 Today','🔥 Habits','🎯 Goals & Roadmap','🧠 Skills & Career','💰 Money Engine','⏱️ Focus Mode','❤️ Mindset & Journal','📊 Life Analytics','⚙️ Settings'])
    st.divider(); st.markdown(f'### {d["profile"]["name"]}'); st.caption(d['profile']['why'])
    st.progress(min(1,(xp_total()%250)/250)); st.markdown(f'**LEVEL {lvl}** · {xp_total()} XP')
    st.divider(); st.markdown('**THE ONE RULE**'); st.caption('Every day, move at least one important thing forward.')
    st.markdown('🟢 **CLOUD SYNC ON**' if supabase else '🟡 **LOCAL MODE**')
    if supabase and st.button('🚪 Log out',use_container_width=True):
        try: supabase.auth.sign_out()
        except Exception: pass
        for k in ['auth_user','access_token','refresh_token','data']: st.session_state.pop(k,None)
        st.rerun()

if nav=='🚀 Command Center':
    st.markdown(f'<div class="hero"><span class="eyebrow">MY ONE • LIFE OS</span><h1>Welcome back, {d["profile"]["name"]} 👋</h1><div style="color:#c8d2e4;font-size:17px">{d["profile"]["north_star"]}</div><br><b class="gold">🔥 LEVEL {lvl}</b> · {xp_total()} XP</div>',unsafe_allow_html=True)
    st.write(''); st.markdown(f'<div class="quote">🔥 {random.choice(["Your future is built on ordinary days when nobody is watching.","You do not need a perfect day. You need one honest step forward.","Learn → Build → Earn → Save → Grow → Give.","Small progress repeated for years becomes a different life."])}</div>',unsafe_allow_html=True)
    c=st.columns(6); c[0].metric('Today',f'{completion()}%'); c[1].metric('Level',lvl); c[2].metric('XP',xp_total()); c[3].metric('Income',f'Rs. {inc:,.0f}'); c[4].metric('Expenses',f'Rs. {exp:,.0f}'); c[5].metric('Net',f'Rs. {net:,.0f}')
    st.markdown('### 🎯 Today at a glance')
    pending=[x for x in tasks_today() if not x.get('done')]
    cols=st.columns(3)
    for i,(title,val,sub) in enumerate([('Missions',f'{len(pending)} pending','Finish the important ones first'),('Habits',f'{sum("" if False else (TODAY in h.get("checks",[])) for h in d["habits"])} / {len(d["habits"])}','Keep the streak alive'),('Goals',f'{sum(1 for g in d["goals"] if g.get("progress",0)>=100)} / {len(d["goals"])}','Play the long game')]): cols[i].markdown(f'<div class="card"><div class="muted">{title}</div><div class="big">{val}</div><div class="muted">{sub}</div></div>',unsafe_allow_html=True)
    st.markdown('### ⚡ The 4 engines')
    for col,(ic,t,s) in zip(st.columns(4),[('🧠','LEARN','Build valuable skills'),('💻','BUILD','Turn knowledge into projects'),('💰','EARN','Increase your value'),('❤️','LIVE','Protect health and family')]): col.markdown(f'<div class="card"><div style="font-size:30px">{ic}</div><h3>{t}</h3><div class="muted">{s}</div></div>',unsafe_allow_html=True)
    if pending:
        first=next((x for x in pending if x.get('priority')=='High'),pending[0]); st.markdown(f'<div class="card"><span class="pill">DO THIS FIRST</span><h2>{first["title"]}</h2><div class="muted">{first["area"]} • {first["priority"]}</div></div>',unsafe_allow_html=True)
    else: st.success('🔥 All missions complete. Protect the streak.')
    st.markdown('### 🗺️ Long game')
    st.markdown('<div class="timeline"><div class="node"><b>2026–2027 · FOUNDATION</b><br><span class="muted">HND • programming • English • Git • SQL • discipline</span></div><div class="node"><b>2027–2028 · EMPLOYABILITY</b><br><span class="muted">Real projects • portfolio • internships/trainee roles • interviews</span></div><div class="node"><b>2028–2030 · CAPABILITY + INCOME</b><br><span class="muted">Specialize • create value • grow income • build capital responsibly</span></div><div class="node"><b>2030+ · FREEDOM</b><br><span class="muted">Resilience • meaningful work • family goals • long-term compounding</span></div></div>',unsafe_allow_html=True)
    unlocked=sum(ok for _,ok,_ in ach()); st.markdown(f'### 🏆 Achievements · {unlocked}/{len(ach())}'); st.write(' · '.join([n for n,ok,_ in ach() if ok]) or 'Your first achievement is waiting.')

elif nav=='📅 Today':
    st.title('📅 Today — Execute the plan')
    st.progress(completion()/100); st.caption(f'{completion()}% of today’s missions complete')
    with st.form('addtask'):
        a,b,c,e=st.columns([.40,.18,.18,.24]); title=a.text_input('Mission'); area=b.selectbox('Area',['Career','Learning','Money','Health','Life']); pri=c.selectbox('Priority',['High','Medium','Low']); dt=e.date_input('Date',date.today())
        if st.form_submit_button('➕ Add mission') and title.strip(): d['tasks'].append({'id':uid('t'),'title':title.strip(),'area':area,'priority':pri,'done':False,'date':dt.isoformat()}); rerun()
    st.subheader('Your missions')
    for i,t in enumerate(d['tasks']):
        if t.get('date') not in ('',TODAY): continue
        done=st.checkbox(f'{t["title"]}  ·  {t["area"]}  ·  {t["priority"]}',value=t.get('done',False),key=f'task_{t["id"]}')
        if done!=t.get('done',False): t['done']=done; save(); st.rerun()
    st.divider(); st.subheader('📌 Upcoming')
    for t in sorted([x for x in d['tasks'] if x.get('date') and x.get('date')>TODAY],key=lambda x:x['date'])[:12]: st.write(f'**{t["date"]}** · {t["title"]} · {t["priority"]}')

elif nav=='🔥 Habits':
    st.title('🔥 Habit & Streak Center'); st.caption('Consistency beats intensity.')
    with st.form('addhabit'):
        n,target=st.columns([.7,.3]); name=n.text_input('New habit'); tg=target.number_input('Weekly target days',1,7,5)
        if st.form_submit_button('➕ Add habit') and name.strip(): d['habits'].append({'id':uid('h'),'name':name.strip(),'checks':[],'target':int(tg)}); rerun()
    for h in d['habits']:
        checked=TODAY in h.get('checks',[]); a,b,c=st.columns([.55,.2,.25]); a.markdown(f'**{h["name"]}**'); b.metric('Streak',f'{streak(h)} 🔥');
        if c.button('✅ Done today' if not checked else '↩️ Undo today',key=f'h_{h["id"]}'):
            if checked: h['checks'].remove(TODAY)
            else: h.setdefault('checks',[]).append(TODAY)
            save(); st.rerun()
        st.progress(min(1,streak(h)/max(1,int(h.get('target',5)))))

elif nav=='🎯 Goals & Roadmap':
    st.title('🎯 Goals & Roadmap')
    with st.form('goal'):
        a,b,c=st.columns([.5,.2,.3]); title=a.text_input('Goal'); area=b.selectbox('Area',['Career','Money','Health','Learning','Life']); dl=c.date_input('Deadline',date.today()+timedelta(days=365)); step=st.text_input('Next action')
        if st.form_submit_button('🎯 Create goal') and title.strip(): d['goals'].append({'id':uid('g'),'title':title.strip(),'area':area,'deadline':dl.isoformat(),'progress':0,'next_step':step}); rerun()
    for g in d['goals']:
        st.markdown(f'<div class="card"><span class="pill">{g["area"]}</span><h3>{g["title"]}</h3><div class="muted">Deadline: {g["deadline"]} · Next: {g.get("next_step", "—")}</div></div>',unsafe_allow_html=True)
        p=st.slider('Progress',0,100,int(g.get('progress',0)),key=f'g_{g["id"]}')
        if p!=g.get('progress',0): g['progress']=p; save()
        st.progress(p/100)
    st.subheader('🗺️ 2026 → 2030 roadmap')
    for year,txt in [('2026','Foundation: HND + programming + English + habits'),('2027','Portfolio: real projects + GitHub + IT opportunity'),('2028','Capability: specialization + stronger income'),('2029','Leverage: high-value skills + responsible capital building'),('2030+','Freedom: resilience, family goals and meaningful work')]: st.markdown(f'<div class="card"><b>{year}</b><br><span class="muted">{txt}</span></div>',unsafe_allow_html=True)

elif nav=='🧠 Skills & Career':
    st.title('🧠 Skills & Career'); st.caption('Learn → Build → Document → Repeat.')
    avg=sum(s['level'] for s in d['skills'])/max(1,len(d['skills'])); st.metric('Average skill level',f'{avg:.0f}%')
    for s in d['skills']:
        a,b=st.columns([.72,.28]); a.markdown(f'**{s["name"]}** · {s.get("category","")}'); b.markdown(f'**{s["level"]}%**'); v=st.slider('',0,100,int(s['level']),key=f's_{s["id"]}',label_visibility='collapsed')
        if v!=s['level']: s['level']=v; save()
        st.progress(v/100)
    st.divider(); st.subheader('🚀 Career progression')
    for n,t,desc in [('01','FOUNDATION','Logic • Python • computer basics'),('02','WEB','HTML • CSS • JavaScript • APIs'),('03','DATA','SQL • databases • data handling'),('04','ENGINEERING','Git • testing • clean code • architecture'),('05','PROJECTS','Build and publish real apps'),('06','CAREER','CV • GitHub • portfolio • interviews')]: st.markdown(f'<div class="card"><span class="pill">{n}</span><h4>{t}</h4><div class="muted">{desc}</div></div>',unsafe_allow_html=True)

elif nav=='💰 Money Engine':
    st.title('💰 Money Engine'); st.caption('Track → Control → Increase earning power → Build safety.')
    c=st.columns(4); c[0].metric('Income',f'Rs. {inc:,.0f}'); c[1].metric('Expenses',f'Rs. {exp:,.0f}'); c[2].metric('Net',f'Rs. {net:,.0f}'); c[3].metric('Monthly target',f'Rs. {d["profile"]["income_goal"]:,.0f}')
    with st.form('tx'):
        a,b,c=st.columns([.18,.22,.6]); typ=a.selectbox('Type',['Income','Expense']); amount=b.number_input('Amount (LKR)',0.0,step=500.0); note=c.text_input('Description')
        if st.form_submit_button('💾 Save transaction') and amount>0: d['transactions'].append({'id':uid('m'),'date':TODAY,'type':typ,'amount':float(amount),'note':note}); rerun()
    if d['transactions']:
        st.subheader('Recent');
        for x in reversed(d['transactions'][-20:]): st.write(f'**{x["date"]}** · {x["type"]} · Rs. {x["amount"]:,.0f} · {x.get("note","")}')
    st.divider(); st.subheader('💎 Financial freedom framework')
    for n,t,s in [('1','STABILITY','Know cash flow'),('2','SAFETY','Build emergency savings'),('3','SKILL','Increase earning power'),('4','CAPITAL','Save/invest responsibly'),('5','FREEDOM','Build resilience over years')]: st.markdown(f'<div class="card"><span class="pill">{n}</span><h4>{t}</h4><div class="muted">{s}</div></div>',unsafe_allow_html=True)

elif nav=='⏱️ Focus Mode':
    st.title('⏱️ Focus Mode'); st.caption('One task. One block. Full attention.')
    a,b=st.columns(2); minutes=a.number_input('Session length',5,180,25,5); task=b.text_input('Focus task','Software Engineering')
    st.markdown(f'<div class="hero" style="text-align:center"><div class="muted">DEEP WORK</div><div class="big">{int(minutes):02d}:00</div><span class="pill">PHONE AWAY • ONE TASK</span></div>',unsafe_allow_html=True)
    if st.button('🚀 Start focus session',type='primary'): st.session_state.focus_started=datetime.now().isoformat(); st.info('Session started. Keep this page open and use your device timer if needed.')
    if st.button('🏁 Complete session'): d['focus_sessions'].append({'id':uid('f'),'date':TODAY,'minutes':int(minutes),'task':task}); rerun()
    total=sum(int(x.get('minutes',0)) for x in d['focus_sessions']); c=st.columns(2); c[0].metric('Completed sessions',len(d['focus_sessions'])); c[1].metric('Focused time',f'{total//60}h {total%60}m')

elif nav=='❤️ Mindset & Journal':
    st.title('❤️ Mindset & Journal'); st.markdown('<div class="quote">The days nobody sees are building the life everybody will see.</div>',unsafe_allow_html=True)
    with st.form('journal'):
        mood=st.select_slider('Today feels',options=['😞','😕','😐','🙂','🔥']); win=st.text_input('🏆 One win'); lesson=st.text_area('🧠 What did I learn?'); tomorrow=st.text_area('🎯 Tomorrow’s ONE')
        if st.form_submit_button('💾 Save reflection'):
            d['journal'].append({'id':uid('j'),'date':TODAY,'mood':mood,'win':win,'lesson':lesson,'tomorrow':tomorrow})
            if win.strip(): d['wins'].append({'id':uid('w'),'date':TODAY,'text':win.strip()})
            rerun()
    st.subheader('🏆 Wins');
    for w in reversed(d['wins'][-20:]): st.markdown(f'<div class="card">🏆 <b>{w["date"]}</b> — {w["text"]}</div>',unsafe_allow_html=True)
    st.subheader('📖 Recent reflections')
    for j in reversed(d['journal'][-7:]): st.markdown(f'<div class="card"><b>{j["date"]}</b> {j["mood"]}<br><span class="muted">Win: {j.get("win","")}<br>Lesson: {j.get("lesson","")}<br>Tomorrow: {j.get("tomorrow","")}</span></div>',unsafe_allow_html=True)

elif nav=='📊 Life Analytics':
    st.title('📊 Life Analytics'); st.caption('Measure what matters. Improve what you control.')
    avg_skill=sum(s['level'] for s in d['skills'])/max(1,len(d['skills'])); goal_avg=sum(g['progress'] for g in d['goals'])/max(1,len(d['goals'])); habit_avg=sum(min(100,streak(h)/max(1,h.get('target',5))*100) for h in d['habits'])/max(1,len(d['habits'])); focus_h=sum(int(x.get('minutes',0)) for x in d['focus_sessions'])/60
    c=st.columns(5); c[0].metric('Missions',f'{completion()}%'); c[1].metric('Skills',f'{avg_skill:.0f}%'); c[2].metric('Goals',f'{goal_avg:.0f}%'); c[3].metric('Habits',f'{habit_avg:.0f}%'); c[4].metric('Focus',f'{focus_h:.1f}h')
    st.subheader('🧭 Life balance')
    for name,val in {'Execution':completion(),'Career':avg_skill,'Goals':goal_avg,'Habits':habit_avg}.items(): st.markdown(f'**{name} — {val:.0f}%**'); st.progress(max(0,min(1,val/100)))
    st.subheader('🏆 Achievement board')
    for n,ok,desc in ach(): st.write(('🟢' if ok else '⚪'),f'**{n}** — {desc}')
    st.divider(); st.write(f'**Total XP:** {xp_total():,}'); st.write(f'**Completed missions:** {sum(x.get("done",False) for x in d["tasks"])}'); st.write(f'**Recorded wins:** {len(d["wins"])}'); st.write(f'**Focus time:** {focus_h:.1f} hours')

elif nav=='⚙️ Settings':
    st.title('⚙️ Settings & Backup')
    p=d['profile']
    with st.form('profile'):
        name=st.text_input('Name',p['name']); why=st.text_input('My Why',p['why']); ns=st.text_area('North Star',p['north_star']); target=st.number_input('Monthly income target (LKR)',0.0,float(p['income_goal']),5000.0)
        if st.form_submit_button('💾 Save profile'): p.update({'name':name,'why':why,'north_star':ns,'income_goal':target}); rerun()
    st.divider(); st.subheader('☁️ Cloud status'); st.success('Supabase connected — data sync is enabled.' if supabase else 'Local mode — add Supabase secrets to enable cloud sync.')
    backup=json.dumps(d,ensure_ascii=False,indent=2); st.download_button('⬇️ Download full backup',backup,f'my_one_backup_{TODAY}.json','application/json')
    up=st.file_uploader('Restore backup',type=['json'])
    if up and st.button('♻️ Restore backup'):
        try: st.session_state.data=merge(json.loads(up.read().decode('utf-8'))); d=st.session_state.data; save(); st.success('Backup restored.'); st.rerun()
        except Exception as ex: st.error(f'Backup error: {ex}')
    st.divider(); st.subheader('⚠️ Reset'); st.warning('Reset will replace your current data with starter data.')
    if st.button('Reset MY ONE',type='secondary'): st.session_state.data=cp(DEFAULT); save(); st.success('Reset complete.'); st.rerun()

# silent periodic local backup; cloud save occurs on meaningful changes
