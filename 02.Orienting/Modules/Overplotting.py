import streamlit as st
import requests
from utils import display_subpage, initialize_single_module_state
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np



def display_module(modules):
    selected_module = 'Overplotting'
    
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
        api_url = "https://api.github.com/repos/marianast97/VisualizationLiteracy/contents/02.Orienting/LearningContent/Overplotting"
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

    # Define base URL to fetch files from GitHub
    base_url = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/main/02.Orienting/LearningContent/Overplotting/Overplotting"

    # Pre-generate URLs for each image
    image_urls = [f"{base_url} ({i + 1}).png" for i in range(num_files)]

    # Check if the current subpage index is within the dynamic range
    if 0 <= current_subpage_index < num_files:

        st.markdown(
        """
        <div style="text-align: center; font-size: 20px; ">
            Overplotting occurs when <strong>too many data points</strong> are plotted on a chart, making it difficult to distinguish between values or detect meaningful patterns. 
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
                Overplotting hides meaningful insights in large datasets. When faced with a dense visualisation where data points overlap, be careful not to fall into misinterpretation.
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

"""         # Add the chart for 'Bar Chart Anatomy' subpage
    if current_subpage_index == 0:  # Assuming Bar Chart Anatomy is at index 1
        # Create the chart using Plotly

        # Creating a new toy example dataset: Hours Studied vs Exam Scores
        np.random.seed(42)
        hours_studied = np.random.normal(loc=4, scale=1, size=150)  # Hours studied per day
        exam_scores = 50 + 10 * hours_studied + np.random.normal(loc=0, scale=5, size=150)  # Exam scores with noise

        # Clip the data to keep it realistic
        hours_studied = np.clip(hours_studied, 1, 7)
        exam_scores = np.clip(exam_scores, 50, 100)

        # Create DataFrame for the new example
        data_new = {
            "Hours Studied": hours_studied,
            "Exam Scores": exam_scores
        }
        df_new = pd.DataFrame(data_new)

        # Create the scatter plot for the new example
        fig_new = px.scatter(
            df_new,
            x="Hours Studied",
            y="Exam Scores",
            title="Relationship Between Hours Studied and Exam Scores",
            labels={"Hours Studied": "Hours Studied (per day)", "Exam Scores": "Exam Scores (%)"},
            #opacity=0.7
        )

        # Increase the size of the data points
        fig_new.update_traces(marker=dict(size=20))  # Set marker size to 12

        fig_new.update_layout(
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
        fig_new.update_traces(
            textfont={
                'size': 18  # Increase the size of the labels
            }
        )
         # Deactivate mode bar in the plotly chart
        config = {
            'displayModeBar': False  # This will hide the toolbar
        }

        # Display the figure in Streamlit
        st.plotly_chart(fig_new, config=config)

        # Create the scatter plot for the new example
        fig_better = px.scatter(
            df_new,
            x="Hours Studied",
            y="Exam Scores",
            title="Relationship Between Hours Studied and Exam Scores",
            labels={"Hours Studied": "Hours Studied (per day)", "Exam Scores": "Exam Scores (%)"},
            opacity=0.5
        )
        # Increase the size of the data points
        fig_better.update_traces(marker=dict(size=12))  # Set marker size to 12

        fig_better.update_layout(
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
        fig_better.update_traces(
            textfont={
                'size': 13  # Increase the size of the labels
            }
        )
         # Deactivate mode bar in the plotly chart
        config = {
            'displayModeBar': False  # This will hide the toolbar
        }

        # Display the figure in Streamlit
        st.plotly_chart(fig_better, config=config)

 """

  