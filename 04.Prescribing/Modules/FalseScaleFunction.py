import streamlit as st
import requests
from utils import display_subpage, initialize_single_module_state, get_image_files, get_base_url
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd



def display_module(modules):
    selected_module = 'False Scale Function'
    
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

    # Specify chart type
    chart_type = selected_module.replace(" ","")

    # Get image files and base URL
    image_files = get_image_files(chart_type)
    num_files = len(image_files)
    base_url = get_base_url(chart_type)

    # Pre-generate URLs for each image
    image_urls = [f"{base_url} ({i + 1}).png" for i in range(num_files)]

    # Check if the current subpage index is within the dynamic range
    if 0 <= current_subpage_index < num_files:
        
        # Conditionally display the second text on the last and penultimate pages
        if current_subpage_index in {num_files - 1, num_files - 2}:

            st.markdown(
            """
            <div style="text-align: center; font-size: 20px; ">
                An inappropriate scale function occurs when the intervals on an axis are <strong>not uniform</strong>, distorting the visual representation of data. 
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
                Inappropriate scale function can mislead viewers by exaggerating or minimizing differences. Ensure that axes have consistent intervals to avoid visual distortions.
            </div>
            """,
            unsafe_allow_html=True
            )
        else:
            st.markdown(
            """
            <div style="text-align: center; font-size: 20px; ">
                An inappropriate scale function occurs when the intervals on an axis are <strong>not uniform</strong>, distorting the visual representation of data. 
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
        
        # Data for the example
        data = {
            "Product": ["Product A", "Product B"],
            "Sales": [250, 500]
        }

        # Misleading Chart: Non-linear y-axis scaling
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=data["Product"],
            y=data["Sales"],
            #text=data["Sales"],
            #textposition="outside"
        ))
 
        fig.update_layout(
            #title="Average Coffee Consumption in Selected Countries",
            title={
                'text': "Sales Comparison for Two Products",
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
                'title': "Sales (in units)",  # Set the y-axis title
                'tickvals': [0, 250, 500],  # Tick values
                'ticktext': ["0", "250", "750"],  # Tick text for non-linear scaling
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

        # Data for the example
        data = {
            "Product": ["Product A", "Product B"],
            "Sales": [250, 750]
        }

        # Misleading Chart: Non-linear y-axis scaling
        fig_correct = go.Figure()

        fig_correct.add_trace(go.Bar(
            x=data["Product"],
            y=data["Sales"],
            #text=data["Sales"],
            #textposition="outside"
        ))
 
        fig_correct.update_layout(
            #title="Average Coffee Consumption in Selected Countries",
            title={
                'text': "Sales Comparison for Two Products",
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
                'title': "Sales (in units)",  # Set the y-axis title
                'tickvals': [0, 250, 500, 750],  # Tick values
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
        st.plotly_chart(fig_correct, config=config)
 """