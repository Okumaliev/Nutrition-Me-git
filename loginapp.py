import streamlit as st
import pandas as pd
import numpy as np
 
# Function to calculate BMI
def calculate_bmi(weight, height):
    return weight / ((height/100) ** 2)

def calculate_bmr(gender, weight, height , age):
    if gender == 'Female':
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    return bmr
 
# Define a function to calculate TDEE based on BMR and activity level
def calculate_tdee(bmr, workout_days_per_week, workload_intensity):
    if workload_intensity.lower() == 'low' and workout_days_per_week == 0:
        activity_multiplier = 1.2
    elif workload_intensity.lower() == 'low' or (1 <= workout_days_per_week <= 3):
        activity_multiplier = 1.375
    elif workload_intensity.lower() == 'moderate' or (3 <= workout_days_per_week <= 5):
        activity_multiplier = 1.55
    elif workload_intensity.lower() == 'high' and workout_days_per_week == 7:
        activity_multiplier = 1.9
    else:
        activity_multiplier = 1.725
    tdee = bmr * activity_multiplier 
    return tdee
 
# Define a function to calculate macronutrient distribution based on goals
def calculate_macronutrients(weight_goal, muscle_gain_goal, tdee):
    protein_ratio = 0.25
    carb_ratio = 0.4
    fat_ratio = 0.35
    if muscle_gain_goal.lower() == 'yes':
        protein_ratio += 0.15
        carb_ratio -= 0.1
        fat_ratio -= 0.05
    if weight_goal == 'Lose Weight (High Priority)':
        protein_ratio -= 0.05
        carb_ratio -= 0.1
        fat_ratio += 0.15
    elif weight_goal == 'Lose Weight':
        protein_ratio -= 0.05
        carb_ratio -= 0.1
        fat_ratio += 0.05
    elif weight_goal == 'Gain Weight':
        protein_ratio += 0.05
        carb_ratio += 0.1
        fat_ratio += 0.1
    elif weight_goal == 'Maintain Weight':
        pass  # No adjustments needed for macronutrients
    protein = protein_ratio * tdee / 4  # 4 calories per gram of protein
    carb = carb_ratio * tdee / 4  # 4 calories per gram of carb
    fat = fat_ratio * tdee / 9  # 9 calories per gram of fat

    return protein, carb, fat
 
# Function to calculate required nutrients
def calculate_nutrients(weight, height, age, gender, muscle_gain, weight_goal, workout_days_per_week, workload_intensity):

    # Calculate BMI
    bmi = calculate_bmi(weight, height)
 
    # Calculate BMR (Basal Metabolic Rate) using Mifflin-St Jeor Equation
    bmr= calculate_bmr(gender,weight,height,age)

    # Calculate TDEE based on BMR based on activity level
    tdee=calculate_tdee(bmr, workout_days_per_week, workload_intensity)
   
    # Calculate nutrients intake
    proteins, carbs, fats =calculate_macronutrients(weight_goal, muscle_gain, tdee)

    return {
        "BMI": bmi,
        "BMR":bmr,
        "Calories": tdee,
        "Proteins (g)": proteins,
        "Carbs (g)": carbs,
        "Fats (g)": fats
    }


# Main function
def main():
    st.title("User Registration and Nutrition Calculator")

    user_data=pd.read_csv("userdatafinal.csv", header=0)
    
    # Login section
    login = st.checkbox("Login")
    
    if login:
        login_user_id = st.text_input("User ID")
        login_password = st.text_input("Password", type="password")
        login_button = st.button("Login")
 
        if login_button:
            if login_button:
                login_successful = False
                for index, row in user_data.iterrows():
                    if row['user_id'] == login_user_id and row['password'] == login_password:
                        login_successful = True
                        st.success("Login successful!")
                        st.session_state.is_logged_in = True
                        st.session_state.user_id = login_user_id
                        st.experimental_rerun()
                        st.info("User Dashboard will be displayed here.")
                        st.stop()
                if not login_successful:
                    st.warning("Invalid User ID or Password. Please try again.")

 
    # Registration section
    st.subheader("New User Registration")
    name = st.text_input("Name")
    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")
    age = st.number_input("Age", min_value=0, max_value=150, step=1)
    weight = st.number_input("Weight (kg)", min_value=0.0, max_value=1000.0, step=0.1)
    height = st.number_input("Height (cm)", min_value=0.0)
    gender = st.radio("Gender", options=["Male", "Female"])
    muscle_gain = st.selectbox("Muscle Gain", options=["Yes", "No"])
    weight_goals = st.selectbox("Weight Goals", options=["Lose Weight (High Priority)", "Maintain Weight", "Gain Weight (Muscle)"])
    workout_days_per_week = st.slider("Number of Workout Days", min_value=0, max_value=7, value=3)
    workload_intensity = st.selectbox("Workout Intensity", options=["Low", "Medium", "High"])
 
    register_button = st.button("Register")

 
    if register_button:
        # Calculate BMI and required nutrients
        bmi = calculate_bmi(weight, height)
        nutrients = calculate_nutrients(weight, height, age, gender, muscle_gain, weight_goals, workout_days_per_week, workload_intensity)
        new_row = {'name': name, 'user_id': user_id,
                  'password': password, 'age': age, 'weight': weight,
                  'height': height, 'bmi': bmi, 'gender': gender,
                  'muscle_gain_goal': muscle_gain, 'weight_goal': weight_goals, 'workout_days_per_week': workout_days_per_week, 'workload_intensity': workload_intensity,
                  'bmr':nutrients["BMR"],'tdee':nutrients["Calories"],'protein':nutrients["Proteins (g)"],'carb':nutrients["Carbs (g)"],'fat':nutrients["Fats (g)"]}

        user_data.loc[len(user_data)]= new_row
        user_data.to_csv("userdatafinal.csv",index=False)
        st.subheader("Required Nutrients")
        df = pd.DataFrame([nutrients])
        st.write(df)
        st.session_state.is_logged_in = True
        st.session_state.user_id = user_id

        st.experimental_rerun()
 
# Run the app
if __name__ == "__main__":
    main()
