import streamlit as st
import requests
from utils import display_subpage, initialize_single_module_state
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd



def display_module(modules):
    selected_module = 'Cherry Picking'
    
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
        api_url = "https://api.github.com/repos/marianast97/VisualizationLiteracy/contents/LearningContent/CherryPicking"
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
    base_url = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/LearningContent/CherryPicking/CherryPicking"

    # Pre-generate URLs for each image
    image_urls = [f"{base_url} ({i + 1}).png" for i in range(num_files)]

    # Check if the current subpage index is within the dynamic range
    if 0 <= current_subpage_index < num_files:

        st.markdown(
        """
        <div style="text-align: center; font-size: 20px; ">
            The term "cherry-picking" refers to <strong>presenting only the best data</strong> and <strong>omitting</strong> less favorable data points to support a particular narrative.
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
                <div style="text-align: center; font-size: 20px;">
                    Cherry-picking selects specific data to tell a misleading story. Always think critically about the visualization to avoid falling into this type of manipulation.
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

    if current_subpage_index == 0:  # Assuming Bar Chart Anatomy is at index 1
        # Create the chart using Plotly

        # Full data for the past 3 years with fluctuating unemployment rate, but increasing overall (except the last 5 months)
        full_data = {
            "Month": [
                "Jan 2023", "Feb 2023", "Mar 2023", "Apr 2023", "May 2023", "Jun 2023", "Jul 2023", "Aug 2023", "Sep 2023", "Oct 2023", "Nov 2023", "Dec 2023",
                "Jan 2024", "Feb 2024", "Mar 2024", "Apr 2024", "May 2024", "Jun 2024", "Jul 2024", "Aug 2024"
            ],
            # Unemployment rate fluctuating but increasing overall except last 5 months
            "Unemployment Rate (%)": [
                5.3, 5.5, 5.4, 5.6, 5.8, 5.7, 5.9, 6.0, 6.1, 6.0, 6.2, 6.3,  # 2022
                6.4, 6.3, 6.1, 6.4, 6.37, 6.28, 6.25, 6.2                # 2023
            ]
        }

        # Convert to DataFrame
        df_full = pd.DataFrame(full_data)

        # Creating the line chart using Plotly Express
        fig = px.line(
            df_full, 
            x="Month",
            y="Unemployment Rate (%)",
            title="Unemployment Rate Trend",
            labels={"Unemployment Rate (%)": "Unemployment Rate (%)", "Month": "Month"},
            markers=True
        )

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

        # Filter the DataFrame to show only May 2024 to August 2024
        df_filtered = df_full[df_full['Month'].isin(["May 2024", "Jun 2024", "Jul 2024", "Aug 2024"])]

        # Creating the line chart using Plotly Express
        fig_filtered = px.line(
            df_filtered, 
            x="Month",
            y="Unemployment Rate (%)",
            title="Unemployment Rate Trend",
            labels={"Unemployment Rate (%)": "Unemployment Rate (%)", "Month": "Month"},
            markers=True
        )

        fig_filtered.update_layout(
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
            width=800,  # Set the width of the chart
            height=500  # Set the height of the chart
        )

        # Update traces to increase label size
        fig_filtered.update_traces(
            textfont={
                'size': 18  # Increase the size of the labels
            }
        )
         # Deactivate mode bar in the plotly chart
        config = {
            'displayModeBar': False  # This will hide the toolbar
        }

        # Display the figure in Streamlit
        st.plotly_chart(fig_filtered, config=config)

        # Add a footnote below the chart
        st.markdown("""
        **Data source**: the author (2024). This is a fictional example created for educational purposes only. Data is fictional and should not be used for any actual analysis.
        """)