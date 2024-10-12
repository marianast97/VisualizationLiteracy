import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Home",
    layout="centered", #centered #wide
    initial_sidebar_state="auto", #collapsed
)

# Main page title and welcome message
st.title("lOVINHO BONITINHO")

#st.logo(
#    "./love.png",
#    icon_image="./heartbeat.gif",
#)

st.markdown("""
To get further insights into Visualization Literacy and improve your scores,
check out the content by by navigating through the menu on the left.
""")

# Display image on Home
#st.image("./MomArt.jpeg", use_column_width=True)

#st.sidebar.header("\n")
#st.sidebar.subheader("App Developers:", divider="red")
#st.sidebar.write("Aditya Panchal")
#st.sidebar.markdown("Mariana Steffens")
#st.sidebar.markdown("Navya Reddy Tiyyagura")
#st.sidebar.markdown("Se Yeon Kim")
#st.sidebar.markdown("##### :gray[App developed as part of the Human Centered Data Science course during SoSe-24 at the Freie Universität Berlin]")
#st.sidebar.markdown("##### :gray[16.07.2024]")

import streamlit as st

# Set a threshold for good/bad scores
GOOD_SCORE_THRESHOLD = 70

# Example of scores assigned to different pages
pages = {
    'Advanced Visualizations': 85,
    'Basic Charts': 50,
    'Intermediate Graphs': 70,
    'Interactive Data': 90
}

# Initialize session state to track accessed pages
if 'accessed_pages' not in st.session_state:
    st.session_state['accessed_pages'] = {}

# Function to display content for each page
def display_content(page_name):
    st.write(f"### {page_name} Content")
    st.write(f"This is the content for {page_name}.")
    
    # Mark page as accessed
    st.session_state['accessed_pages'][page_name] = True

# Function to get icon based on score
def get_score_icon(score):
    if score >= GOOD_SCORE_THRESHOLD:
        return '👍'  # Good score icon
    else:
        return '👎'  # Bad score icon

# Sort pages based on scores (highest first)
sorted_pages = sorted(pages.items(), key=lambda x: x[1], reverse=True)

# Streamlit sidebar navigation with icons and accessed status
st.sidebar.title("Learning Content Navigation")

for page, score in sorted_pages:
    # Icon for good/bad score
    score_icon = get_score_icon(score)
    
    # Check if the page was accessed
    if page in st.session_state['accessed_pages']:
        accessed_icon = '✅'  # Icon for accessed page
    else:
        accessed_icon = '⬜'  # Icon for non-accessed page

    # Create sidebar buttons with icons and track access
    if st.sidebar.button(f"{score_icon} {page} {accessed_icon}"):
        display_content(page)

# Display a message if a page is selected
st.write("Select a learning content page from the sidebar to view.")

