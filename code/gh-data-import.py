"""Load simulated pendulum data for GH """

import rhinoscriptsyntax as rs

m1Points = []
m2Planes = []
if not reload:
    f = open(fname)
    for l in f:
        raw = l.strip().split(" ")
        vals = [float(v) * 1000 for v in raw]
        m1Points.append(rs.coerce3dpoint(vals[:3]))
        m2Planes.append(rs.PlaneFromFrame(vals[3:6], vals[6:9], vals[9:12]))
    f.close()

