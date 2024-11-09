import streamlit as st
from utils import display_subpage, navigate_subpage, initialize_single_module_state
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd



def display_module(modules):
    selected_module = 'Scatter Plot'
    
    # Ensure that session state is initialized for this module
    initialize_single_module_state(selected_module, modules)

    # Get the current subpage index
    current_subpage_index = st.session_state['current_subpage'][selected_module]

    # Now display the current subpage
    display_subpage(selected_module, current_subpage_index, modules)

    # Add custom CSS to make buttons the same size and align them
    button_style = """
            <style>
            .stButton button {
                width: 100%;
            }
            </style>
        """
    st.markdown(button_style, unsafe_allow_html=True)

    # Base URL pattern
    base_url = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/AreaChart/AreaChart"

    # Check if the current subpage index is within the range you expect
    if 0 <= current_subpage_index < 13:  # Adjust the range as needed
        # Generate the URL using the current_subpage_index + 1
        url = f"{base_url}{current_subpage_index + 1:02}.png"
        
        # Display the image using st.markdown()
        image_markdown = f'<img src="{url}" style="width:100%;">'
        st.markdown(image_markdown, unsafe_allow_html=True)

    # Keep navigation buttons at the bottom
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    # Handle navigation buttons
    prev_clicked = False
    next_clicked = False

    # Conditionally render "Previous" button if not on the first subpage
    if current_subpage_index > 0:
        with col3:
            prev_clicked = st.button("Previous")

    # Conditionally render "Next" button if not on the last subpage
    if current_subpage_index < len(modules[selected_module]) - 1:
        with col4:
            next_clicked = st.button("Next")

    # Update the session state based on button clicks
    if prev_clicked:
        st.session_state['current_subpage'][selected_module] -= 1
        st.rerun()  # Immediately rerun the script to reflect the state change

    if next_clicked:
        st.session_state['current_subpage'][selected_module] += 1
        st.rerun()  # Immediately rerun the script to reflect the state change

    # Display current page number
    st.write(f"Page {current_subpage_index + 1} of {len(modules[selected_module])}")

        # Add the chart for 'Bar Chart Anatomy' subpage
    if current_subpage_index == 0:  # Assuming Bar Chart Anatomy is at index 1
        # Create the chart using Plotly

        data = {
            "University": ["Ocean State Institute", "Ocean State Institute", "Mountain Ridge College", 
                        "Ocean State Institute", "Tech Valley University", "Mountain Ridge College", 
                        "Tech Valley University", "Tech Valley University", "Mountain Ridge College", 
                        "Ocean State Institute", "Mountain Ridge College", "Tech Valley University", 
                        "Ocean State Institute", "Tech Valley University", "Mountain Ridge College"],
            "Hours of Study": [5, 8, 6, 10, 12, 9, 12, 15, 8, 6, 7, 11, 9, 13, 10],
            "Exam Score (%)": [75, 85, 78, 90, 80, 88, 95, 98, 82, 79, 85, 92, 87, 96, 89]
        }

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Create scatter plot
        fig = px.scatter(
            df,
            x="Hours of Study",
            y="Exam Score (%)",
            color="University",  # Changed to use the fictional university names
            title="Relationship Between Study Hours and Exam Scores by University",
            labels={"Hours of Study": "Hours of Study", "Exam Score (%)": "Exam Score (%)"},
            trendline="ols",  # Add a trendline (correlation line)
            trendline_scope="overall",  # Apply one trendline for the entire dataset
            trendline_color_override="black"  # Set the trendline color to black for visibility
        )

        # Customize the marker appearance (optional)
        fig.update_traces(marker=dict(size=10))  # Adjust marker size

        fig.update_layout(
            #title="Average Coffee Consumption in Selected Countries",
            title={
                #'text': "text here",
                'font': {
                'size': 24  # Set title size larger
                },
                #'x': 0.5,  # Center the title
            },
            #xaxis_title="Product",
            #yaxis_title="Coffee Consumption (kg per capita)",
            xaxis={
                'tickfont': {'color': 'black', 'size': 14},  # Set axis tick labels to black with larger font
                'titlefont': {'color': 'black', 'size': 16},  # Set axis title font to black and slightly larger
            },
            yaxis={
                'tickfont': {'color': 'black', 'size': 14},  # Set axis tick labels to black with larger font
                'titlefont': {'color': 'black', 'size': 16},  # Set axis title font to black and slightly larger
            },
            legend={
                'title': {
                    'font': {'color': 'black'}  # Set legend title font color to black
                }
            },
            width=800,  # Set the width of the chart
            height=500  # Set the height of the chart
        )

        # Update traces to increase label size
        fig.update_traces(
            textfont={
                'size': 18  # Increase the size of the labels
            }
        )
         # Deactivate mode bar in the plotly chart
        config = {
            'displayModeBar': False  # This will hide the toolbar
        }

        # Display the figure in Streamlit
        st.plotly_chart(fig, config=config)

        # Add a footnote below the chart
        st.markdown("""
        **Data source**: the author (2024). This is a fictional example created for educational purposes only. Data is fictional and should not be used for any actual analysis.
        """)