import streamlit as st
import requests
import pandas as pd
from API_LimeSurvey import get_session_key, release_session_key, fetch_responses
from utils import get_score_icon, all_subpages_accessed, initialize_session_state
from Modules import BarChart, AreaChart, PieChart, LineChart, Maps, ScatterPlot, StackedBarChart  # type: ignore
from Modules import CherryPicking, ConcealedUncertainty, FalseAggregation, MisleadingAnnotation  # type: ignore
from Modules import MissingData, TruncatedAxis, MissingNormalization, Overplotting  # type: ignore
from Modules import FalseScaleDirection, FalseScaleFunction, FalseScaleOrder  # type: ignore
import plotly.graph_objects as go

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    )

# Custom CSS to adjust sidebar spacing and fix the final assessment at the bottom
sidebar_adjustment_style = """
    <style>
    .stButton button {
        width: 100%;
        margin: 0px;
    }
    /* Style for the final assessment link */
    .sidebar-link {
        position: absolute;
        bottom: 0;
        display: block;
        width: 100%;
        padding: 10px;
        text-align: center;
        border-radius: 5px;
        text-decoration: none;
        color: black;
        background-color: #f0f2f6;
        margin-top: 20px;
        font-weight: bold;
    }
    /* Adjust the top margin in the sidebar */
    .st-emotion-cache-1gwvy71 {
        position: start;
        padding-top: 0px !important;
        width:100%;
    }
    .st-emotion-cache-16i25t9 {
        position: start;
        padding-top: 0px !important;
        width:100%;
        gap: 0.5rem;
    }

    /* Make the sidebar container scrollable and fix the final block at the bottom */
       [data-testid="stSidebar"][aria-expanded="true"]{
           min-width: 350px;
           max-width: 350px;
           padding-bottom: 0px;
       }

    /* Fix the final assessment block at the bottom of the sidebar */
    [data-testid="stSidebar"] aside {
        position: fixed;
        bottom: 0;
        width: 300px;  /* Adjust width to match your sidebar */
        padding: 10px 0;
        background-color: #f0f2f6;
        border-top: 1px solid #ddd;
        text-align: center;
    }
    </style>
"""
st.markdown(sidebar_adjustment_style, unsafe_allow_html=True)


# Example of scores assigned to the two modules
basics = {
    'Area Chart': 0,
    'Bar Chart': 0,
    'Maps': 0,
    'Line Chart': 0,
    'Pie Chart': 0,
    'Scatter Plot': 3,
    'Stacked Bar Chart': 0,
}

# Example of scores assigned to the two modules
pitfalls = {
    'Cherry Picking': 2,
    'Concealed Uncertainty': 0,
    'False Aggregation': 0,
    'False Scale Order': 0,
    'False Scale Function': 0,
    'False Scale Direction': 0,
    'Misleading Annotation': 0,
    'Missing Data': 1,
    'Missing Normalization': 0,
    'Overplotting': 0,
    'Truncated Axis': 1
}

BarChartSubpages = ['Anatomy'] * 6 + ['Common Tasks associated to Bar Chart'] * 6 + ['Module Completed']
AreaChartSubpages = ['Anatomy'] * 7 + ['Common Tasks associated to Bar Chart'] * 8 + ['Module Completed']
LineChartSubpages = ['Anatomy'] * 6 + ['Common Tasks associated to Bar Chart'] * 7 + ['Module Completed']
MapsSubpages = ['Anatomy'] * 5 + ['Common Tasks associated to Bar Chart'] * 3 + ['Module Completed']
PieChartSubpages = ['Anatomy'] * 6 + ['Common Tasks associated to Bar Chart'] * 5 + ['Module Completed']
ScatterPlotSubpages = ['Anatomy'] * 7 + ['Common Tasks associated to Bar Chart'] * 7 + ['Module Completed']
StackedBarChartSubpages = ['Anatomy'] * 7 + ['Common Tasks associated to Bar Chart'] * 3 + ['Module Completed']
CherryPickingSubpages = [''] * 5 + ['Module Completed']
ConcealedUncertaintySubpages = [''] * 5 + ['Module Completed']
FalseAggregationSubpages =  [''] * 6 + ['Module Completed']
FalseScaleOrderSubpages = [''] * 6 + ['Module Completed']
FalseScaleFunctionSubpages = [''] * 6 + ['Module Completed']
FalseScaleDirectionSubpages = [''] * 6 + ['Module Completed']
MisleadingAnnotationSubpages =  [''] * 5 + ['Module Completed']
MissingDataSubpages =  [''] * 6 + ['Module Completed']
MissingNormalizationSubpages =  [''] * 6 + ['Module Completed']
OverplottingSubpages =  [''] * 5 + ['Module Completed']
TruncatedAxisSubpages =  [''] * 6 + ['Module Completed']



