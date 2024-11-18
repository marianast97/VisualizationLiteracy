import streamlit as st
import requests
from utils import display_subpage, initialize_single_module_state
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd



def display_module(modules):
    selected_module = 'Misleading Annotation'
    
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
        api_url = "https://api.github.com/repos/marianast97/VisualizationLiteracy/contents/LearningContent/MisleadingAnnotation"
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
    base_url = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/main/LearningContent/MisleadingAnnotation/MisleadingAnnotation"

    # Pre-generate URLs for each image
    image_urls = [f"{base_url} ({i + 1}).png" for i in range(num_files)]

    # Check if the current subpage index is within the dynamic range
    if 0 <= current_subpage_index < num_files:

        st.markdown(
        """
        <div style="text-align: center; font-size: 20px; ">
            Misleading annotations occur when <strong>labels</strong> or <strong>annotations</strong> in a chart are <strong>incorrect</strong> or <strong>misleading</strong>, leading viewers to misinterpret the data.
        </div>
        """,
        unsafe_allow_html=True
        )

        # Get the pre-generated URL based on current index
        url = image_urls[current_subpage_index]
        
        # Display the image using st.markdown()
        image_markdown = f'<img src="{url}" style="width:100%;">'
        st.markdown(image_markdown, unsafe_allow_html=True)

        st.markdown(
        """
        <div style="text-align: center; font-size: 20px; ">
            Misleading annotations can distort data interpretation. Always ensure that annotations correctly reflect the actual data.
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

        # Add the chart for 'Bar Chart Anatomy' subpage
    if current_subpage_index == 0:  # Assuming Bar Chart Anatomy is at index 1
        
        # Toy Example: Misleading chart showing Transportation Preferences with incorrect annotation
        data_transportation = {
            "Mode of Transportation": ["Driving", "Public Transportation"],
            "Percentage": [60, 40],
            "Wrong": [40, 60]  # Incorrect values to mislead
        }

        # Convert to DataFrame
        df_transportation = pd.DataFrame(data_transportation)

        # Create the misleading pie chart
        fig_misleading_transport = px.pie(
            df_transportation,
            names="Mode of Transportation",
            values="Percentage",
            title="Transportation Preferences"
        )

        # Add wrong label using hovertemplate and texttemplate for misleading information
        fig_misleading_transport.update_traces(
            hovertemplate="<b>%{label}</b><br>Actual Value: %{value}<br>Wrong Value: %{customdata[0]}%",
            customdata=df_transportation[['Wrong']],  # Use the 'Wrong' column for hover
            texttemplate="%{customdata[0]}%",  # Show wrong values directly on the chart
            textposition="inside",  # Position text inside the pie slices
            showlegend=True,  # Ensure legend is displayed
            textfont=dict(size=18)  # Increase text size to 16
        )


        fig_misleading_transport.update_layout(
            title={
                'font': {
                'size': 24  # Set title size larger
                },
            },
            xaxis={
                'tickfont': {'color': 'black', 'size': 18},  # Set axis tick labels to black with larger font
                'titlefont': {'color': 'black', 'size': 18},  # Set axis title font to black and slightly larger
            },
            yaxis={
                'tickfont': {'color': 'black', 'size': 18},  # Set axis tick labels to black with larger font
                'titlefont': {'color': 'black', 'size': 18},  # Set axis title font to black and slightly larger
            },
            legend={
                'title': {
                    'font': {'color': 'black'}  # Set legend title font color to black
                }
            },
            width=400,  # Set the width of the chart
            height=500  # Set the height of the chart
        )
         # Deactivate mode bar in the plotly chart
        config = {
            'displayModeBar': False  # This will hide the toolbar
        }

        # Display the figure in Streamlit
        st.plotly_chart(fig_misleading_transport, config=config)

        # Add wrong label using hovertemplate and texttemplate for misleading information
        fig_misleading_transport.update_traces(
            hovertemplate="<b>%{label}</b><br>Actual Value: %{value}<br>Wrong Value: %{customdata[0]}%",
            customdata=df_transportation[['Percentage']],  # Use the 'Wrong' column for hover
            texttemplate="%{customdata[0]}%",  # Show wrong values directly on the chart
            textposition="inside",  # Position text inside the pie slices
            showlegend=True,  # Ensure legend is displayed
            textfont=dict(size=18)  # Increase text size to 16
        )

        # Display the figure in Streamlit
        st.plotly_chart(fig_misleading_transport, config=config)

