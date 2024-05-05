import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def main():
    # Load data
    @st.cache(allow_output_mutation=True)
    def load_data():
        return pd.read_csv('recipes_updated.csv')

    # Setup similarity matrix
    @st.cache(allow_output_mutation=True)
    def setup_similarity_matrix(data):
        vectorizer = TfidfVectorizer(stop_words='english')
        ingredient_matrix = vectorizer.fit_transform(data['ingredients'])
        cosine_sim = cosine_similarity(ingredient_matrix)
        return cosine_sim, vectorizer

    data = load_data()
    cosine_sim, vectorizer = setup_similarity_matrix(data)

    # Sidebar for nutritional and ingredient filters
    st.sidebar.header('Filter recipes based on:')
    protein = st.sidebar.slider('Protein per serving (grams)', 0, int(data['proteins_per_serving'].max()), (0, int(data['proteins_per_serving'].max())))
    calories = st.sidebar.slider('Calories per serving', 0, int(data['calories_per_serving'].max()), (0, int(data['calories_per_serving'].max())))
    fats = st.sidebar.slider('Fats per serving (grams)', 0, int(data['fats_per_serving'].max()), (0, int(data['fats_per_serving'].max())))
    carbs = st.sidebar.slider('Carbohydrates per serving (grams)', 0, int(data['carbs_per_serving'].max()), (0, int(data['carbs_per_serving'].max())))
    ingredients_input = st.sidebar.text_input('Include Ingredients (comma-separated)', '')

    # Filter data
    filtered_data = data[(data['proteins_per_serving'] >= protein[0]) & (data['proteins_per_serving'] <= protein[1]) &
                         (data['calories_per_serving'] >= calories[0]) & (data['calories_per_serving'] <= calories[1]) &
                         (data['fats_per_serving'] >= fats[0]) & (data['fats_per_serving'] <= fats[1]) &
                         (data['carbs_per_serving'] >= carbs[0]) & (data['carbs_per_serving'] <= carbs[1])]

    if ingredients_input:
        included_ingredients = [ingredient.strip().lower() for ingredient in ingredients_input.split(',')]
        filtered_data = filtered_data[filtered_data['ingredients'].apply(lambda x: any(ingredient.lower() in x.lower() for ingredient in included_ingredients))]

    # Display recipes in the main page
    st.write('Filtered Recipes:', filtered_data[['id', 'label', 'proteins_per_serving', 'calories_per_serving', 'fats_per_serving', 'carbs_per_serving']])

    # Selecting a recipe
    selected_recipe_id = st.selectbox('Select a recipe ID to see suggestions:', filtered_data['id'])
    selected_recipe = data[data['id'] == selected_recipe_id]

    # Display the selected recipe details
    if not selected_recipe.empty:
        st.write('Selected Recipe Details:', selected_recipe[['label', 'ingredients', 'url']].iloc[0])

        # Show similar recipes
        index = selected_recipe.index[0]
        scores = list(enumerate(cosine_sim[index]))
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        top_5_recipes = [data.iloc[i[0]] for i in sorted_scores[1:6]]  # skip the first one as it is the recipe itself

        st.write('Top 5 similar recipes:', pd.DataFrame(top_5_recipes)[['id', 'label', 'ingredients']])

        # Display steps one by one
        st.subheader("Recipe Preparation Steps:")
        st.markdown("### Ingredients:")
        steps = selected_recipe['ingredient_lines']
        st.write(steps.iloc[0])

        # Display recipe URL
        st.markdown("### Recipe URL:")
        st.write(selected_recipe['url'].iloc[0])

        # Consume Recipe Today button
        if st.button('Consume Recipe Today'):
            st.session_state.selected_recipe_id = selected_recipe_id
            st.session_state.protein = selected_recipe['proteins_per_serving']
            st.session_state.calories = selected_recipe['calories_per_serving']
            st.session_state.carbs = selected_recipe['carbs_per_serving']
            st.session_state.fats = selected_recipe['fats_per_serving']
            st.write(f"Recipe ID {selected_recipe_id} has been selected to consume today!")
            st.write("Proteins Consumed",st.session_state.protein.iloc[0])
            st.write("Calories Consumed",st.session_state.calories.iloc[0])
            st.write("Carbs Consumed",st.session_state.carbs.iloc[0])
            st.write("Fats Consumed",st.session_state.fats.iloc[0])
            



        def update_nutrition_tracking(user_id,  calories_to_remove, proteins_to_remove, fats_to_remove, carbs_to_remove):
            nutrition_tracking_df = pd.read_csv("nutrition_tracking.csv")

            # Check if the row for the user_id and date exists
            mask = (nutrition_tracking_df['user_id'] == user_id)
            existing_rows = nutrition_tracking_df.loc[mask]

            if not existing_rows.empty:
                # Modify the existing row
                nutrition_tracking_df.loc[mask, 'calories_left'] += calories_to_remove.iloc[0]
                nutrition_tracking_df.loc[mask, 'proteins_left'] += proteins_to_remove.iloc[0]
                nutrition_tracking_df.loc[mask, 'fats_left'] += fats_to_remove.iloc[0]
                nutrition_tracking_df.loc[mask, 'carbs_left'] += carbs_to_remove.iloc[0]
            else:
                
                # Create a new entry
                new_entry = {
                    'user_id': user_id,
                    'calories_left': calories_to_remove.iloc[0],
                    'proteins_left': proteins_to_remove.iloc[0],
                    'fats_left': fats_to_remove.iloc[0],
                    'carbs_left': carbs_to_remove.iloc[0]
                }

                # Append the new entry to the DataFrame
        
                nutrition_tracking_df.loc[len(nutrition_tracking_df)]=new_entry
            st.session_state.user_id=user_id

            # Write the updated DataFrame back to CSV
            nutrition_tracking_df.to_csv('nutrition_tracking.csv', index=False)

        # Example usage
        update_nutrition_tracking(st.session_state.user_id , st.session_state.calories,
                                  st.session_state.protein, st.session_state.fats, st.session_state.carbs)

       


if __name__ == "__main__":
    main()