modules = {
    'Bar Chart': BarChartSubpages,
    'Area Chart': AreaChartSubpages,
    'Line Chart': LineChartSubpages,
    'Maps': MapsSubpages,
    'Pie Chart': PieChartSubpages,
    'Scatter Plot': ScatterPlotSubpages,
    'Stacked Bar Chart': StackedBarChartSubpages,
    'Cherry Picking': CherryPickingSubpages,
    'Concealed Uncertainty': ConcealedUncertaintySubpages,
    'False Aggregation': FalseAggregationSubpages,
    'False Scale Order': FalseScaleOrderSubpages,
    'False Scale Function': FalseScaleFunctionSubpages,
    'False Scale Direction': FalseScaleDirectionSubpages,
    'Misleading Annotation': MisleadingAnnotationSubpages,
    'Missing Data': MissingDataSubpages,
    'Missing Normalization': MissingNormalizationSubpages,
    'Overplotting': OverplottingSubpages,
    'Truncated Axis': TruncatedAxisSubpages,
}


# Define the URLs of your custom icons
icon_well_done   = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/02.Orienting/Icons/NotRecommended.png"

icon_improvement = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/02.Orienting/Icons/Recommended.png"

# Add custom CSS to target a specific button using a span element         
st.markdown("""
    <style>
    .element-container:has(#learning-buttons) + div button,
    .element-container:has(#home-button-after) + div button {
        background-color: #f0f2f6;
        color: #0068c9;
        border-radius: 2px;
        font-weight: bold;
        width: 100%;
        height: 1px;
        margin: 1px;
        padding: 1px;
        border: 2px solid #f0f2f6;
    }
    .element-container:has(#learning-buttons) + div button:hover,
    .element-container:has(#home-button-after) + div button:hover {
        background-color: #f0f2f6;
        border-color: #f0f2f6;
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

# Ensure session state is initialized before proceeding
#initialize_session_state(modules)

if 'accessed_subpages' not in st.session_state:
    initialize_session_state(modules)

# LimeSurvey API Configuration
USERNAME = "marianasteffens"  # Replace with your LimeSurvey admin username
PASSWORD = "MyThesis123"  # Replace with your LimeSurvey admin password
SURVEY_ID = "967331"


# Extract query parameters
try:
    query_params = st.query_params  # Attempt to fetch query parameters
    user_token_raw = query_params["token"]
    user_token = user_token_raw.strip().lower() if user_token_raw else ""
except Exception as e:
    # Handle any error by assigning a fallback URL and token
    #st.warning("No token found in the query parameters. Using a default token for testing.")
    user_token_raw = "NNCzENfS2kY27uI"  # Default dummy token for local testing
    user_token = user_token_raw.strip().lower() if user_token_raw else ""


# Handle missing token
if not user_token:
    st.error("No token provided in the URL. Please complete the survey.")


@st.cache_data
def fetch_survey_data(username, password, survey_id):
    """Fetch and cache survey responses."""
    session_key = get_session_key(username, password)
    if session_key:
        responses = fetch_responses(session_key, survey_id)
        release_session_key(session_key)
        return responses
    return None

# Fetch survey data once and cache it
responses = fetch_survey_data(USERNAME, PASSWORD, SURVEY_ID)

if responses:
    df = pd.DataFrame(responses["responses"])
    df["token"] = df["token"].astype(str).str.strip().str.lower()
    user_response = df[df["token"] == user_token]

    if not user_response.empty:
        # Calculate and display score
        correct_answers = {
            "N1": "AO02", "N2": "AO03", "N3": "AO03",
            "N4": "AO02", "N5": "AO01", "N6": "AO01",
            "N7": "AO01", "N8": "AO01"
        }

        user_score = sum(
            user_response.iloc[0][q] == a
            for q, a in correct_answers.items()
        )
    else:
        st.error("No response found for your token.")
else:
    st.error("Failed to fetch survey responses.")

if 'selected_module' not in st.session_state:
    st.session_state['selected_module'] = 'Home: My Scores'

# Dictionary to map module names to display functions
module_display_mapping = {
    'Bar Chart': BarChart.display_module,
    'Area Chart': AreaChart.display_module,
    'Line Chart': LineChart.display_module,
    'Maps': Maps.display_module,
    'Pie Chart': PieChart.display_module,
    'Scatter Plot': ScatterPlot.display_module,
    'Stacked Bar Chart': StackedBarChart.display_module,
    'Cherry Picking': CherryPicking.display_module,
    'Concealed Uncertainty': ConcealedUncertainty.display_module,
    'False Aggregation': FalseAggregation.display_module,
    'False Scale Order': FalseScaleOrder.display_module,
    'False Scale Function': FalseScaleFunction.display_module,
    'False Scale Direction': FalseScaleDirection.display_module,
    'Misleading Annotation': MisleadingAnnotation.display_module,
    'Missing Data': MissingData.display_module,
    'Missing Normalization': MissingNormalization.display_module,
    'Overplotting': Overplotting.display_module,
    'Truncated Axis': TruncatedAxis.display_module,
}

st.sidebar.markdown('<span id="home-button-after"></span>', unsafe_allow_html=True)
if st.sidebar.button("Home: My Scores"):
    st.session_state['selected_module'] = 'Home: My Scores'

# Function to render a styled section header
def render_section_header(main_header, sub_header):
    """
    Render a styled section header with a main title and sub-title.
    
    Args:
        main_header (str): The main header (e.g., "Content Recommended").
        sub_header (str): The sub-header (e.g., "Basics").
    """
    st.sidebar.markdown(
        f"""
        <div style="padding: 10px 0;">
            <h4 style="margin: 0; font-size: 16px; color: #333;">{sub_header}</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )

def categorize_modules(basics, pitfalls):
    """
    Categorize and sort modules into four sections based on scores.
    
    Args:
        basics (dict): Scores for basics modules.
        pitfalls (dict): Scores for pitfalls modules.
    
    Returns:
        dict: A dictionary with categorized and sorted modules.
    """
    categorized = {
        "Recommended: Basics": sorted(
            [module for module, score in basics.items() if score > 0],
            key=lambda x: basics[x],
            reverse=True
        ),
        "Recommended: Common Pitfalls": sorted(
            [module for module, score in pitfalls.items() if score > 0],
            key=lambda x: pitfalls[x],
            reverse=True
        ),
        "Other: Pitfalls": sorted(
            [module for module, score in pitfalls.items() if score == 0]
        ),
        "Other: Basics": sorted(
            [module for module, score in basics.items() if score == 0]
        ),
    }
    return categorized


# Categorize modules with sorting
categorized_modules = categorize_modules(basics, pitfalls)

# Define the main sections and their subcategories
sections = {
    "Top Recommended": ["Recommended: Basics", "Recommended: Common Pitfalls"],
    "Others": ["Other: Basics", "Other: Pitfalls"],
}

# Render the sidebar content
for main_section, sub_sections in sections.items():
    # Render the main section header
    st.sidebar.markdown(f"<h1 style='font-size: 22px; color: #333;'>{main_section}</h1>", unsafe_allow_html=True)
    for sub_section in sub_sections:
        # Render the sub-section header
        render_section_header(main_section, sub_section.split(": ")[1])  # Extract "Basics" or "Common Pitfalls"
        # Display modules under the sub-section
        for module in categorized_modules.get(sub_section, []):
            # Determine score and accessed status
            score = basics.get(module, pitfalls.get(module, 0))  # Get the score from basics or pitfalls
            score_icon = get_score_icon(score)
            accessed_icon = '✔️' if all_subpages_accessed(module, modules) else ' '

            # Display module button with icon
            col1, col2 = st.sidebar.columns([0.6, 4])
            with col1:
                st.markdown(f'<img src="{score_icon}" width="35px">', unsafe_allow_html=True)
            with col2:
                if st.button(f"{module} {accessed_icon}", key=f"{module}_button"):
                    st.session_state['selected_module'] = module

