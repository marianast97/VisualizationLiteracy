import streamlit as st
from utils import get_score_icon, all_subpages_accessed, navigate_subpage, initialize_session_state
import module_advanced_visualizations
import module_basic_charts

# Example of scores assigned to the two modules
pages = {
    'Advanced Visualizations': 85,
    'Basic Charts': 50
}

modules = {
    'Advanced Visualizations': ['Overview', 'Techniques', 'Examples'],
    'Basic Charts': ['Introduction', 'Bar Charts', 'Line Charts']
}

# Ensure session state is initialized before proceeding
initialize_session_state(modules)

if 'selected_module' not in st.session_state:
    st.session_state['selected_module'] = None

# Sort pages based on scores (highest first)
sorted_pages = sorted(pages.items(), key=lambda x: x[1], reverse=True)

# Streamlit sidebar navigation with icons and accessed status
st.sidebar.title("Learning Content Navigation")

# Display buttons for each module in the sidebar
for module, score in sorted_pages:
    # Icon for good/bad score
    score_icon = get_score_icon(score)
    
    # Check if all subpages are accessed (use try/except to ensure initialization happens smoothly)
    try:
        if all_subpages_accessed(module, modules):
            accessed_icon = '✅'
        else:
            accessed_icon = '⬜'
    except KeyError:
        accessed_icon = '⬜'

    # Create button for each module
    if st.sidebar.button(f"{score_icon} {accessed_icon} {module} (Score: {score})"):
        st.session_state['selected_module'] = module

# Check if a module is selected and import the relevant module
if st.session_state['selected_module']:
    selected_module = st.session_state['selected_module']
    
    if selected_module == 'Advanced Visualizations':
        module_advanced_visualizations.display_module(modules)

    elif selected_module == 'Basic Charts':
        module_basic_charts.display_module(modules)

else:
    st.write("Please select a module from the sidebar to begin.")

