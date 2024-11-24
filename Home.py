import streamlit as st
import requests
import pandas as pd
from API_LimeSurvey import get_session_key, release_session_key, fetch_responses
from utils import get_score_icon, all_subpages_accessed, initialize_session_state
from Modules import BarChart, AreaChart, PieChart, LineChart, Maps, ScatterPlot, StackedBarChart  # type: ignore
from Modules import CherryPicking, ConcealedUncertainty, InappropriateAggregation, MisleadingAnnotation  # type: ignore
from Modules import MissingData, TruncatedAxis, MissingNormalization, Overplotting  # type: ignore
from Modules import InappropriateScaleDirection, InappropriateScaleFunction, InappropriateScaleOrder  # type: ignore
import plotly.graph_objects as go

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    )

# LimeSurvey API Configuration
USERNAME = "marianasteffens"  # Replace with your LimeSurvey admin username
PASSWORD = "MyThesis123"  # Replace with your LimeSurvey admin password
SURVEY_ID = "967331"

# Extract token from the URL
query_params = st.query_params
user_token = query_params.get("token", [""])[0].strip().lower()

if not user_token:
    st.error("No token provided in the URL. Please complete the survey or ensure the token is passed.")
    st.stop()

# Authenticate and fetch data
session_key = get_session_key(USERNAME, PASSWORD)
if session_key:
    responses = fetch_responses(session_key, SURVEY_ID)
    release_session_key(session_key)

    if responses:
        # Convert responses to a DataFrame
        df = pd.DataFrame(responses["responses"])

        # Normalize token column and filter by user token
        df["token"] = df["token"].astype(str).str.strip().str.lower()
        user_response = df[df["token"] == user_token]

        if not user_response.empty:
            # Display user's response
            st.write("### Your Survey Response:")
            st.dataframe(user_response)

            # Add logic to calculate the score
            correct_answers = {
                "N1": "AO02",
                "N2": "AO03",
                "N3": "AO03",
                "N4": "AO02",
                "N5": "AO01",
                "N6": "AO01",
                "N7": "AO02",
                "N8": "AO03"
            }

            # Check correctness of answers
            user_score = 0
            for question, correct_answer in correct_answers.items():
                if user_response.iloc[0][question] == correct_answer:
                    user_score += 1

            # Display the score
            st.write(f"### Your Score: {user_score}/{len(correct_answers)}")

            # Visualize the score with the gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=user_score,
                number={'font': {'color': 'black', 'size': 100}},
                title={'text': "Your Score", 'font': {'size': 26, 'color': "#2b2b2b"}},
                gauge={
                    'axis': {'range': [0, len(correct_answers)], 'tickwidth': 2, 'tickcolor': "black"},
                    'bar': {'color': "rgba(0,127,255,0.8)", 'thickness': 0.3},
                    'steps': [
                        {'range': [0, len(correct_answers) // 2], 'color': "#f7d8d8"},
                        {'range': [len(correct_answers) // 2, len(correct_answers)], 'color': "#d6e5ff"}
                    ],
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("No response found for your token.")
    else:
        st.error("No responses found.")
else:
    st.error("Failed to connect to LimeSurvey API.")


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
    'Bar Chart': 1,
    'Maps': 1,
    'Line Chart': 1,
    'Pie Chart': 1,
    'Scatter Plot': 1,
    'Stacked Bar Chart': 1,
}

# Example of scores assigned to the two modules
pitfalls = {
    'Cherry Picking': 0,
    'Concealed Uncertainty': 0,
    'Inappropriate Aggregation': 1,
    'Inappropriate Scale Order': 1,
    'Inappropriate Scale Function': 0,
    'Inappropriate Scale Direction': 1,
    'Misleading Annotation': 1,
    'Missing Data': 1,
    'Missing Normalization': 1,
    'Overplotting': 1,
    'Truncated Axis': 0
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
InappropriateAggregationSubpages =  [''] * 6 + ['Module Completed']
InappropriateScaleOrderSubpages = [''] * 6 + ['Module Completed']
InappropriateScaleFunctionSubpages = [''] * 6 + ['Module Completed']
InappropriateScaleDirectionSubpages = [''] * 6 + ['Module Completed']
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
    'Inappropriate Aggregation': InappropriateAggregationSubpages,
    'Inappropriate Scale Order': InappropriateScaleOrderSubpages,
    'Inappropriate Scale Function': InappropriateScaleFunctionSubpages,
    'Inappropriate Scale Direction': InappropriateScaleDirectionSubpages,
    'Misleading Annotation': MisleadingAnnotationSubpages,
    'Missing Data': MissingDataSubpages,
    'Missing Normalization': MissingNormalizationSubpages,
    'Overplotting': OverplottingSubpages,
    'Truncated Axis': TruncatedAxisSubpages,
}


# Define the URLs of your custom icons
icon_well_done = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/Icons/NotRecommended.png"
icon_improvement = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/Icons/Recommended.png"



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
initialize_session_state(modules)

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
    'Inappropriate Aggregation': InappropriateAggregation.display_module,
    'Inappropriate Scale Order': InappropriateScaleOrder.display_module,
    'Inappropriate Scale Function': InappropriateScaleFunction.display_module,
    'Inappropriate Scale Direction': InappropriateScaleDirection.display_module,
    'Misleading Annotation': MisleadingAnnotation.display_module,
    'Missing Data': MissingData.display_module,
    'Missing Normalization': MissingNormalization.display_module,
    'Overplotting': Overplotting.display_module,
    'Truncated Axis': TruncatedAxis.display_module,
}

st.sidebar.markdown('<span id="home-button-after"></span>', unsafe_allow_html=True)
if st.sidebar.button("Home: My Scores"):
    st.session_state['selected_module'] = 'Home: My Scores'

# Sidebar Basics section
st.sidebar.subheader("Basics")
for module, score in basics.items():
    score_icon = get_score_icon(score)
    accessed_icon = '✔️' if all_subpages_accessed(module, modules) else ' '
    
    col1, col2 = st.sidebar.columns([0.6, 4])
    with col1:
        st.markdown(f'<img src="{score_icon}" width="35px">', unsafe_allow_html=True)
    with col2:
        if st.button(f"{module} {accessed_icon}", key=f"{module}_button"):
            st.session_state['selected_module'] = module

# Sidebar Common Pitfalls section
st.sidebar.subheader("Common Pitfalls")
for module, score in pitfalls.items():
    score_icon = get_score_icon(score)
    accessed_icon = '✔️' if all_subpages_accessed(module, modules) else ' '
    
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
        value=21,  # Replace with your desired score variable if needed
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
                'value': 21  # Replace with your dynamic score if needed
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

