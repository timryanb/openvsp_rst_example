import numpy as np
import openvsp as vsp
import matplotlib.pyplot as plt

# Open VSP geometry
vsp_file = 'wing.vsp3'
vsp.ReadVSPFile(vsp_file)
all_geoms = vsp.FindGeoms()
geom_id = all_geoms[0]

# Create a grid of test points in rst for wing
nr = 25
ns = 5
nt = 3
r_array = np.linspace(0.0, 1.0, nr)
s_array = np.linspace(0.0, 0.5, ns)
t_array = np.linspace(0.0, 1.0, nt)
rst0 = np.zeros([nr, ns, nt, 3])
rst0[:, :, :, 0], rst0[:, :, :, 1], rst0[:, :, :, 2] = np.meshgrid(r_array, s_array, t_array, indexing='ij')
rst0 = rst0.reshape(-1, 3)
# Find the test points xyz locations
pts0 = vsp.CompVecPntRST(geom_id, 0, rst0[:, 0], rst0[:, 1], rst0[:, 2])
xyz0 = np.array([[pnt.x(), pnt.y(), pnt.z()] for pnt in pts0])

# Preform RST projection on test points (this should give the rst points we defined in the step above)
r1, s1, t1, d1 = vsp.FindRSTVec(geom_id, 0, pts0)
# Evaluate the new rst projections in xyz (again, these should be the same points we found above)
pts1 = vsp.CompVecPntRST(geom_id, 0, r1, s1, t1)
xyz1 = np.array([[pnt.x(), pnt.y(), pnt.z()] for pnt in pts1])

# Print max error from projection
print(f'Max projection error is: {max(d1)}')

# Plot the test points vs projected points in xy
fig = plt.figure(0)
ax = fig.add_subplot(projection='3d')
ax.set_title('Wing projection test')
ax.scatter(xyz0[:, 0], xyz0[:, 1], xyz0[:, 2])
ax.scatter(xyz1[:, 0], xyz1[:, 1], xyz1[:, 2])
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend(['Original points', 'rst Projections'])
plt.show()