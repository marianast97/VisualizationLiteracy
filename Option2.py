import streamlit as st

# Set a threshold for good/bad scores
GOOD_SCORE_THRESHOLD = 70

# Example of scores assigned to different modules (pages)
pages = {
    'Advanced Visualizations': 85,
    'Basic Charts': 50,
    'Intermediate Graphs': 70,
    'Interactive Data': 90
}

# Define subpages for each module
modules = {
    'Advanced Visualizations': ['Overview', 'Techniques', 'Examples'],
    'Basic Charts': ['Introduction', 'Bar Charts', 'Line Charts'],
    'Intermediate Graphs': ['Scatter Plots', 'Histograms', 'Box Plots'],
    'Interactive Data': ['Dashboarding', 'Interactivity', 'Dynamic Data']
}

# Initialize session state to track accessed pages and subpage navigation
if 'accessed_subpages' not in st.session_state:
    st.session_state['accessed_subpages'] = {module: [False] * len(subpages) for module, subpages in modules.items()}

if 'current_subpage' not in st.session_state:
    st.session_state['current_subpage'] = {module: 0 for module in modules}

if 'selected_module' not in st.session_state:
    st.session_state['selected_module'] = None

# Function to display content for each subpage of a module
def display_subpage(module_name, subpage_index):
    subpage_name = modules[module_name][subpage_index]
    st.write(f"### {module_name} - {subpage_name}")
    st.write(f"This is the content for {subpage_name} in {module_name}.")
    
    # Mark the subpage as accessed
    st.session_state['accessed_subpages'][module_name][subpage_index] = True

# Function to get an icon based on score
def get_score_icon(score):
    if score >= GOOD_SCORE_THRESHOLD:
        return '👍'  # Good score icon
    else:
        return '👎'  # Bad score icon

# Function to handle subpage navigation
def navigate_subpage(module_name, direction):
    current_index = st.session_state['current_subpage'][module_name]
    if direction == 'next' and current_index < len(modules[module_name]) - 1:
        st.session_state['current_subpage'][module_name] += 1
    elif direction == 'prev' and current_index > 0:
        st.session_state['current_subpage'][module_name] -= 1

# Function to check if all subpages of a module are accessed
def all_subpages_accessed(module_name):
    return all(st.session_state['accessed_subpages'][module_name])

# Sort pages based on scores (highest first)
sorted_pages = sorted(pages.items(), key=lambda x: x[1], reverse=True)

# Streamlit sidebar navigation with icons and accessed status
st.sidebar.title("Learning Content Navigation")

# Display buttons for each module in the sidebar
for module, score in sorted_pages:
    # Icon for good/bad score
    score_icon = get_score_icon(score)
    
    # Check if all subpages are accessed
    if all_subpages_accessed(module):
        accessed_icon = '✅'
    else:
        accessed_icon = '⬜'

    # Create button for each module
    if st.sidebar.button(f"{score_icon} {accessed_icon} {module} (Score: {score})"):
        st.session_state['selected_module'] = module

# Check if a module is selected
if st.session_state['selected_module']:
    selected_module = st.session_state['selected_module']
    
    # Show content for the selected module's current subpage
    current_subpage_index = st.session_state['current_subpage'][selected_module]
    display_subpage(selected_module, current_subpage_index)

    # "Previous" and "Next" navigation buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Previous"):
            navigate_subpage(selected_module, 'prev')

    with col2:
        if st.button("Next"):
            navigate_subpage(selected_module, 'next')

    # Show navigation status (page number)
    st.write(f"Subpage {current_subpage_index + 1} of {len(modules[selected_module])}")
else:
    st.write("Please select a module from the sidebar to begin.")
