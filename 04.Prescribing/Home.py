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


BarChartSubpages = ['Anatomy'] * 6 + ['Common Tasks associated to Bar Chart'] * 6 + ['Module Completed']
AreaChartSubpages = ['Anatomy'] * 7 + ['Common Tasks associated to Bar Chart'] * 8 + ['Module Completed']
LineChartSubpages = ['Anatomy'] * 6 + ['Common Tasks associated to Bar Chart'] * 7 + ['Module Completed']
MapsSubpages = ['Anatomy'] * 5 + ['Common Tasks associated to Bar Chart'] * 3 + ['Module Completed']
PieChartSubpages = ['Anatomy'] * 6 + ['Common Tasks associated to Bar Chart'] * 5 + ['Module Completed']
ScatterPlotSubpages = ['Anatomy'] * 7 + ['Common Tasks associated to Bar Chart'] * 7 + ['Module Completed']
StackedBarChartSubpages = ['Anatomy'] * 7 + ['Common Tasks associated to Bar Chart'] * 3 + ['Module Completed']
CherryPickingSubpages = [''] * 6 + ['Module Completed']
ConcealedUncertaintySubpages = [''] * 6 + ['Module Completed']
FalseAggregationSubpages =  [''] * 7 + ['Module Completed']
FalseScaleOrderSubpages = [''] * 7 + ['Module Completed']
FalseScaleFunctionSubpages = [''] * 7 + ['Module Completed']
FalseScaleDirectionSubpages = [''] * 7 + ['Module Completed']
MisleadingAnnotationSubpages =  [''] * 6 + ['Module Completed']
MissingDataSubpages =  [''] * 7 + ['Module Completed']
MissingNormalizationSubpages =  [''] * 7 + ['Module Completed']
OverplottingSubpages =  [''] * 6 + ['Module Completed']
TruncatedAxisSubpages =  [''] * 7 + ['Module Completed']



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
SURVEY_ID = "177584"


# Extract query parameters
try:
    query_params = st.query_params  # Attempt to fetch query parameters
    user_token_raw = query_params["token"]
    user_token = user_token_raw  if user_token_raw else "" #.strip().lower()
except Exception as e:
    # Handle any error by assigning a fallback URL and token
    #st.warning("No token found in the query parameters. Using a default token for testing.")
    user_token_raw = "8aFs1OeBIzaV1vR"  # Default dummy token for local testing
    user_token = user_token_raw if user_token_raw else "" #.strip().lower() 


# Handle missing token
if not user_token:
    st.error("No token provided in the URL. Please complete the survey.")


#@st.cache_data
def fetch_survey_data(username, password, survey_id):
    """Fetch and cache survey responses."""
    session_key = get_session_key(username, password)
    if session_key:
        responses = fetch_responses(session_key, survey_id)
        release_session_key(session_key)
        return responses
    return None

# Define the mapping of modules to their respective questions
basics_mapping = {
    'Area Chart': ["N08", "N09"],
    'Bar Chart': ["N01", "N02"],
    'Maps':  ["N14", "N15"],
    'Line Chart': ["N06", "N07"],
    'Pie Chart': ["N12", "N13"],
    'Scatter Plot': ["N10", "N11"],
    'Stacked Bar Chart': ["N03", "N04", "N05"],
    }

pitfalls_mapping = {
    'Cherry Picking': ["T43"],
    'Concealed Uncertainty': ["T48"],
    'False Aggregation': ["T35", "T37"],
    'False Scale Order': ["T20", "T25"],
    'False Scale Function': ["T26"],
    'False Scale Direction': ["T10", "T14"],
    'Misleading Annotation': ["T47", "T49"],
    'Missing Data': ["T30"],
    'Missing Normalization': ["T42"],
    'Overplotting': ["T40"],
    'Truncated Axis': ["T03"],
    }

