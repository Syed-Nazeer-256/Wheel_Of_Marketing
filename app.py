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

# Create a thread-like network graph
def create_thread_graph(categories):
    # Nodes: Categories + Subcategories
    nodes = list(categories.keys())
    subcategory_nodes = [subcat for sublist in categories.values() for subcat in sublist]
    all_nodes = nodes + subcategory_nodes

    # Edges: Connections between categories and their subcategories
    edges = []
    for category, subcats in categories.items():
        for subcat in subcats:
            edges.append((category, subcat))

    # Create edge traces
    edge_x = []
    edge_y = []
    for edge in edges:
        x0, y0 = all_nodes.index(edge[0]), 0  # Source node position
        x1, y1 = all_nodes.index(edge[1]), 1  # Target node position
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    # Create node traces
    node_x = [i for i in range(len(all_nodes))]
    node_y = [0 if node in nodes else 1 for node in all_nodes]
    node_color = ['blue' if node in nodes else 'green' for node in all_nodes]

    # Create figure
    fig = go.Figure()

    # Add edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=1, color='gray'),
        hoverinfo='none'
    ))

    # Add nodes
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=all_nodes,
        marker=dict(size=15, color=node_color),
        textposition="top center",
        hoverinfo='text'
    ))

    # Customize layout
    fig.update_layout(
        title="Thread-Like Category Connections",
        showlegend=False,
        margin=dict(l=0, r=0, b=0, t=40),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        template="plotly_dark"
    )
    return fig

# Display the thread-like network graph
st.title("🌟 Dynamic Marketing Wheel with Thread Visualization 🌟")
st.subheader("🌐 Thread-Like Category Connections")
fig_thread = create_thread_graph(categories)
st.plotly_chart(fig_thread, use_container_width=True)

# Display the 3D wheel
st.subheader("🌍 Interactive 3D Marketing Wheel")
fig_3d = go.Figure()

# Generate points for the wheel
num_categories = len(categories)
theta = [i * 2 * 3.14 / num_categories for i in range(num_categories)]
radius = 1
x = [radius * np.cos(t) for t in theta]
y = [radius * np.sin(t) for t in theta]
z = [0] * num_categories

# Add main category points
fig_3d.add_trace(go.Scatter3d(
    x=x, y=y, z=z,
    mode='markers+text',
    text=list(categories.keys()),
    marker=dict(size=10, color=['blue', 'purple', 'cyan', 'magenta', 'lime', 'gold', 'teal', 'coral']),
    textposition="top center",
    hoverinfo='text'
))

# Customize layout
fig_3d.update_layout(
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
st.plotly_chart(fig_3d, use_container_width=True)

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
