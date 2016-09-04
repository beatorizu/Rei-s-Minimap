from matplotlib import use
use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import interp, Basemap
from numpy import meshgrid
from numpy.ma import MaskedArray
import seaborn as sns


class Minimap:

    def __init__(self, lon, lat, mlon, mlat, urcrnrlat=None, urcrnrlon=None, llcrnrlat=None, llcrnrlon=None):
        self.lon = lon
        self.lat = lat
        self.mlon = mlon
        self.mlat = mlat
        self.basemap = Basemap(urcrnrlat=urcrnrlat,
                               urcrnrlon=urcrnrlon,
                               llcrnrlat=llcrnrlat,
                               llcrnrlon=llcrnrlon,
                               resolution='l')
        self.x, self.y = self.basemap(lon, lat)
        self.x2, self.y2 = self.basemap(*meshgrid(mlon, mlat))

    def maskData(self, data, mask=None):
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
        result = interp(data, self.x, self.y, self.x2, self.y2)
        self.masked_var = MaskedArray(result, mask=mask)

    def renderMap(self, waypoint, shape=[], bounds=[0, 7, 42], cmap=None, norm=None, extend='both', name='NOME',
                  transparent=False):
        plt.clf()
        self.basemap.contourf(self.x2, self.y2, self.masked_var, bounds, cmap=cmap, norm=norm, extend=extend)
        for s in shape:
            self.basemap.readshapefile(s, name)
        self.basemap.colorbar(location='bottom')
        self.basemap.imshow(self.masked_var)
        plt.savefig(waypoint, transparent=transparent, dpi=200, bbox_inches='tight', pad_inches=0.1)
