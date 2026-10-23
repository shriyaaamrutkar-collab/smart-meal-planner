import streamlit as st
from datetime import date
from logic.database import init_db, get_latest_user, get_all_foods, get_reward_completions, award_reward_task, get_total_reward_points
from logic.calorie import get_full_calorie_summary
from logic.protein import calculate_protein_target
from logic.ui import apply_theme, sidebar
st.set_page_config(page_title='SmartMeal', page_icon='🥗', layout='wide', initial_sidebar_state='expanded')
init_db()
apply_theme()
sidebar()
user = get_latest_user()
if user is None:
    st.markdown('<div class="hero"><h1>🥗 SmartMeal</h1>\n    <p>Your offline, rule-based personal meal planning and nutrition manager.</p></div>', unsafe_allow_html=True)
    st.info('Welcome! Create your profile first so SmartMeal can calculate your calorie and protein targets.')
    if st.button('👤 Create my profile', type='primary'):
        st.switch_page('pages/2_Profile.py')
else:
    summary = get_full_calorie_summary(user['gender'], user['weight_kg'], user['height_cm'], user['age'], user['activity_level'], user['goal'])
    protein = calculate_protein_target(user['weight_kg'], user['goal'], user['activity_level'])
    st.markdown(f"""<div class="hero"><h1>Good to see you, {user['name']} 👋</h1>\n    <p>Stay consistent with your <b>{user['goal']}</b> goal — one meal at a time.</p></div>""", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric('Daily calories', f"{summary['calorie_target']:.0f} kcal")
    c2.metric('Protein target', f'{protein:.0f} g')
    c3.metric('Current weight', f"{user['weight_kg']:.1f} kg")
    c4.metric('Meals / day', str(user['meals_per_day']))
    quotes = [('Small steps every day add up to big changes.', 'Consistency beats perfection.'), ('You do not need a perfect day; you need a next good choice.', 'Progress, not perfection.'), ('Take care of your body. It is the place you live in.', 'Your health matters.'), ('Every healthy choice is a vote for the person you want to become.', 'Keep showing up.'), ('Rest, fuel, move, repeat. Sustainable habits win.', 'One day at a time.'), ('Celebrate effort, not just outcomes.', 'You are building a habit.'), ('A little progress is still progress.', 'Keep going.')]
    quote, tagline = quotes[date.today().toordinal() % len(quotes)]
    st.markdown(f'<div class="card" style="background:linear-gradient(135deg,#fff8df,#ffffff);border-color:#f0e2ae;"><div class="muted">✨ DAILY MOTIVATION</div><h3>“{quote}”</h3><div class="muted">{tagline}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section">🏆 Daily challenges & rewards</div>', unsafe_allow_html=True)
    today = date.today().isoformat()
    completed = get_reward_completions(user['user_id'], today)
    completed_keys = {item['task_key'] for item in completed}
    points_total = get_total_reward_points(user['user_id'])
    done_today = sum((item['points'] for item in completed))
    r1, r2, r3 = st.columns(3)
    r1.metric('⭐ Total reward points', points_total)
    r2.metric("Today's points", done_today)
    r3.metric('Challenges completed', f'{len(completed)}/4')
    tasks = [('log_food', 'Log your food for today', 10), ('track_water', 'Track your water intake', 10), ('record_steps', "Record today's step count", 15), ('complete_workout', 'Complete or intentionally do a planned workout', 20)]
    st.caption('Mark a challenge only after you have done it. Each challenge can earn points once per day.')
    for task_key, label, points in tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(('✅ ' if task_key in completed_keys else '🎯 ') + f'**{label}** — {points} points')
        with col2:
            if task_key in completed_keys:
                st.button('Claimed', key=f'reward_{task_key}', disabled=True, use_container_width=True)
            elif st.button('Mark done', key=f'reward_{task_key}', use_container_width=True):
                awarded = award_reward_task(user['user_id'], today, task_key, label, points)
                if awarded:
                    st.success(f'Well done! +{points} reward points earned.')
                else:
                    st.info('You have already claimed this challenge today.')
                st.rerun()
    if points_total >= 100:
        st.success('🎉 Reward unlocked: SmartMeal Habit Builder (100 points)! Keep building your healthy routine.')
    elif points_total >= 50:
        st.info('🏅 Reward unlocked: Consistency Star (50 points)! Your habits are adding up.')
    else:
        st.caption(f'Next reward: Consistency Star at 50 points — {max(0, 50 - points_total)} points to go.')
    st.markdown('<div class="section">Quick actions</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    actions = [('🍽️', 'Plan meals', 'pages/4_Meal_Planner.py'), ('📝', 'Log food', 'pages/6_Food_Logger.py'), ('👣', 'Enter steps', 'pages/14_Step_Tracker.py'), ('🥗', 'Analyze nutrition', 'pages/5_Nutrition_Analyzer.py')]
    for col, (icon, label, path) in zip(cols, actions):
        with col:
            st.markdown(f'<div class="card"><h3>{icon} {label}</h3><div class="muted">Open this SmartMeal tool.</div></div>', unsafe_allow_html=True)
            if st.button('Open', key=label, use_container_width=True):
                st.switch_page(path)
    st.markdown('<div class="section">How SmartMeal works</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for col, title, desc in zip(cols, ['1. Personalize', '2. Plan & log', '3. Track progress'], ['Your profile drives the calculations.', 'Use the local food database to plan meals and record intake.', 'See calories, protein, water, weight and activity trends.']):
        with col:
            st.markdown(f'<div class="card"><h3>{title}</h3><div class="muted">{desc}</div></div>', unsafe_allow_html=True)
    st.caption('SmartMeal is completely offline and rule-based. It does not use AI or external APIs.')
