import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")
st.title("AI Tools Technology Radar (Plotly Interactive)")


# ----------------------------------
# Configuration
# ----------------------------------
quadrant_labels = ["GenAI", "Dev tool", "Platforms", "Tools"]

status_rings = {
    "Approved": {"radius": 2, "color": "rgba(76, 175, 80, 0.25)"},
    "Testing": {"radius": 3, "color": "rgba(255, 193, 7, 0.25)"},
    "Innovation": {"radius": 4, "color": "rgba(33, 150, 243, 0.25)"},
    "Not Approved": {"radius": 5, "color": "rgba(255, 0, 0, 0.25)"},
}

ai_tools = {
    "ChatGPT-4": ("GenAI", "Approved"),
    "Copilot": ("Dev tool", "Approved"),
    "TensorFlow": ("Platforms", "Approved"),
    "Midjourney": ("GenAI", "Testing"),
    "GitHub Actions": ("Tools", "Approved"),
    "LangChain": ("Dev tool", "Testing"),
    "Hugging Face": ("Platforms", "Innovation"),
    "Zapier": ("Tools", "Not Approved"),
    "DALL-E 3": ("GenAI", "Innovation"),
    "Jira": ("Tools", "Testing"),
}


# ----------------------------------
# Precompute ring boundaries
# ----------------------------------
status_order = list(status_rings.keys())
status_radius_map = {s: status_rings[s]["radius"] for s in status_order}

# compute inner radius per ring
status_inner_map = {}
prev = 0
for s in status_order:
    status_inner_map[s] = prev
    prev = status_radius_map[s]


# ----------------------------------
# Create Radar Figure
# ----------------------------------
fig = go.Figure()

# ----- Draw rings (background layers) -----
for status, props in status_rings.items():
    outer = props["radius"]
    inner = status_inner_map[status]

    # Create circular annulus by drawing 100 points around
    theta = np.linspace(0, 2 * np.pi, 200)

    # Outer circle
    x_outer = outer * np.cos(theta)
    y_outer = outer * np.sin(theta)

    # Inner circle (reversed)
    x_inner = inner * np.cos(theta)[::-1]
    y_inner = inner * np.sin(theta)[::-1]

    # Add filled annulus shape
    fig.add_trace(go.Scatter(
        x=np.concatenate([x_outer, x_inner]),
        y=np.concatenate([y_outer, y_inner]),
        fill="toself",
        fillcolor=props["color"],
        line=dict(color="black", width=1),
        name=status,
        hoverinfo="skip"
    ))

    # Add status text (mid radius)
    mid_r = (inner + outer) / 2
    fig.add_trace(go.Scatter(
        x=[0], y=[mid_r],
        text=[status],
        mode="text",
        textfont=dict(size=14, color="black"),
        hoverinfo="skip",
        showlegend=False
    ))


# ----- Draw Quadrant Lines -----
max_r = max(status_radius_map.values())

fig.add_shape(type="line", x0=-max_r, y0=0, x1=max_r, y1=0, line=dict(color="black", width=2))
fig.add_shape(type="line", x0=0, y0=-max_r, x1=0, y1=max_r, line=dict(color="black", width=2))


# ----- Add Quadrant Labels -----
offset = max_r * 0.82

quadrant_positions = [
    (offset, offset),
    (-offset, offset),
    (-offset, -offset),
    (offset, -offset),
]

for label, (x, y) in zip(quadrant_labels, quadrant_positions):
    fig.add_trace(go.Scatter(
        x=[x], y=[y],
        text=[label],
        mode="text",
        textfont=dict(size=16, color="black", family="Arial Black"),
        hoverinfo="skip",
        showlegend=False
    ))


# ----- Add Tools (placed randomly) -----
np.random.seed(42)

for tool, (quadrant, status) in ai_tools.items():
    q_index = quadrant_labels.index(quadrant)

    # Quadrant angle range
    angle_min = q_index * 90
    angle_max = (q_index + 1) * 90
    angle = np.deg2rad(np.random.uniform(angle_min + 8, angle_max - 8))

    # Radial bounds
    r_inner = status_inner_map[status]
    r_outer = status_radius_map[status]
    r = np.random.uniform(r_inner + 0.25, r_outer - 0.25)

    x = r * np.cos(angle)
    y = r * np.sin(angle)

    fig.add_trace(go.Scatter(
        x=[x], y=[y],
        text=[tool],
        mode="text",
        textposition="middle center",
        textfont=dict(size=12),
        showlegend=False,
        hovertemplate=f"<b>{tool}</b><br>Status: {status}<br>Category: {quadrant}<extra></extra>"
    ))


# ----------------------------------
# Final Layout
# ----------------------------------
fig.update_layout(
    width=900,
    height=900,
    title="AI Tools Technology Radar",
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    showlegend=False,
    plot_bgcolor="white",
)

fig.update_xaxes(range=[-max_r - 1, max_r + 1])
fig.update_yaxes(range=[-max_r - 1, max_r + 1])

st.plotly_chart(fig, use_container_width=True)
