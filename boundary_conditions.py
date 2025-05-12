import json
import sys
import pyvista as pv
import numpy as np

def generate_boundary_conditions(mesh_file, output_file="testing-input-output/boundary_conditions.json"):
    """Processes the mesh and creates a structured boundary condition JSON file using improved region detection."""

    # Load the mesh
    mesh = pv.read(mesh_file)

    # Verify Mesh Properties
    print(f"🔍 Loaded Mesh: {mesh}")

    # Initialize Boundary Conditions Structure
    boundary_conditions = {
        "inlet": {"region_id": [], "velocity": [1.0, 0.0, 0.0]},
        "outlet": {"region_id": [], "pressure": 101325},
        "walls": {"region_id": [], "no_slip": True}
    }

    # Compute Percentiles for Improved Boundary Detection
    z_min = np.percentile(mesh.points[:, 2], 5)  # Lower 5% of points → Inlet
    z_max = np.percentile(mesh.points[:, 2], 95)  # Upper 5% of points → Outlet

    # Extract Surface Normals for Wall Detection
    if mesh.n_points > 0:
        normals = mesh.point_normals
    else:
        print("⚠️ No surface normals found. Wall detection might be inaccurate.")
        normals = None

    # Assign Boundary Regions
    for i, point in enumerate(mesh.points):
        if point[2] > z_max:  # Outlet (Upper region)
            boundary_conditions["outlet"]["region_id"].append(i)
        elif point[2] < z_min:  # Inlet (Lower region)
            boundary_conditions["inlet"]["region_id"].append(i)
        elif normals is not None and abs(normals[i][2]) < 0.2:  # Walls (Mostly vertical surfaces)
            boundary_conditions["walls"]["region_id"].append(i)

    # Save Boundary Conditions to JSON
    with open(output_file, "w") as f:
        json.dump(boundary_conditions, f, indent=4)

    # ✅ Print JSON to Logs for Visibility
    print("\n🔹 Generated Boundary Conditions:")
    print(json.dumps(boundary_conditions, indent=4))

    print(f"\n✅ Boundary conditions saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Usage: python boundary_conditions.py <mesh.obj>")
        sys.exit(1)

    mesh_file = sys.argv[1]
    generate_boundary_conditions(mesh_file)



