import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from openpyxl import load_workbook

# Initialize session state
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None

# Define the main categories and subcategories
categories = {
    "Digital Marketing": ["Blogs", "SEO", "Social Media", "Email Marketing", "Content Marketing"],
    "Traditional Marketing": ["Print Ads", "Billboards", "Flyers", "Brochures", "Direct Mail"],
    "Content Assets": ["Ebooks", "White Papers", "Case Studies", "Infographics", "Videos"],
    "Public Relations": ["Press Releases", "Media Relations", "Events", "Speaking Engagements"],
    "Audio Marketing": ["Podcasts", "Radio Ads", "Voice Marketing", "Audio Books"],
    "Visual Marketing": ["Photography", "Graphics", "Animation", "Video Production"],
    "Website & Tech": ["Website Design", "Landing Pages", "Mobile Apps", "Web Analytics"],
    "Advertising": ["PPC", "Display Ads", "Native Ads", "Social Media Ads"]
}

# Priority color mapping
priority_colors = {"High": "red", "Medium": "orange", "Low": "green"}

# Load preferences from Excel
def load_preferences():
    try:
        df = pd.read_excel("data/user_preferences.xlsx", sheet_name="Preferences")
        return df
    except FileNotFoundError:
        st.error("Preferences file not found. Please ensure `data/user_preferences.xlsx` exists.")
        return pd.DataFrame(columns=["Category", "Priority"])

# Save preferences to Excel
def save_preferences(df):
    with pd.ExcelWriter("data/user_preferences.xlsx", engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Preferences")

# Create a 3D pie chart for main categories
def create_main_pie_chart(categories):
    labels = list(categories.keys())
    values = [len(subcats) for subcats in categories.values()]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        textinfo='label+percent',
        insidetextorientation='radial',
        marker=dict(colors=['blue', 'purple', 'cyan', 'magenta', 'lime', 'gold', 'teal', 'coral'])
    )])
    fig.update_layout(title="3D Pie Chart of Main Categories", template="plotly_dark")
    return fig

# Create a 3D pie chart for subcategories
def create_subcategory_pie_chart(selected_category, categories):
    subcategories = categories[selected_category]
    values = [1] * len(subcategories)  # Equal distribution for simplicity

    fig = go.Figure(data=[go.Pie(
        labels=subcategories,
        values=values,
        hole=0.3,
        textinfo='label+percent',
        insidetextorientation='radial',
        marker=dict(colors=['lightblue', 'lightgreen', 'lightpink', 'lightyellow', 'lavender'])
    )])
    fig.update_layout(title=f"Subcategories of {selected_category}", template="plotly_dark")
    return fig

# Display the main pie chart
st.title("🌟 Dynamic Marketing Wheel with Interactive Pie Charts 🌟")
st.subheader("📊 3D Pie Chart of Main Categories")

# Create the main pie chart
fig_main_pie = create_main_pie_chart(categories)

# Add click event to the main pie chart
event = st.plotly_chart(fig_main_pie, use_container_width=True)

# Handle click events
if st.session_state.selected_category is None:
    st.info("Click on a slice in the main pie chart to view its subcategories.")
else:
    st.subheader(f"📊 Subcategories of {st.session_state.selected_category}")
    fig_sub_pie = create_subcategory_pie_chart(st.session_state.selected_category, categories)
    st.plotly_chart(fig_sub_pie, use_container_width=True)

# Allow users to manually select a category (fallback)
st.subheader("🔍 Explore Categories Manually")
selected_category_manual = st.selectbox("Select a category to view its subcategories:", list(categories.keys()))
if selected_category_manual:
    st.session_state.selected_category = selected_category_manual

# Priority setting system
if st.session_state.selected_category:
    st.subheader("🎯 Set Priority")
    priority = st.selectbox("Set Priority:", list(priority_colors.keys()))
    st.markdown(f"Priority for **{st.session_state.selected_category}**: <span style='color:{priority_colors[priority]}'>{priority}</span>", unsafe_allow_html=True)

    # Save preferences to Excel
    df = load_preferences()
    new_row = pd.DataFrame({"Category": [st.session_state.selected_category], "Priority": [priority]})
    df = pd.concat([df, new_row], ignore_index=True).drop_duplicates(subset=["Category"], keep="last")
    save_preferences(df)
    st.success(f"✅ Preferences saved for {st.session_state.selected_category}!")

    # Load saved preferences
    st.subheader("📚 Saved Preferences")
    st.table(df)

# Add animations and real-time updates
st.subheader("🎉 Real-Time Updates")
st.info("Hover over the pie charts or update priorities to see real-time changes!")
