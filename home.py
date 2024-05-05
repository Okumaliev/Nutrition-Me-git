import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def main():
    
    # Load user data from CSV based on user_id stored in session_state
    user_data = pd.read_csv("userdatafinal.csv")
    user_data = user_data[user_data['user_id'] == st.session_state.user_id].iloc[0]
    nutrition_tracking_df = pd.read_csv("nutrition_tracking.csv")
    # Check if the row for the user_id and date exists
    mask = (nutrition_tracking_df['user_id'] == st.session_state.user_id)
    existing_rows = nutrition_tracking_df.loc[mask]
    if not existing_rows.empty:

        nutrition_data = {
            'user_id': user_data['user_id'],
            'calories_left': existing_rows['calories_left'].iloc[0],
            'proteins_left': existing_rows['proteins_left'].iloc[0],
            'fats_left': existing_rows['fats_left'].iloc[0],
            'carbs_left': existing_rows['carbs_left'].iloc[0]
        }
    else:
        nutrition_data = {
            'user_id': [user_data['user_id']],
            'calories_left': 0,
            'proteins_left': 0,
            'fats_left': 0,
            'carbs_left': 0
        }
    
    

    # User goals for the health tips
    user_goals = {
        'calories_goal': user_data['tdee'],
        'proteins_goal': user_data['protein'],
        'fats_goal': user_data['fat'],
        'carbs_goal': user_data['carb']
    }

    # Create Streamlit App
    st.title('Nutrition and Health Dashboard')

    # Display User Demographic Information and User Goals side by side
    col1, col2 = st.columns(2)

    # User Demographic Information
    with col1:
        st.subheader('User Demographic Information')
        st.markdown("""
        <style>
        .key {
            font-weight: bold;
            font-style: italic;
        }
        </style>
        """, unsafe_allow_html=True)
        st.text_input('Name:', user_data['name'], key='name', disabled=True)
        st.text_input('User ID:', user_data['user_id'], key='user_id', disabled=True)
        st.text_input('Age:', str(user_data['age']) + ' years', key='age', disabled=True)
        st.text_input('Weight:', str(user_data['weight']) + ' kg', key='weight', disabled=True)
        st.text_input('Height:', str(user_data['height']) + ' cm', key='height', disabled=True)

    # User Goals
    with col2:
        st.subheader('User Goals')
        st.text_input('Muscle Gain Goal:', user_data['muscle_gain_goal'], key='muscle_gain_goal', disabled=True)
        st.text_input('Weight Goal:', user_data['weight_goal'], key='weight_goal', disabled=True)
        st.text_input('Workout Days per Week:', str(user_data['workout_days_per_week']), key='workout_days_per_week', disabled=True)
        st.text_input('Workload Intensity:', user_data['workload_intensity'], key='workload_intensity', disabled=True)

    # Merge nutrition data with user goals
    merged_df = pd.merge(pd.DataFrame([nutrition_data]), pd.DataFrame([user_goals]), left_index=True, right_index=True)
    st.write(merged_df)

    # Function to create horizontal bar load
    def horizontal_bar_load(value, goal, color):
        left = goal - value
        if value < goal:
            percentage = (value / goal) * 100
        else:
            percentage = 100
        fig, ax = plt.subplots(figsize=(8, 1))
        ax.barh([1], percentage, color=color)
        ax.set_xlim(0, 100)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(percentage - 5, 1, f'{percentage:.1f}%', color='black', va='center', ha='right', fontsize=10)
        ax.text(0, 0.6, str(int(left)), color='red', va='center', ha='right', fontsize=10)
        return fig

    # Visualizations with Horizontal Bar Load
    for nutrient, color in zip(['calories', 'proteins', 'fats', 'carbs'], ['skyblue', 'green', 'purple', 'blue']):
        st.subheader(f'{nutrient.capitalize()} Consumption and Goals')
        
        # Display Horizontal Bar Load
        st.pyplot(horizontal_bar_load(merged_df[f'{nutrient}_left'][0], merged_df[f'{nutrient}_goal'][0], color=color))
    # Generate Health Tips based on user goals

    st.subheader('Health Tips Based on User Goals')

    if user_data['muscle_gain_goal'] == 'Yes':
        st.markdown(" 🥩 **Tip 1:** To support muscle gain, focus on consuming enough protein. Aim for high-quality protein sources like lean meats, eggs, and dairy.")
    else:
        st.markdown(" 🌿 **Tip 1:** Even if you're not focusing on muscle gain, including some protein in every meal can help maintain muscle mass and support overall health.")
        
    if user_data['weight_goal'] == 'Gain Weight':
        st.markdown(" 🍚 **Tip 2:** To gain weight healthily, focus on nutrient-dense foods like whole grains, healthy fats, and protein-rich foods.")
    elif user_data['weight_goal'] == 'Lose Weight':
        st.markdown(" 🥗 **Tip 2:** To lose weight, aim for a balanced diet with a slight calorie deficit. Include plenty of vegetables, lean proteins, and whole grains.")
    else:
        st.markdown(" ⚖️ **Tip 2:** To maintain weight, ensure your calorie intake matches your energy expenditure. Monitor your nutrient consumption regularly.")
        
    if user_data['workout_days_per_week'] >= 3:
        st.markdown(" 🏋️ **Tip 3:** Consistency is key! Stick to your workout schedule to achieve your fitness goals and support your nutrient needs.")
    else:
        st.markdown(" 🚶 **Tip 3:** Even light exercise like walking can have health benefits. Try to incorporate movement into your daily routine.")
        
    if user_data['workload_intensity'] == 'Low':
        st.markdown(" 💪 **Tip 4:** Consider increasing your workout intensity gradually to challenge your muscles and boost metabolism.")
    elif user_data['workload_intensity'] == 'High':
        st.markdown(" 🏃 **Tip 4:** High-intensity workouts can be effective but ensure you're giving your body enough rest and recovery time.")
    else:
        st.markdown(" 🧘 **Tip 4:** Finding a balanced workout routine that suits your lifestyle and fitness level is key to long-term success.")

if __name__ == "__main__":
    main()

