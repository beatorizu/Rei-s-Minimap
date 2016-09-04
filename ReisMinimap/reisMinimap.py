from matplotlib import use

use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import interp, Basemap
from numpy import meshgrid
from numpy.ma import MaskedArray
import seaborn as sns


class Minimap:
    def __init__(self, lon, lat, urcrnrlat=None, urcrnrlon=None, llcrnrlat=None, llcrnrlon=None):
        self.basemap = Basemap(urcrnrlat=urcrnrlat,
                               urcrnrlon=urcrnrlon,
                               llcrnrlat=llcrnrlat,
                               llcrnrlon=llcrnrlon,
                               resolution='l', fix_aspect=False)
        self.x, self.y = self.basemap(*meshgrid(lon, lat))

    def maskData(self, data, mlon, mlat, mask=None):
        """
        This function apply a mask to a data array

        Parameters
        ----------
        data:numpy.ndarray
        mask:numpy.ndarray or None

        Returns
        -------
            None

        """
        mask_x, mask_y = self.basemap(*meshgrid(mlon, mlat))
        result = interp(data, self.x, self.y, mask_x, mask_y)
        return MaskedArray(result, mask=mask)

    def renderMap(self, data, shape=[], bounds=[0, 7, 42], cmap=None, norm=None, extend='both', name='NOME'):
        plt.clf()
        self.basemap.contourf(self.x, self.y, data, bounds, cmap=cmap, norm=norm, extend=extend)
        for s in shape:
            self.basemap.readshapefile(s, name)
        self.basemap.colorbar(location='bottom')
        self.basemap.imshow(self.masked_var)

    def saveMap(self, waypoint, transparent=False):
        plt.savefig(waypoint, transparent=transparent, bbox_inches='tight', pad_inches=0.1)
