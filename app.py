import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from openpyxl import load_workbook
import numpy as np

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
        df = pd.read_excel("user_preferences.xlsx", sheet_name="Preferences")
        return df
    except FileNotFoundError:
        st.error("Preferences file not found. Please ensure `data/user_preferences.xlsx` exists.")
        return pd.DataFrame(columns=["Category", "Priority"])

# Save preferences to Excel
def save_preferences(df):
    with pd.ExcelWriter("user_preferences.xlsx", engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Preferences")

# Create a 3D network graph
def create_3d_network_graph(categories):
    # Nodes: Categories + Subcategories
    nodes = list(categories.keys())
    subcategory_nodes = [subcat for sublist in categories.values() for subcat in sublist]
    all_nodes = nodes + subcategory_nodes

    # Edges: Connections between categories and their subcategories
    edges = []
    for category, subcats in categories.items():
        for subcat in subcats:
            edges.append((all_nodes.index(category), all_nodes.index(subcat)))

    # Generate random positions for nodes in 3D space
    np.random.seed(42)  # For reproducibility
    node_positions = {i: (np.random.rand(), np.random.rand(), np.random.rand()) for i in range(len(all_nodes))}

    # Create edge traces
    edge_x = []
    edge_y = []
    edge_z = []
    for src, tgt in edges:
        x0, y0, z0 = node_positions[src]
        x1, y1, z1 = node_positions[tgt]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
        edge_z += [z0, z1, None]

    # Create node traces
    node_x = [node_positions[i][0] for i in range(len(all_nodes))]
    node_y = [node_positions[i][1] for i in range(len(all_nodes))]
    node_z = [node_positions[i][2] for i in range(len(all_nodes))]
    node_color = ['blue' if node in nodes else 'green' for node in all_nodes]

    # Create figure
    fig = go.Figure()

    # Add edges
    fig.add_trace(go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode='lines',
        line=dict(width=1, color='gray'),
        hoverinfo='none'
    ))

    # Add nodes
    fig.add_trace(go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers+text',
        text=all_nodes,
        marker=dict(size=8, color=node_color),
        textposition="top center",
        hoverinfo='text'
    ))

    # Customize layout
    fig.update_layout(
        title="3D Network Graph of Categories and Subcategories",
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False)
        ),
        showlegend=False,
        margin=dict(l=0, r=0, b=0, t=40),
        template="plotly_dark"
    )
    return fig

# Create a 3D pie chart
def create_3d_pie_chart(categories):
    labels = list(categories.keys())
    values = [len(subcats) for subcats in categories.values()]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=12,
                      marker=dict(colors=['blue', 'purple', 'cyan', 'magenta', 'lime', 'gold', 'teal', 'coral']))
    fig.update_layout(title="3D Pie Chart of Category Distribution", template="plotly_dark")
    return fig

# Create a bubble chart
def create_bubble_chart(categories):
    labels = list(categories.keys())
    sizes = [len(subcats) for subcats in categories.values()]
    colors = ['blue', 'purple', 'cyan', 'magenta', 'lime', 'gold', 'teal', 'coral']

    fig = go.Figure(data=[go.Scatter(
        x=labels, y=sizes, mode='markers', marker=dict(size=sizes, color=colors, sizemode='area', sizeref=2.*max(sizes)/(40.**2))
    )])
    fig.update_layout(title="Bubble Chart of Category Sizes", template="plotly_dark")
    return fig

# Display the 3D network graph
st.title("🌟 Dynamic Marketing Wheel with Advanced Visualizations 🌟")
st.subheader("🌐 3D Network Graph of Categories and Subcategories")
fig_3d_network = create_3d_network_graph(categories)
st.plotly_chart(fig_3d_network, use_container_width=True)

# Display the 3D pie chart
st.subheader("📊 3D Pie Chart of Category Distribution")
fig_3d_pie = create_3d_pie_chart(categories)
st.plotly_chart(fig_3d_pie, use_container_width=True)

# Display the bubble chart
st.subheader("🎈 Bubble Chart of Category Sizes")
fig_bubble = create_bubble_chart(categories)
st.plotly_chart(fig_bubble, use_container_width=True)

# Display the 3D wheel
st.subheader("🌍 Interactive 3D Marketing Wheel")
fig_3d_wheel = go.Figure()

# Generate points for the wheel
num_categories = len(categories)
theta = [i * 2 * 3.14 / num_categories for i in range(num_categories)]
radius = 1
x = [radius * np.cos(t) for t in theta]
y = [radius * np.sin(t) for t in theta]
z = [0] * num_categories

# Add main category points
fig_3d_wheel.add_trace(go.Scatter3d(
    x=x, y=y, z=z,
    mode='markers+text',
    text=list(categories.keys()),
    marker=dict(size=10, color=['blue', 'purple', 'cyan', 'magenta', 'lime', 'gold', 'teal', 'coral']),
    textposition="top center",
    hoverinfo='text'
))

# Customize layout
fig_3d_wheel.update_layout(
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
st.plotly_chart(fig_3d_wheel, use_container_width=True)

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
