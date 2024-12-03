import streamlit as st
import requests
from utils import display_subpage, initialize_single_module_state
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd



def display_module(modules):
    selected_module = 'Inappropriate Aggregation'
    
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
        api_url = "https://api.github.com/repos/marianast97/VisualizationLiteracy/contents/02.Orienting/LearningContent/InappropriateAggregation"
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
    base_url = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/main/02.Orienting/LearningContent/InappropriateAggregation/InappropriateAggregation"

    # Pre-generate URLs for each image
    image_urls = [f"{base_url} ({i + 1}).png" for i in range(num_files)]

    # Check if the current subpage index is within the dynamic range
    if 0 <= current_subpage_index < num_files:

        st.markdown(
        """
        <div style="text-align: center; font-size: 20px; ">
            Inappropriate aggregation occurs when <strong>data is combined</strong> in a way that <strong>hides important patterns or details</strong>, leading to misleading conclusions.
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
                Inappropriate aggregation misleads by ignoring key data or context. Check if the dataset is complete and comparable across different time periods.
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
        
        # Toy Example: Wrong Deliveries - Misleading chart with partial data for 2022
        data = {
            "Year": ["2021", "2022", "2023", "2024"],
            "Wrong Deliveries": [300, 276, 288, 66]  # 2022 data is incomplete (only 5 months)
        }

        # Convert to DataFrame
        df_data = pd.DataFrame(data)
        
        # Create the misleading bar chart
        fig = px.bar(
            df_data,
            x="Year",
            y="Wrong Deliveries",
            title="Wrong Deliveries",
            labels={"Wrong Deliveries": "Number of Wrong Deliveries", "Year": "Year"}
        )
 
        fig.update_layout(
            #title="Average Coffee Consumption in Selected Countries",
            title={
                #'text': "Average Coffee Consumption in Selected Countries",
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
            width=400,  # Set the width of the chart
            height=500  # Set the height of the chart
        )
         # Deactivate mode bar in the plotly chart
        config = {
            'displayModeBar': False  # This will hide the toolbar
        }

        # Display the figure in Streamlit
        st.plotly_chart(fig, config=config)

        # Create a dataset showing the average number of wrong deliveries per month for each year
        data_avg = {
            "Year": ["2021", "2022", "2023", "2024"],
            "Wrong Deliveries (Avg per Month)": [300/12, 276/12, 288/12, 66/3]  # Average for 2022 based on 5 months
        }

        # Convert to DataFrame
        df_avg = pd.DataFrame(data_avg)

        # Create the correct bar chart
        fig_correct = px.bar(
            df_avg,
            x="Year",
            y="Wrong Deliveries (Avg per Month)",
            title="Average Wrong Deliveries per Month",
            labels={"Wrong Deliveries (Avg per Month)": "Average Wrong Deliveries per Month", "Year": "Year"}
        )


        fig_correct.update_layout(
            #title="Average Coffee Consumption in Selected Countries",
            title={
                #'text': "Average Coffee Consumption in Selected Countries",
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
            width=400,  # Set the width of the chart
            height=500  # Set the height of the chart
        )


        # Add annotation for 2024 data
        fig_correct.add_annotation(
            x="2024",
            y=df_avg.loc[df_avg['Year'] == "2024", "Wrong Deliveries (Avg per Month)"].values[0],
            text="Partial data (3 months only)",
            showarrow=True,
            arrowhead=1,
            ax=0,
            ay=-40,  # Adjust the position of the annotation arrow as needed
            font=dict(size=14, color="black"),  # Customize font size and color for visibility
        )
         # Deactivate mode bar in the plotly chart
        config = {
            'displayModeBar': False  # This will hide the toolbar
        }

        # Display the figure in Streamlit
        st.plotly_chart(fig_correct, config=config)
 """