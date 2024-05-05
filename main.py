import streamlit as st
import loginapp
import home
import page2
import warnings
warnings.filterwarnings('ignore')

def main():
    st.title("NutritionME.")

    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False

    if not st.session_state.is_logged_in:
        loginapp.main()
    else:
        # Page selection
        page = st.sidebar.selectbox("Go to", ["Dashboard", "Recipies"])

        if page == "Dashboard":
            home.main()

        elif page == "Recipies":
            page2.main()

if __name__ == "__main__":
    main()
