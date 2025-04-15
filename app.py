import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sqlite3

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

# Create a 3D scatter plot for the wheel
def create_3d_wheel(categories):
    fig = go.Figure()

    # Generate points for the wheel
    num_categories = len(categories)
    theta = np.linspace(0, 2 * np.pi, num_categories, endpoint=False)
    radius = 1
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = np.zeros(num_categories)

    # Add main category points with hover effects
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers+text',
        text=list(categories.keys()),
        marker=dict(size=10, color=['blue', 'purple', 'cyan', 'magenta', 'lime', 'gold', 'teal', 'coral']),
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
        title_font=dict(color="darkblue", size=20)
    )
    return fig

# Display the wheel in Streamlit
st.title("🌟 3D Marketing Wheel Interface 🌟")
fig = create_3d_wheel(categories)
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

    # Save preferences to SQLite database
    conn = sqlite3.connect('data/user_preferences.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS preferences
                 (category TEXT, priority TEXT)''')

    if st.button("💾 Save Preferences"):
        c.execute("INSERT INTO preferences (category, priority) VALUES (?, ?)",
                  (st.session_state.selected_category, priority))
        conn.commit()
        st.success(f"✅ Preferences saved for {st.session_state.selected_category}!")

    # Load saved preferences
    c.execute("SELECT * FROM preferences")
    preferences = c.fetchall()
    st.subheader("📚 Saved Preferences")
    st.table(preferences)

    # Close connection
    conn.close()

# Add animations and real-time updates
st.subheader("🎉 Real-Time Updates")
st.info("Hover over the wheel or update priorities to see real-time changes!")