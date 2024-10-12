import streamlit as st
from utils import get_score_icon, all_subpages_accessed, initialize_session_state
import module_advanced_visualizations
import module_basic_charts
import plotly.graph_objects as go

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
    st.session_state['selected_module'] = 'Home'

# Home button in the sidebar (without any title)
if st.sidebar.button("My Scores"):
    st.session_state['selected_module'] = 'Home'

# Display buttons for each module in the sidebar
for module, score in pages.items():
    # Icon for good/bad score
    score_icon = get_score_icon(score)
    
    # Check if all subpages are accessed
    if all_subpages_accessed(module, modules):
        accessed_icon = '✔️'
    else:
        accessed_icon = '  '

    # Create button for each module (without scores in the label, only icons and names)
    if st.sidebar.button(f"{score_icon} {module} {accessed_icon}"):
        st.session_state['selected_module'] = module

# Display content based on selection
selected_module = st.session_state['selected_module']

if selected_module == 'Home':
    st.write("### Visualization Literacy")
    #st.write("Here is an overview of your scores across all modules:")

    # Loop over the pages to show scores
    #for module, score in pages.items():
    #    st.write(f"- **{module}**: {score}/100")
    
    # Add the Plotly gauge chart for one of the scores (make the chart smaller)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=21,  # Replace with your desired score variable if needed
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "My Scores", 'font': {'size': 24, 'color': "#4a4a4a"}},
        gauge={
            'axis': {'range': [0, 30], 'tickwidth': 2, 'tickcolor': "#4a4a4a"},
            'bar': {'color': "#007FFF"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#cccccc",
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': 21  # Replace with your dynamic score if needed
            }
        }
    ))

    # Set the layout to make the gauge chart smaller
    fig.update_layout(
        #width=300,  # Set width
        height=300  # Set height
    )

    # Display the gauge chart inside the centered container
    st.plotly_chart(fig)

    # Add the message with styled text and emoji below the gauge chart
    st.markdown("""
        ### Keep Learning!
        To get further insights into Visualization Literacy and improve your scores, check out the content by navigating through the menu on the left.
        
        **Legend:**
        
        - <span style="color:black">🟢 Well done! You seem to master this topic 🏆</span>
        - <span style="color:black">❌ There is some room for improvement here 🎯</span>
    """, unsafe_allow_html=True)

elif selected_module == 'Advanced Visualizations':
    module_advanced_visualizations.display_module(modules)
elif selected_module == 'Basic Charts':
    module_basic_charts.display_module(modules)
