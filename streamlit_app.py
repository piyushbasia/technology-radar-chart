import streamlit as st
import random
import math

st.set_page_config(layout="wide")
st.title("AI Tools Technology Radar (Pure HTML + SVG)")
st.caption("No Plotly, No Matplotlib — Fully rendered using HTML, CSS, and SVG.")

# -------------------------------------------------------
# Data
# -------------------------------------------------------
quadrant_labels = ["GenAI", "Dev tool", "Platforms", "Tools"]

status_rings = {
    "Approved": {"radius": 120, "color": "rgba(76,175,80,0.25)"},
    "Testing": {"radius": 180, "color": "rgba(255,193,7,0.25)"},
    "Innovation": {"radius": 240, "color": "rgba(33,150,243,0.25)"},
    "Not Approved": {"radius": 300, "color": "rgba(255,0,0,0.25)"},
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

# -------------------------------------------------------
# Compute ring boundaries
# -------------------------------------------------------
status_order = list(status_rings.keys())
inner_radius_map = {}
prev = 0

for s in status_order:
    inner_radius_map[s] = prev
    prev = status_rings[s]["radius"]

# Center of SVG radar
CX, CY = 350, 350

# SVG WIDTH / HEIGHT
W, H = 700, 700

# -------------------------------------------------------
# Build SVG dynamically
# -------------------------------------------------------
svg = f"""
<svg width="{W}" height="{H}" style="font-family:Arial;">
    <!-- Background -->
    <rect width="100%" height="100%" fill="white"></rect>
"""

# -------------------------------------------------------
# Draw Rings
# -------------------------------------------------------
for status, props in status_rings.items():
    outer = props["radius"]
    inner = inner_radius_map[status]

    svg += f"""
    <circle cx="{CX}" cy="{CY}" r="{outer}" 
            fill="{props['color']}" 
            stroke="black" stroke-width="1"></circle>

    <!-- Status Label -->
    <text x="{CX}" y="{CY - (inner + outer) / 2}" 
          text-anchor="middle" font-weight="bold" font-size="14">
        {status}
    </text>
    """

# -------------------------------------------------------
# Draw quadrant crosshairs
# -------------------------------------------------------
svg += f"""
<line x1="0" y1="{CY}" x2="{W}" y2="{CY}" stroke="black" stroke-width="2"/>
<line x1="{CX}" y1="0" x2="{CX}" y2="{H}" stroke="black" stroke-width="2"/>
"""

# -------------------------------------------------------
# Quadrant Labels
# -------------------------------------------------------
offset = 330
quad_positions = [
    (CX + offset, CY - offset),
    (CX - offset, CY - offset),
    (CX - offset, CY + offset),
    (CX + offset, CY + offset),
]

for label, (x, y) in zip(quadrant_labels, quad_positions):
    svg += f"""
    <text x="{x}" y="{y}" text-anchor="middle" font-size="18" font-weight="bold">{label}</text>
    """

# -------------------------------------------------------
# Place Tools
# -------------------------------------------------------
random.seed(42)

for tool, (quadrant, status) in ai_tools.items():
    q_index = quadrant_labels.index(quadrant)

    angle_min = q_index * 90 + 10
    angle_max = (q_index + 1) * 90 - 10
    angle_deg = random.uniform(angle_min, angle_max)
    angle_rad = math.radians(angle_deg)

    inner_r = inner_radius_map[status]
    outer_r = status_rings[status]["radius"]
    r = random.uniform(inner_r + 20, outer_r - 20)

    x = CX + r * math.cos(angle_rad)
    y = CY - r * math.sin(angle_rad)

    svg += f"""
    <text x="{x}" y="{y}" text-anchor="middle"
          font-size="12"
          style="background:white; paint-order:stroke; stroke:black; stroke-width:0.5;">
        {tool}
    </text>
    """

# Close SVG
svg += "</svg>"

# -------------------------------------------------------
# Render in Streamlit
# -------------------------------------------------------
st.components.v1.html(svg, height=750, width=750, scrolling=False)
