import streamlit as st
import numpy as np
import json

# Page config
st.set_page_config(layout="wide")
st.title("AI Tools Technology Radar (SVG)")

# --- Configuration ---
quadrant_labels = ["GenAI", "Dev tool", "Platforms", "Tools"]
status_rings = {
    "Approved": {"radius": 2, "color": "#4CAF50"},
    "Testing": {"radius": 3, "color": "#FFC107"},
    "Innovation": {"radius": 4, "color": "#2196F3"},
    "Not Approved": {"radius": 5, "color": "#FF0000"},
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

# Precompute ring boundaries
status_order = list(status_rings.keys())
status_radius_map = {s: status_rings[s]["radius"] for s in status_order}
status_inner_map = {}
prev = 0.0
for s in status_order:
    status_inner_map[s] = prev
    prev = status_radius_map[s]

# Compute tool positions
np.random.seed(42)
tool_positions = []
max_radius = max(status_radius_map.values())
for tool, (quadrant, status) in ai_tools.items():
    q_idx = quadrant_labels.index(quadrant)
    # angle
    angle_min = q_idx * 90
    angle_max = (q_idx + 1) * 90
    angle_deg = np.random.uniform(angle_min + 5, angle_max - 5)
    angle_rad = np.deg2rad(angle_deg)
    # radius
    r_inner = status_inner_map[status]
    r_outer = status_radius_map[status]
    r = np.random.uniform(r_inner + 0.25, r_outer - 0.25)
    x = r * np.cos(angle_rad)
    y = r * np.sin(angle_rad)
    tool_positions.append({
        "name": tool,
        "quadrant": quadrant,
        "status": status,
        "x": x,
        "y": y
    })

# Convert to JSON for JS / HTML
tool_json = json.dumps(tool_positions)
ring_json = json.dumps([
    {"status": s, "radius": status_rings[s]["radius"], "color": status_rings[s]["color"]}
    for s in status_order
])
quadrant_json = json.dumps([
    {"label": quadrant_labels[i], "angle_start": i * 90, "angle_end": (i+1)*90}
    for i in range(len(quadrant_labels))
])

# --- Build SVG HTML ---
html = f"""
<div>
  <svg width="600" height="600" viewBox="-6 -6 12 12" xmlns="http://www.w3.org/2000/svg">
    <!-- Draw rings -->
    {''.join([
      f'<circle cx="0" cy="0" r="{status_rings[s]["radius"]}" fill="none" stroke="{status_rings[s]["color"]}" stroke-width="0.05"/>' 
      for s in status_order
    ])}
    <!-- Quadrant lines -->
    <line x1="-{max_radius}" y1="0" x2="{max_radius}" y2="0" stroke="black" stroke-width="0.03"/>
    <line x1="0" y1="-{max_radius}" x2="0" y2="{max_radius}" stroke="black" stroke-width="0.03"/>
    <!-- Quadrant labels -->
    {''.join([
      f'<text x="{(max_radius+0.5)*np.cos(np.deg2rad((i*90 + (i+1)*90)/2))}" y="{(max_radius+0.5)*np.sin(np.deg2rad((i*90 + (i+1)*90)/2))}" ' +
      'font-size="0.6" font-weight="bold" text-anchor="middle" alignment-baseline="middle">{quadrant_labels[i]}</text>'
      for i in range(4)
    ])}
    <!-- Tools -->
    {''.join([
      f'<text x="{p["x"]:.3f}" y="{p["y"]:.3f}" font-size="0.4" text-anchor="middle" alignment-baseline="middle" ' +
      'style="fill:black; background: white;">{p["name"]}</text>'
      for p in tool_positions
    ])}
  </svg>
</div>
"""

# Embed the SVG in the app
import streamlit.components.v1 as components
components.html(html, height=620, width=620)

st.write("Status Rings: ", status_rings)
st.write("Tool Positions:", tool_positions)