# Display content based on selection
selected_module = st.session_state['selected_module']

if selected_module == 'Home: My Scores':
    # Center the title
    st.markdown(f"<h1 style='text-align: center;'>{'Visualization Literacy Assessment'}</h1>", unsafe_allow_html=True)
    
    # Add the Plotly gauge chart with improved styling and black numbers
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=user_score,  # Replace with your desired score variable if needed
        number={'font': {'color': 'black', 'size': 100}},  # Set the inside value to black and larger size
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "My Scores", 'font': {'size': 26, 'color': "#2b2b2b"}},  # Modern font and color for the title

        gauge={
            'axis': {'range': [0, 30], 'tickwidth': 2, 'tickcolor': "black", 'tickfont': {'size': 14, 'color': 'black'}},  # Black tick labels
            'bar': {'color': "rgba(0,127,255,0.8)", 'thickness': 0.3},  # Gradient-like bar color # "rgba(0,127,255,0.8)
            'bgcolor': "#f5f5f5",  # Subtle background color
            'borderwidth': 2,
            'bordercolor': "#d9d9d9",  # Soft border color
            'steps': [
                {'range': [0, 10], 'color': "#d6e5ff"},  # Light blue for lower range
                {'range': [10, 20], 'color': "#d6e5ff"},  # Medium blue
                {'range': [20, 30], 'color': "#d6e5ff"}   # Dark blue
            ],
            'threshold': {
                'line': {'color': "#ff6666", 'width': 6},  # Soft red threshold line
                'thickness': 0.75,
                'value': user_score  # Replace with your dynamic score if needed
            }
        }
    ))

    # Set the layout to make the gauge chart smaller and centered
    fig.update_layout(
        height=300,  # Set height
        width=600,   # Set a fixed width to prevent shifting
        margin=dict(t=80, b=40, l=20, r=20),  # Adjust margin for better spacing
        paper_bgcolor="#ffffff",  # Clean background
    )

    # Use three columns and plot the chart in the second column
    col1, col2, col3 = st.columns([1, 2, 1])  # Adjust the width ratios if necessary

    with col2:
        st.plotly_chart(fig, use_container_width=False, config={'displayModeBar': False})  # Disable toolbar and center chart


    # Add the message with styled text and emoji below the gauge chart
    st.markdown(f"""
        ### Keep Learning!
        To get further insights into Visualization Literacy and improve your scores, check out the content by navigating through the menu on the left.
        
        **Legend:**
        
        - <span style="color:black"><img src="{icon_well_done}" width="22px" >  Well done! You seem to master this topic! </span>
        - <span style="color:black"><img src="{icon_improvement}" width="22px" >  There is some room for improvement here :) </span>
    """, unsafe_allow_html=True)

else:
    # Load only the selected module's content
    if selected_module in module_display_mapping:
        module_display_mapping[selected_module](modules)


# Fixed block for Final Assessment in the sidebar
final_assessment_html = """
    <aside>
        <a href="https://example.com/final-assessment" target="_blank" class="sidebar-link">
            Final Assessment
        </a>
    </aside>
"""

st.sidebar.markdown(final_assessment_html, unsafe_allow_html=True)
