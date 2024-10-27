import streamlit as st
from utils import display_subpage, navigate_subpage, initialize_single_module_state
import plotly.graph_objects as go
import plotly.express as px



#modules = {
#    'Basics: Bar Chart': ['Chart Anatomy', 'Common Tasks associated to Bar Chart', 'Common Tasks associated to Bar Chart']
#}



def display_module(modules):
    selected_module = 'Basics: Bar Chart'
    
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

    # Add the chart for 'Bar Chart Anatomy' subpage
    if current_subpage_index == 0:  # Assuming Bar Chart Anatomy is at index 1
        # Create the bar chart using Plotly
        fig = go.Figure(data=[
            go.Bar(name='Coffee Consumption', x=['USA', 'Canada', 'Mexico', 'Brazil', 'Argentina', 'UK', 'France', 
                                                 'Germany', 'Italy', 'Spain', 'China', 'India', 'Russia', 
                                                 'Japan', 'South Korea'],
                   y=[9.5, 6.0, 4.0, 5.5, 3.5, 7.0, 8.0, 7.5, 6.5, 4.5, 2.0, 3.0, 5.5, 7.5, 6.0],
                   hoverinfo='none'  # This disables the tooltip
                   )
        ])
        fig.update_layout(
            #title="Average Coffee Consumption in Selected Countries",
            title={
                'text': "Average Coffee Consumption in Selected Countries",
                'font': {
                'size': 24  # Set title size larger
                },
                #'x': 0.5,  # Center the title
            },
            xaxis_title="Country",
            yaxis_title="Coffee Consumption (kg per capita)",
            xaxis={
                'tickfont': {'color': 'black', 'size': 14},  # Set axis tick labels to black with larger font
                'titlefont': {'color': 'black', 'size': 16},  # Set axis title font to black and slightly larger
            },
            yaxis={
                'tickfont': {'color': 'black', 'size': 14},  # Set axis tick labels to black with larger font
                'titlefont': {'color': 'black', 'size': 16},  # Set axis title font to black and slightly larger
            },
            width=800,  # Set the width of the chart
            height=500  # Set the height of the chart
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


    # Add the chart for 'Bar Chart Anatomy' subpage
    if current_subpage_index == 0:  # Assuming Bar Chart Anatomy is at index 1

        # URL of the image
        url = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/test6-min.png"

        # Display the image using st.markdown()
        image_markdown = f'<img src="{url}" style="width:100%;">'
        st.markdown(image_markdown, unsafe_allow_html=True)


    # Add the chart for 'Bar Chart Anatomy' subpage
    if current_subpage_index == 1:  # Assuming Bar Chart Anatomy is at index 1

        # URL of the image
        url = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/test6-min.png"
        #url = "test6.png"


        # Display the image using st.markdown()
        # st.image(url, output_format="PNG", use_column_width=True) 
        image_markdown = f'<img src="{url}" style="width:100%;">'
        st.markdown(image_markdown, unsafe_allow_html=True)



    # Add the chart for 'Bar Chart Anatomy' subpage
    if current_subpage_index == 2:  # Assuming Bar Chart Anatomy is at index 1

        # URL of the image
        url = "https://raw.githubusercontent.com/marianast97/VisualizationLiteracy/refs/heads/main/test6-min.png"
        #url = "test6.png"


        # Display the image using st.markdown()
        # st.image(url, output_format="PNG", use_column_width=True) 
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