import streamlit as st

SCORE_THRESHOLD = 0

# Base URL for accessing files directly from GitHub's raw content
GITHUB_BASE_URL = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/main/02.Orienting/LearningContent"

# Function to initialize session state for all modules
def initialize_session_state(modules):
    if 'accessed_subpages' not in st.session_state:
        st.session_state['accessed_subpages'] = {module: [False] * len(subpages) for module, subpages in modules.items()}
    
    if 'current_subpage' not in st.session_state:
        st.session_state['current_subpage'] = {module: 0 for module in modules}

# Function to initialize session state for a specific module
def initialize_single_module_state(module_name, modules):
    if 'accessed_subpages' in st.session_state and module_name not in st.session_state['accessed_subpages']:
        st.session_state['accessed_subpages'][module_name] = [False] * len(modules[module_name])

    if 'current_subpage' in st.session_state and module_name not in st.session_state['current_subpage']:
        st.session_state['current_subpage'][module_name] = 0

# Function to get image files for a specific chart type
def get_image_files(chart_type):
    """
    Return the list of image files for a given chart type.
    
    Args:
        chart_type (str): The name of the chart type (e.g., "AreaChart", "BarChart").
        
    Returns:
        list: List of image file names.
    """
    return IMAGE_FILES.get(chart_type, [])

# Function to get base URL for a specific chart type
def get_base_url(chart_type):
    """
    Get the base URL for fetching chart images from the GitHub repository.
    
    Args:
        chart_type (str): The name of the chart type (e.g., "AreaChart", "BarChart").
        
    Returns:
        str: The base URL for the chart type.
    """
    return f"{GITHUB_BASE_URL}/{chart_type}/{chart_type}"

# Function to display content for each subpage of a module
def display_subpage(module_name, subpage_index, modules):
    subpage_name = modules[module_name][subpage_index]
    
    # Center the title
    st.markdown(f"<h1 style='text-align: center;'>{module_name}</h1>", unsafe_allow_html=True)
    # Center the subpage name
    st.markdown(f"<h3 style='text-align: center;'>{subpage_name}</h3>", unsafe_allow_html=True)
    
    st.session_state['accessed_subpages'][module_name][subpage_index] = True

# Function to get an icon based on score
def get_score_icon(score):
    if score > SCORE_THRESHOLD:
        return f"https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/main/02.Orienting/Icons/Recommended.png"
    else:
        return f"https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/main/02.Orienting/Icons/NotRecommended.png"

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

# Dictionary containing image files for each module
IMAGE_FILES = {
    "CherryPicking": [
        f"https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/01.NoGuidance/LearningContent/CherryPicking/CherryPicking%20({i}).png"
        for i in range(1, 7)
    ],
    "AreaChart": [
        f"https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/02.Orienting/LearningContent/AreaChart/AreaChart%20({i}).png"
        for i in range(1, 17)
    ],
    "BarChart": [
        f"https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/02.Orienting/LearningContent/BarChart/BarChart%20({i}).png"
        for i in range(1, 14)
    ],
    "ConcealedUncertainty": [
        f"https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/03.Misleading/LearningContent/ConcealedUncertainty/ConcealedUncertainty%20({i}).png"
        for i in range(1, 7)
    ],
    "InappropriateAggregation": [
        f"https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/03.Misleading/LearningContent/InappropriateAggregation/InappropriateAggregation%20({i}).png"
        for i in range(1, 8)
    ],
    "InappropriateScaleDirection": [
        f"https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/03.Misleading/LearningContent/InappropriateScaleDirection/InappropriateScaleDirection%20({i}).png"
        for i in range(1, 8)
    ],
    "InappropriateScaleFunction": [
        f"https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/03.Misleading/LearningContent/InappropriateScaleFunction/InappropriateScaleFunction%20({i}).png"
        for i in range(1, 8)
    ],
    "InappropriateScaleOrder": [
        f"https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/03.Misleading/LearningContent/InappropriateScaleOrder/InappropriateScaleOrder%20({i}).png"
        for i in range(1, 8)
    ],
    "LineChart": [
        f"https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/02.Orienting/LearningContent/LineChart/LineChart%20({i}).png"
        for i in range(1, 15)
    ],
    "Maps": [
        f"https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/02.Orienting/LearningContent/Maps/Maps%20({i}).png"
        for i in range(1, 10)
    ],
    "MisleadingAnnotation": [
        f"https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/03.Misleading/LearningContent/MisleadingAnnotation/MisleadingAnnotation%20({i}).png"
        for i in range(1, 7)
    ],
    "MissingData": [
        f"https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/03.Misleading/LearningContent/MissingData/MissingData%20({i}).png"
        for i in range(1, 8)
    ],
    "MissingNormalization": [
        f"https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/03.Misleading/LearningContent/MissingNormalization/MissingNormalization%20({i}).png"
        for i in range(1, 8)
    ],
    "Overplotting": [
        f"https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/03.Misleading/LearningContent/Overplotting/Overplotting%20({i}).png"
        for i in range(1, 7)
    ],
    "PieChart": [
        f"https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/02.Orienting/LearningContent/PieChart/PieChart%20({i}).png"
        for i in range(1, 13)
    ],
    "ScatterPlot": [
        f"https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/02.Orienting/LearningContent/ScatterPlot/ScatterPlot%20({i}).png"
        for i in range(1, 16)
    ],
    "StackedBarChart": [
        f"https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/02.Orienting/LearningContent/StackedBarChart/StackedBarChart%20({i}).png"
        for i in range(1, 12)
    ],
    "TruncatedAxis": [
        f"https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/03.Misleading/LearningContent/TruncatedAxis/TruncatedAxis%20({i}).png"
        for i in range(1, 8)
    ],
}
