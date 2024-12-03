import streamlit as st
import requests
from utils import display_subpage, navigate_subpage, initialize_single_module_state
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd



def display_module(modules):
    selected_module = 'Missing Normalization'
    
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
        api_url = "https://api.github.com/repos/marianast97/VisualizationLiteracy/contents/LearningContent/MissingNormalization"
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
    base_url = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/main/LearningContent/MissingNormalization/MissingNormalization"

    # Pre-generate URLs for each image
    image_urls = [f"{base_url} ({i + 1}).png" for i in range(num_files)]

    # Check if the current subpage index is within the dynamic range
    if 0 <= current_subpage_index < num_files:

        st.markdown(
        """
        <div style="text-align: center; font-size: 20px; ">
            Missing normalization occurs when <strong>raw numbers</strong> are <strong>shown</strong> without considering the <strong>relative size</strong> of the compared groups.
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
                Raw numbers can be misleading when <strong>comparing countries or regions of different sizes</strong>. Always consider if the data is normalized before before drawing conclusions.
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

        # Toy Example: Total Carbon Emissions with Missing Normalization for various countries
        data_emissions = {
            "Country": ["USA", "CHN", "IND", "BRA", "RUS", "AUS", "CAN", "ZAF"],
            "Total Carbon Emissions (Million Tons)": [5000, 10000, 3000, 1200, 2000, 1500, 1400, 800]  # Raw emissions data
        }

        # Convert to DataFrame
        df_emissions = pd.DataFrame(data_emissions)

        # Create the misleading choropleth map with missing normalization
        fig_misleading_emissions = px.choropleth(
            df_emissions,
            locations="Country",
            locationmode="ISO-3",
            color="Total Carbon Emissions (Million Tons)",
            title="Carbon Emissions Data",
            color_continuous_scale=px.colors.sequential.YlOrRd,
            labels={"Total Carbon Emissions (Million Tons)": "Total Emissions (Million Tons)"}
        )

        fig_misleading_emissions.update_layout(
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
        #fig.update_traces(
        #    textfont={
        #        'size': 18  # Increase the size of the labels
        #    }
        #)

         # Deactivate mode bar in the plotly chart
        config = {
            'displayModeBar': False  # This will hide the toolbar
        }

        # Display the figure in Streamlit
        st.plotly_chart(fig_misleading_emissions, config=config)

        # Add per capita emissions to the dataset
        data_emissions_normalized = {
            "Country": ["USA", "CHN", "IND", "BRA", "RUS", "AUS", "CAN", "ZAF"],
            "Carbon Emissions per Capita (Tons)": [15, 7, 2.2, 2.5, 10, 18, 12, 9]  # Normalized data
        }

        # Convert to DataFrame
        df_emissions_normalized = pd.DataFrame(data_emissions_normalized)

        # Create the correct choropleth map with normalized data
        fig_correct_emissions = px.choropleth(
            df_emissions_normalized,
            locations="Country",
            locationmode="ISO-3",
            color="Carbon Emissions per Capita (Tons)",
            title="Carbon Emissions Data (Per Capita)",
            color_continuous_scale=px.colors.sequential.YlOrRd,
            labels={"Carbon Emissions per Capita (Tons)": "Emissions per Capita (Tons)"}
        )

        fig_correct_emissions.update_layout(
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

        # Display the correct chart
        st.plotly_chart(fig_correct_emissions, config=config)
   """