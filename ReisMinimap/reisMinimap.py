from matplotlib import use

use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import interp, Basemap
from numpy import meshgrid
from numpy.ma import MaskedArray


class Minimap:
    def __init__(self, lon, lat, urcrnrlat=None, urcrnrlon=None, llcrnrlat=None, llcrnrlon=None):
        self.basemap = Basemap(urcrnrlat=urcrnrlat,
                               urcrnrlon=urcrnrlon,
                               llcrnrlat=llcrnrlat,
                               llcrnrlon=llcrnrlon,
                               resolution='l', fix_aspect=False)
        self.x, self.y = self.basemap(*meshgrid(lon, lat))

    def maskData(self, data, lon, lat, mlon, mlat, mask=None):
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
        self.x, self.y = self.basemap(*meshgrid(mlon, mlat))
        result = interp(data, lon, lat, self.x, self.y)
        return MaskedArray(result, mask=mask)

    def renderMap(self, data, shape=[], bounds=[0, 7, 42], cmap=None, norm=None, extend='both', name='NOME'):
        plt.clf()
        # TODO: Add flag or use Interfaces
        self.basemap.bluemarble()
        self.basemap.contourf(self.x, self.y, data, bounds, cmap=cmap, norm=norm, extend=extend)
        for s in shape:
            self.basemap.readshapefile(s, name, linewidth=0.25)
        # self.basemap.colorbar(location='bottom')

    def saveMap(self, waypoint, transparent=False):
        plt.savefig(waypoint, transparent=transparent, bbox_inches='tight', pad_inches=0)
