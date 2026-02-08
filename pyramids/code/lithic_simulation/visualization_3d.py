import numpy as np
import plotly.graph_objects as go

def get_box_mesh(x_min, x_max, y_min, y_max, z_min, z_max):
    """
    Generates vertices and indices for a 3D box mesh.
    """
    # Vertices (8 corners)
    x = [x_min, x_min, x_max, x_max, x_min, x_min, x_max, x_max]
    y = [y_min, y_max, y_max, y_min, y_min, y_max, y_max, y_min]
    z = [z_min, z_min, z_min, z_min, z_max, z_max, z_max, z_max]
    
    # 12 triangles (2 per face, 6 faces)
    # Standard cube triangulation indices
    i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
    j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
    k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6]
    
    return x, y, z, i, j, k

def visualize_chamber_resonance(L, W, H, nx, ny, nz):
    """
    Creates a 3D Volumetric Plot of the standing wave pressure field.
    Also renders the 9 Granite Beams above the chamber.
    """
    # 1. The Grid (Sparse enough for web rendering)
    res_x = 40
    res_y = 20
    res_z = 20
    X, Y, Z = np.mgrid[0:L:complex(res_x), 0:W:complex(res_y), 0:H:complex(res_z)]
    
    # 2. The Physics (Standing Wave Equation)
    # P = cos(nx*pi*x/L) * cos(ny*pi*y/W) * cos(nz*pi*z/H)
    P = np.cos(nx * np.pi * X / L) * np.cos(ny * np.pi * Y / W) * np.cos(nz * np.pi * Z / H)
    
    fig = go.Figure()
    
    # 3. The Render (Volume)
    fig.add_trace(go.Volume(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=P.flatten(),
        isomin=-0.5, # Show only significant pressure
        isomax=0.5,
        opacity=0.15, # Semi-transparent to see structure
        surface_count=15, # Number of isosurfaces
        colorscale='RdBu', # Red=High, Blue=Low
        caps=dict(x_show=False, y_show=False, z_show=False),
        name="Pressure Field"
    ))
    
    # 4. The Structure (9 Granite Beams)
    # Assumed Logic: Beams span the Width (Y), stacked along Length (X)
    beam_width_x = L / 9.0 
    beam_height_z = 1.5 # Meters (approx thickness)
    
    for b in range(9):
        x0 = b * beam_width_x + 0.05 # Small gap
        x1 = (b+1) * beam_width_x - 0.05
        y0 = 0
        y1 = W
        z0 = H # Rest on top of walls
        z1 = H + beam_height_z
        
        bx, by, bz, bi, bj, bk = get_box_mesh(x0, x1, y0, y1, z0, z1)
        
        fig.add_trace(go.Mesh3d(
            x=bx, y=by, z=bz,
            i=bi, j=bj, k=bk,
            opacity=0.2, # Glassy look
            color='darkgrey',
            name=f'Beam {b+1}',
            hoverinfo='name'
        ))
        
    # Layout
    fig.update_layout(
        title=f"Volumetric Resonance (Harmonics: {nx}-{ny}-{nz})",
        scene=dict(
            xaxis_title='Length (m)',
            yaxis_title='Width (m)',
            zaxis_title='Height (m)',
            # Aspect ratio matching physical dimensions
            aspectratio=dict(x=L/H, y=W/H, z=(H+2)/H) 
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        height=600
    )
    
    return fig