# Correct answers for all questions
correct_answers = {
    "N01": "AO02", "N02": "AO03", "N03": "AO02",
    "N04": "AO03", "N05": "AO02", "N06": "AO01",
    "N07": "AO02", "N08": "AO01", "N09": "AO04",
    "N10": "AO01", "N11": "AO03", "N12": "AO02",
    "N13": "AO03", "N14": "AO01", "N15": "AO03",
    "T03": "AO04", "T10": "AO02", "T14": "AO03",
    "T20": "AO04", "T25": "AO03", "T26": "AO04",
    "T30": "AO03", "T35": "AO04", "T37": "AO04",
    "T40": "AO03", "T42": "AO04", "T43": "AO04",
    "T47": "AO02", "T48": "AO04", "T49": "AO03",
}

# Fetch survey data once and cache it
responses = fetch_survey_data(USERNAME, PASSWORD, SURVEY_ID)

if responses:
    df = pd.DataFrame(responses["responses"])
    df["token"] = df["token"].astype(str).str.strip()#.str.lower()
    user_response = df[df["token"] == user_token]

    if not user_response.empty:

        basics = {module: 0 for module in basics_mapping.keys()}
        pitfalls = {module: 0 for module in pitfalls_mapping.keys()}  

        # Calculate scores for basics
        for module, questions in basics_mapping.items():
            incorrect_count = sum(
                user_response.iloc[0].get(question, None) != correct_answers.get(question, None)
                for question in questions
            )
            basics[module] = incorrect_count

        # Calculate scores for pitfalls
        for module, questions in pitfalls_mapping.items():
            incorrect_count = sum(
                user_response.iloc[0].get(question, None) != correct_answers.get(question, None)
                for question in questions
            )
            pitfalls[module] = incorrect_count
        
        # Calculate overall user score
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

# Filter modules for recommended basics and pitfalls (score == 0)
recommended_basics = {k: v for k, v in basics.items() if v >= 1}
recommended_pitfalls = {k: v for k, v in pitfalls.items() if v >= 1}

# Filter the modules dictionary to include only recommended modules
filtered_modules = {
    k: v
    for k, v in modules.items()
    if k in recommended_basics or k in recommended_pitfalls
}

# Filter the modules dictionary to include only unfiltered modules
unfiltered_modules = {
    k: v
    for k, v in modules.items()
    if k not in recommended_basics and k not in recommended_pitfalls
}

# Define the URLs of your custom icons
icon_well_done   = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/04.Prescribing/Icons/NotRecommended.png"

icon_improvement = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/main/02.Orienting/Icons/book-solid.svg"

st.sidebar.markdown('<span id="home-button-after"></span>', unsafe_allow_html=True)
if st.sidebar.button("Home: My Scores"):
    st.session_state['selected_module'] = 'Home: My Scores'

# Sidebar Basics section
#st.sidebar.header("Top Recommended")

