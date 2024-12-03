import streamlit as st
import requests
from utils import display_subpage, initialize_single_module_state, get_image_files, get_base_url
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd



def display_module(modules):
    selected_module = 'Maps'
    
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
        # Get the pre-generated URL based on current index
        url = image_urls[current_subpage_index]
        
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

"""         # Add the chart for 'Bar Chart Anatomy' subpage
    if current_subpage_index == 0:  # Assuming Bar Chart Anatomy is at index 1
        # Create the chart using Plotly

        data = {
            "State": ["AL", "MS", "LA", "AR", "TN", "GA", "FL", "SC", "NC", "VA", "KY", "WV", "TX", "MO", "OK", "KS", "CO", 
                    "UT", "NM", "AZ", "NV", "CA", "OR", "WA", "ID", "MT", "WY", "ND", "SD", "NE", "IA", "MN", "WI", "MI", 
                    "IL", "IN", "OH", "PA", "ME", "NJ", "MA", "CT", "VT", "NH", "RI", "NY", "MD", "DE"],
            # Randomly distribute values across 3 bins: 40-50%, 20-39%, and 0-19%
            "Percentage": [48, 25, 38, 43, 43, 23, 26, 30, 37, 25, 50, 38, 26, 45, 
                        45, 39, 42, 32, 28, 33, 32, 37, 28, 44, 34, 40, 32, 12, 
                        44, 49, 12, 13, 18, 30, 39, 29, 41, 13, 36, 37, 45, 43, 42, 33, 41, 25, 14, 15]
        }

        # Ensure both lists have the same length
        assert len(data['State']) == len(data['Percentage']), "State and Percentage arrays must be of the same length"

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Handle NaN values by ensuring that all percentages fit in defined bins
        df['Percentage'] = df['Percentage'].clip(upper=50)

        # Create bins for the percentage ranges (3 bins)
        bins = [9, 19, 39, 50]
        labels = ["40 - 50%", "20 - 39%", "10 - 19%"]
        df['Percentage Range'] = pd.cut(df['Percentage'], bins=bins, labels=labels, include_lowest=True)

        # Create the choropleth map with the new green palette
        fig = px.choropleth(
            df,
            locations="State",
            locationmode="USA-states",
            color="Percentage Range",  # Use the binned percentage ranges
            scope="usa",
            title="Renewable Energy Adoption by State",
            category_orders={"Percentage Range": labels},  # Sort legend from bottom to top
            #color_discrete_map={
            #    "10 - 19%": "#D9F0A3",  # Very light green
            #    "20 - 39%": "#41AB5D",  # Darker medium green
            #    "40 - 50%": "#005A32"  # Very dark green
            #},
            labels={"Percentage Range": "Renewable Energy (%)"}
        )

        # Add state labels using Scattergeo
        fig.add_trace(go.Scattergeo(
            locationmode='USA-states',
            locations=df['State'],
            text=df['State'],  # Use state abbreviations as labels
            mode='text',
            textfont=dict(size=12, color="black"),  # Customize font size and color
            showlegend=False  # Do not show in legend
        ))


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
        st.plotly_chart(fig, config=config)

 """      