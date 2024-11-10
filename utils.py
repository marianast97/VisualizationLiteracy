import streamlit as st

GOOD_SCORE_THRESHOLD = 1

# Function to initialize session state for all modules
def initialize_session_state(modules):
    if 'accessed_subpages' not in st.session_state:
        st.session_state['accessed_subpages'] = {module: [False] * len(subpages) for module, subpages in modules.items()}
    
    if 'current_subpage' not in st.session_state:
        st.session_state['current_subpage'] = {module: 0 for module in modules}

# Function to initialize session state for a specific module
def initialize_single_module_state(module_name, modules):
    # Ensure 'accessed_subpages' and 'current_subpage' are initialized for the specific module
    if 'accessed_subpages' in st.session_state and module_name not in st.session_state['accessed_subpages']:
        st.session_state['accessed_subpages'][module_name] = [False] * len(modules[module_name])

    if 'current_subpage' in st.session_state and module_name not in st.session_state['current_subpage']:
        st.session_state['current_subpage'][module_name] = 0

# Function to display content for each subpage of a module
def display_subpage(module_name, subpage_index, modules):
    subpage_name = modules[module_name][subpage_index]
    
    # Center the title
    st.markdown(f"<h1 style='text-align: center;'>{module_name}</h1>", unsafe_allow_html=True)
    # Center the subpage name
    st.markdown(f"<h3 style='text-align: center;'>{subpage_name}</h3>", unsafe_allow_html=True)
    #st.title(module_name)
    #st.write(f"### {module_name} - {subpage_name}")
    # st.write(f"This is the content for {subpage_name} in {module_name}.")
    
    st.session_state['accessed_subpages'][module_name][subpage_index] = True

# Function to get an icon based on score
def get_score_icon(score):
    if score >= GOOD_SCORE_THRESHOLD:
        return "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/IconRight2.png"

    else:
        return "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/IconWrong2.png"

# Function to handle subpage navigation
def navigate_subpage(module_name, direction, modules):
    current_index = st.session_state['current_subpage'][module_name]
    if direction == 'next' and current_index < len(modules[module_name]) - 1:
        st.session_state['current_subpage'][module_name] += 1
    elif direction == 'prev' and current_index > 0:
        st.session_state['current_subpage'][module_name] -= 1

# Function to check if all subpages of a module are accessed
def all_subpages_accessed(module_name, modules):
    if module_name in st.session_state['accessed_subpages']:
        return all(st.session_state['accessed_subpages'][module_name])
    return False



