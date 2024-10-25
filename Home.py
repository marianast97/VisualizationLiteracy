import streamlit as st
from utils import get_score_icon, all_subpages_accessed, initialize_session_state
import module_advanced_visualizations
import BarChart
import plotly.graph_objects as go

st.set_page_config(layout="wide") #"centered"


# Example of scores assigned to the two modules
pages = {
    'Advanced Visualizations': 1,
    'Basics: Bar Chart': 0
}

modules = {
    'Advanced Visualizations': ['Overview', 'Techniques', 'Examples'],
    'Basics: Bar Chart': ['Anatomy', 'Common Tasks associated to Bar Chart', 'Common Tasks associated to Bar Chart']
}

# Define the URLs of your custom icons
icon_well_done = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/IconRight2.png"
icon_improvement = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/IconWrong2.png"

# Add custom CSS to make buttons the same size and align them
sidebar_style = """
    <style>
    .stButton button {
        width: 100%;
    }
    .sidebar-link {
        display: block;
        width: 100%;
        padding: 10px;
        margin: 5px 0;
        text-align: center;
        border-radius: 5px;
        text-decoration: none;
        color: black;
    }
    </style>
    """
st.markdown(sidebar_style, unsafe_allow_html=True) #        font-weight: bold;

# Add custom CSS to target a specific button using a span element
st.markdown("""
    <style>
    .element-container:has(#home-button-after) + div button {
        background-color: #f0f2f6;
        color: #0068c9;
        border-radius: 5px;
        font-weight: bold;
        width: 100%;
        margin: 5px 0;
        padding: 10px;
        border: 2px solid #f0f2f6;
    }
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


st.sidebar.markdown('<span id="home-button-after"></span>', unsafe_allow_html=True)
if st.sidebar.button("Home: My Scores"):
    st.session_state['selected_module'] = 'Home: My Scores'

st.sidebar.subheader("Learning Content")

# Display buttons for each module in the sidebar
for module, score in pages.items():
    # Icon for good/bad score
    score_icon = get_score_icon(score)
    
    # Check if all subpages are accessed
    if all_subpages_accessed(module, modules):
        accessed_icon = '✔️'
    else:
        accessed_icon = '  '

    # Use columns to align the icon and the button
    col1, col2 = st.sidebar.columns([0.6, 4])  # Adjust column proportions as needed
    
    # Display the icon in the first column using markdown
    with col1:
        icon_markdown = f'<img src="{score_icon}" alt="icon" width="35px">'  # Adjust width as needed
        st.markdown(icon_markdown, unsafe_allow_html=True)

    # Display the button in the second column
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
                {'range': [10, 20], 'color': "#99c2ff"},  # Medium blue
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

elif selected_module == 'Advanced Visualizations':
    module_advanced_visualizations.display_module(modules)
elif selected_module == 'Basics: Bar Chart':
    BarChart.display_module(modules)


st.sidebar.subheader("", divider="red")

# Example of adding a link to the sidebar
st.sidebar.markdown("When you are confident that you have learnt enough, click on the link below to proceed to the final assessment:", unsafe_allow_html=True)

#st.sidebar.markdown("[When you feel like you're ready, click here for the Final Assessment](https://example.com/final-assessment)", unsafe_allow_html=True)

# Add the Final Assessment link at the bottom of the sidebar
final_assessment_link = """
<a href="https://example.com/final-assessment" target="_blank" class="sidebar-link">
    Final Assessment
</a>
"""

st.sidebar.markdown(final_assessment_link, unsafe_allow_html=True)

