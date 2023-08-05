# marks spots as small green circles when given a list of spots with format [[x,y,r]] and axis to plot on
def marking_spots_plt(spotlist, axis_name):
    import matplotlib.pyplot as plt
    for blob in spotlist:
        y, x, r = blob
        c = plt.Circle((x, y), 1, color="lime", linewidth=1, fill=False)
        axis_name.add_patch(c)