st.sidebar.subheader("Basics")
for module, score in recommended_basics.items():
    #score_icon = get_score_icon(score)
    #accessed_icon = '✔️' if all_subpages_accessed(module, modules) else ' '

    accessed_icon = '✔️' if all_subpages_accessed(module, modules) else ' '

    score_icon = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/main/04.Prescribing/Icons/book-solid-gray.svg" if all_subpages_accessed(module, modules) and score>0 else get_score_icon(score)

    col1, col2 = st.sidebar.columns([0.5, 4])
    with col1:
        #st.markdown(f'<img src="{score_icon}" width="35px">', unsafe_allow_html=True)
        # Center-align the icon using HTML and CSS
        st.markdown(f"""
        <div style="
            margin-top: 3px;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 35px;  /* Ensure icon height matches button height */
            width: 35px;">
            <img src="{score_icon}" width="35px" style="vertical-align: middle;">
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button(f"{module} {accessed_icon}", key=f"{module}_button"):
            st.session_state['selected_module'] = module

# Sidebar Common Pitfalls section
st.sidebar.subheader("Common Pitfalls")
for module, score in recommended_pitfalls.items():
    #score_icon = get_score_icon(score)
    #accessed_icon = '✔️' if all_subpages_accessed(module, modules) else ' '
    
    accessed_icon = '✔️' if all_subpages_accessed(module, modules) else ' '

    score_icon = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/main/04.Prescribing/Icons/book-solid-gray.svg" if all_subpages_accessed(module, modules) and score>0 else get_score_icon(score)

    col1, col2 = st.sidebar.columns([0.5, 4])
    with col1:
        #st.markdown(f'<img src="{score_icon}" width="35px">', unsafe_allow_html=True)
        # Center-align the icon using HTML and CSS
        st.markdown(f"""
        <div style="
            margin-top: 3px;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 35px;  /* Ensure icon height matches button height */
            width: 35px;">
            <img src="{score_icon}" width="35px" style="vertical-align: middle;">
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button(f"{module} {accessed_icon}", key=f"{module}_button"):
            st.session_state['selected_module'] = module

# Add an expander for showing all unfiltered modules in the sidebar
with st.sidebar.expander("Show All Modules", expanded=False):
    #st.subheader("All Modules")
    for module in modules.keys(): #unfiltered_modules
        accessed_icon = '✔️' if all_subpages_accessed(module, modules) else ' '
        
        # Dynamic icon logic
        #score_icon = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/main/04.Prescribing/Icons/book-solid-gray.svg" \
        #             if all_subpages_accessed(module, modules) else icon_improvement

        # Use consistent layout without X markers
        col1, col2 = st.columns([0.5, 4])
        #with col1:
        #    st.markdown(
        #        f'<img src="{score_icon}" width="20px" style="vertical-align: middle; margin-right: 5px;">',
        #        unsafe_allow_html=True
        #    )
        with col2:
            if st.button(f"{module} {accessed_icon}", key=f"all_{module}_button"):
                st.session_state['selected_module'] = module


# Display content based on selection
selected_module = st.session_state['selected_module']

if selected_module == 'Home: My Scores':
    # Center the title
    st.markdown(f"<h1 style='text-align: center;'>{'Visualization Literacy Assessment'}</h1>", unsafe_allow_html=True)
            
    st.markdown(
            """
            <div style="text-align: center; font-size: 20px; ">
                <strong>Visualization Literacy</strong> is the ability to understand, interpret and think critically about visual representations of data, enabling the discovery of patterns and insights.
                By mastering it, we can simplify complex information, promote informed collaboration, and challenge misleading visuals for a  <b>more critical</b> and  <b>informed society</b>.
            </div>
            """,
            unsafe_allow_html=True
            )
    
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
        ### Let's improve your skills!        
    """, unsafe_allow_html=True)

    st.markdown(f"<p style='text-align: left; font-size: 20px;'>{'To get further insights into Visualization Literacy, check out the content by navigating through the menu on the left.'}</p>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align: left; align-items: left; font-size: 20px;">
        <div style="margin-bottom: 5px;">
            Note: The Icon <img src="{icon_improvement}" width="15px" style="vertical-align: middle; margin-right: 5px; margin-left: 5px;"> indicates that the module is recommended based on your assessment.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Add the message with styled text and emoji below the gauge chart
    st.markdown(f"""
        ###       
    """, unsafe_allow_html=True)


    st.info("Once you feel confident with your learning, proceed to the Final Assessment located at the bottom of the sidebar.")




else:
    # Load only the selected module's content
    if selected_module in module_display_mapping:
        module_display_mapping[selected_module](modules)


# HTML block with JavaScript to reload if "Access code mismatch" occurs
final_assessment_html = f"""
    <aside>
        <a href="https://userpage.fu-berlin.de/~hcc/survey-research/index.php/593693?token={user_token}&lang=en" target="_blank" class="sidebar-link" onclick="checkErrorAndReload()">
            Final Assessment
        </a>
    </aside>
    <script>
        function checkErrorAndReload() {{
            window.open("https://userpage.fu-berlin.de/~hcc/survey-research/index.php/593693?token={user_token}&lang=en", "_blank");
            setTimeout(() => {{ window.location.reload(); }}, 1000); // Reload after 1 second
        }}
    </script>
"""
st.sidebar.markdown(final_assessment_html, unsafe_allow_html=True)