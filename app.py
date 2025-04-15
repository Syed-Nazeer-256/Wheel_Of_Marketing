import streamlit as st
import plotly.graph_objects as go
import numpy as np
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

# Create a dynamic 3D scatter plot for the wheel
def create_3d_wheel(categories, selected_category=None):
    fig = go.Figure()

    # Generate points for the wheel
    num_categories = len(categories)
    theta = np.linspace(0, 2 * np.pi, num_categories, endpoint=False)
    radius = 1
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = np.zeros(num_categories)

    # Add main category points with hover effects
    colors = ['blue', 'purple', 'cyan', 'magenta', 'lime', 'gold', 'teal', 'coral']
    if selected_category:
        colors = ["yellow" if cat == selected_category else color for cat, color in zip(categories.keys(), colors)]

    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers+text',
        text=list(categories.keys()),
        marker=dict(size=10, color=colors),
        textposition="top center",
        hoverinfo='text'
    ))

    # Customize layout
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False)
        ),
        showlegend=False,
        margin=dict(l=0, r=0, b=0, t=0),
        title="Interactive 3D Marketing Wheel",
        title_font=dict(color="darkblue", size=20),
        template="plotly_dark"
    )
    return fig

# Display the wheel in Streamlit
st.title("🌟 Live Dynamic 3D Marketing Wheel 🌟")
fig = create_3d_wheel(categories, st.session_state.selected_category)
st.plotly_chart(fig, use_container_width=True)

# Category selection and expansion
st.subheader("🔍 Explore Categories")
selected_category = st.selectbox("Select a category to expand:", list(categories.keys()))
if selected_category:
    st.session_state.selected_category = selected_category

# Display subcategories if a category is selected
if st.session_state.selected_category:
    subcategories = categories[st.session_state.selected_category]
    st.write(f"✨ Subcategories for **{st.session_state.selected_category}**: ✨")
    st.markdown("\n".join([f"- {subcat}" for subcat in subcategories]))

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
st.info("Hover over the wheel or update priorities to see real-time changes!")
