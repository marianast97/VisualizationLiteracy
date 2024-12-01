import streamlit as st
import requests
from utils import display_subpage, navigate_subpage, initialize_single_module_state
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from pycountry import countries




def display_module(modules):
    selected_module = 'Missing Data'
    
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
        api_url = "https://api.github.com/repos/marianast97/VisualizationLiteracy/contents/02.Orienting/LearningContent/MissingData"
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
    base_url = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/main/02.Orienting/LearningContent/MissingData/MissingData"

    # Pre-generate URLs for each image
    image_urls = [f"{base_url} ({i + 1}).png" for i in range(num_files)]

    # Check if the current subpage index is within the dynamic range
    if 0 <= current_subpage_index < num_files:

        st.markdown(
        """
        <div style="text-align: center; font-size: 20px; ">
            Missing data refers to when <strong>important information</strong> is <strong>absent</strong> from a chart, making it impossible to draw accurate conclusions. 
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
                Missing data can lead to incorrect conclusions, whether intentionally or not. Always consider whether data is complete before drawing conclusions.
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

        # Toy Example: Percentage of Renewable Energy Usage with missing data for some countries
        data_energy = {
            "Country": [
                "USA", "CAN", "BRA", "IND", "AUS", "ZAF", "RUS", "CHN", 
                "GER", "FRA", "JPN", "MEX", "ITA", "ESP", "KOR", "ARG", 
                "SAU", "UK", "IDN", "NGA", "PAK", "EGY", "TUR", "IRN"
            ],
            "Renewable Energy Usage (%)": [
                15, 25, 40, None, 10, 5, None, 20, 
                45, 50, 25, 18, 35, 40, 30, 22, 
                None, 50, 12, 7, 8, 3, 27, 6  # Some countries have missing data (None)
            ]
        }

        # Convert to DataFrame
        df_energy = pd.DataFrame(data_energy)

        # Create the choropleth map with missing data
        fig_misleading_energy = px.choropleth(
            df_energy,
            locations="Country",
            locationmode="ISO-3",
            color="Renewable Energy Usage (%)",
            title="Renewable Energy Usage",
            color_continuous_scale=px.colors.sequential.Blues,
            labels={"Renewable Energy Usage (%)": "Renewable Energy (%)"}
        )


        fig_misleading_energy.update_layout(
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


         # Deactivate mode bar in the plotly chart
        config = {
            'displayModeBar': False  # This will hide the toolbar
        }

        # Display the figure in Streamlit
        st.plotly_chart(fig_misleading_energy, config=config)

        # Updated data with missing values
        data_energy = {
            "Country": [
                "USA", "CAN", "BRA", "IND", "AUS", "ZAF", "RUS", "CHN", 
                "GER", "FRA", "JPN", "MEX", "ITA", "ESP", "KOR", "ARG", 
                "SAU", "UK", "IDN", "NGA", "PAK", "EGY", "TUR", "IRN"
            ],
            "Renewable Energy Usage (%)": [
                15, 25, 40, None, 10, 5, None, 20, 
                45, 50, 25, 18, 35, 40, 30, 22, 
                None, 50, 12, 7, 8, 3, 27, 6
            ]
        }

        # Convert to DataFrame
        df_energy = pd.DataFrame(data_energy)

        # Fill missing values with a placeholder (-1)
        df_energy["Renewable Energy Usage (%)"] = df_energy["Renewable Energy Usage (%)"].fillna(-1)

        all_countries = [country.alpha_3 for country in countries]

        # Add missing countries to the dataset and mark them with -1
        existing_countries = df_energy["Country"].tolist()
        missing_countries = [country for country in all_countries if country not in existing_countries]

        # Append missing countries to the DataFrame with placeholder data
        missing_data = pd.DataFrame({
            "Country": missing_countries,
            "Renewable Energy Usage (%)": -1
        })
        df_energy = pd.concat([df_energy, missing_data], ignore_index=True)

        # Define a custom color scale
        color_scale = [
            (0.0, "LightGray"),  # Map missing data (-1) to gray
            (0.00001, "yellow"),  # Transition color for valid data
            (1.0, "red")       # Scale up to red for higher values
        ]

        # Create the choropleth map with the custom color scale
        fig_correct_energy_discrete = px.choropleth(
            df_energy,
            locations="Country",
            locationmode="ISO-3",
            color="Renewable Energy Usage (%)",
            title="Renewable Energy Usage",
            color_continuous_scale=color_scale,
            range_color=(-1, 50),  # Ensure -1 (missing data) is included in the range
            labels={"Renewable Energy Usage (%)": "Renewable Energy (%)"}
        )

        # Add annotation indicating missing data
        fig_correct_energy_discrete.add_annotation(
            x=0.5, y=-0.1, text="Gray regions indicate missing data", showarrow=False,
            font=dict(size=14, color="black"), xref="paper", yref="paper"
        )

        fig_correct_energy_discrete.update_layout(
            title={
                'font': {'size': 24}
            },
            legend={
                'title': {
                    'font': {'color': 'black'}
                }
            },
            width=800,
            height=500
        )

        # Display the figure in Streamlit
        st.plotly_chart(fig_correct_energy_discrete, config={"displayModeBar": False})
 """