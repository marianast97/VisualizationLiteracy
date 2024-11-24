import streamlit as st
import requests
from utils import display_subpage, initialize_single_module_state
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd



def display_module(modules):
    selected_module = 'Inappropriate Scale Direction'
    
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

    @st.cache_data
    def get_image_files():
        # GitHub API URL to list files in the folder
        api_url = "https://api.github.com/repos/marianast97/VisualizationLiteracy/contents/LearningContent/InappropriateScaleDirection"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            files = response.json()
            # Filter to get only PNG files
            image_files = [file['name'] for file in files if file['name'].endswith('.png')]
            return image_files
        else:
            st.error("Failed to load image files.")
            return []

    # Call the cached function
    image_files = get_image_files()
    num_files = len(image_files)

    # Base URL pattern
    base_url = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/main/LearningContent/InappropriateScaleDirection/InappropriateScaleDirection"

    # Pre-generate URLs for each image
    image_urls = [f"{base_url} ({i + 1}).png" for i in range(num_files)]

    # Check if the current subpage index is within the dynamic range
    if 0 <= current_subpage_index < num_files:

        st.markdown(
        """
        <div style="text-align: center; font-size: 20px; ">
            Inappropriate Scale Direction is a misleading practice where the <strong>direction</strong> of a scale is <strong>flipped</strong> to misrepresent the data.
        </div>
        """,
        unsafe_allow_html=True
        )

        # Get the pre-generated URL based on current index
        url = image_urls[current_subpage_index]
        
        # Display the image using st.markdown()
        image_markdown = f'<img src="{url}" style="width:100%;">'
        st.markdown(image_markdown, unsafe_allow_html=True)

        # Conditionally display the second text on the last and penultimate pages
        if current_subpage_index in {num_files - 1, num_files - 2}:
            st.markdown(
            """
            <div style="text-align: center; font-size: 20px; ">
                The inverted scale direction confuses viewers, suggesting incorrect trends. Always double check how the scale is presented.
            </div>
            """,
            unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="text-align: center; font-size: 20px;">
                <span style="color: white;"> Placeholder </span>
                </div>
                """,
                unsafe_allow_html=True
            )

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
""" 
    if current_subpage_index == 0:  # Assuming Bar Chart Anatomy is at index 1

        # Data for Annual Sales
        data = {
            "Year": ["2018", "2019", "2020", "2021", "2022", "2023"],
            "Test Failures": [50, 60, 55, 70, 75, 80]

        }

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Create the misleading chart with an inverted y-axis
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df["Year"],
            y=df["Test Failures"],
            mode="lines+markers",
            marker=dict(size=8),
            name="Test Failures"
        ))

        fig.update_layout(
            #title="Average Coffee Consumption in Selected Countries",
            title={
                'text': "Number of Test Failures Over Time",
                'font': {
                'size': 24  # Set title size larger
                },
                #'x': 0.5,  # Center the title
            },
            #xaxis_title="Product",
            #yaxis_title="Coffee Consumption (kg per capita)",
            xaxis={
                'tickfont': {'color': 'black', 'size': 18},  # Set axis tick labels to black with larger font
                'titlefont': {'color': 'black', 'size': 18},  # Set axis title font to black and slightly larger
            },
            yaxis=dict(
                title="Number of Test Failures",
                autorange="reversed",  # Invert the y-axis
                tickfont=dict(size=18),
                titlefont=dict(size=18)
            ),
            legend={
                'title': {
                    'font': {'color': 'black'}  # Set legend title font color to black
                }
            },
            width=800,  # Set the width of the chart
            height=500  # Set the height of the chart
        )

        # Deactivate mode bar in the plotly chart
        config = {
            'displayModeBar': False  # This will hide the toolbar
        }

        # Display the misleading figure with a unique key
        st.plotly_chart(fig, config=config, key="misleading_chart")

        # Create the misleading chart with an inverted y-axis
        fig_correct = go.Figure()

        fig_correct.add_trace(go.Scatter(
            x=df["Year"],
            y=df["Test Failures"],
            mode="lines+markers",
            marker=dict(size=8),
            name="Test Failures"
        ))

        fig_correct.update_layout(
            #title="Average Coffee Consumption in Selected Countries",
            title={
                'text': "Number of Test Failures Over Time",
                'font': {
                'size': 24  # Set title size larger
                },
                #'x': 0.5,  # Center the title
            },
            #xaxis_title="Product",
            #yaxis_title="Coffee Consumption (kg per capita)",
            xaxis={
                'tickfont': {'color': 'black', 'size': 18},  # Set axis tick labels to black with larger font
                'titlefont': {'color': 'black', 'size': 18},  # Set axis title font to black and slightly larger
            },
            yaxis=dict(
                title="Number of Test Failures",
                #autorange="reversed",  # Invert the y-axis
                tickfont=dict(size=18),
                titlefont=dict(size=18)
            ),
            legend={
                'title': {
                    'font': {'color': 'black'}  # Set legend title font color to black
                }
            },
            width=800,  # Set the width of the chart
            height=500  # Set the height of the chart
        )
        # Deactivate mode bar in the plotly chart
        config = {
            'displayModeBar': False  # This will hide the toolbar
        }

        # Display the figure in Streamlit
        st.plotly_chart(fig_correct, config=config, key="correct_chart")
 """