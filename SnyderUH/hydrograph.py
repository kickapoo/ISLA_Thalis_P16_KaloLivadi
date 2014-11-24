import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = (10.0, 5.0)


class SnyderUH(object):
    """
    class.Shyder
      Calculation of Snyder Unit Hydrograph

      Atrributes:
        name: Catchment Name
        A: Area
        L: River Length
        Lc: Distance from catchment center to basin exit point
        C1: Unit correction factor
        Ct: Unit Hydrograph regional parameter
        Cp: Unit Hydrograph regional parameter
        tR: Effective rainfall duration

      Methods:
        Snyder.calc()
          Calculate Snyder
        Snyder.plot()
          Plot Snyder Unit Hydrograph

      Reference: Physical Hydrology (2nd edition)
                 S. Lawrence Dingman
                 Waveland Press
                 ISBN: 978-1-577766-561-8
    """
    def __init__(self, name, A, L, Lc, C1=1, Ct=2.0, Cp=0.65, tR=0.5):
        self.name = name
        self.A = A
        self.L = L
        self.Lc = Lc
        self.C1 = C1
        self.Ct = Ct
        self.Cp = Cp
        self.tR = tR

    def calc(self):
        self.tp = self.C1 * self.Ct * \
                  ((self.L * 0.621371) * (self.Lc * 0.621371) ** 0.3)
        self.tr = self.tp / 5.5
        self.tPR = self.tp + 0.25 * (self.tR - self.tr)
        self.QPR = 2.75 * self.Cp * (self.A / self.tPR)
        self.W50 = 2.14 / ((self.QPR / self.A) ** 1.08)
        self.W75 = 1.22 / ((self.QPR / self.A) ** 1.08)
        self.Tb = 11.11 * (self.A / self.QPR) - 1.5 * self.W50 - self.W75
        return dict(tp=self.tp, tr=self.tr, tPR=self.tPR, QPR=self.QPR,
                    W50=self.W50, W75=self.W75, Tb=self.Tb, tR=self.tR)

    def plot(self):
        self.calc()
        self.plot_t = np.array([0, (self.tr / 2 + self.tPR) - self.W50 / 3,
                               (self.tr / 2 + self.tPR) - self.W75 / 3,
                               self.tr / 2 + self.tPR,
                               (self.tr / 2 + self.tPR) + self.W75 / 3,
                               (self.tr / 2 + self.tPR) + self.W50 / 3,
                               self.Tb]
                               )
        self.plot_Q = np.array([0, self.QPR * 0.5, self.QPR * 0.75,
                               self.QPR, self.QPR * 0.75, self.QPR * 0.5, 0])
        fig, ax1 = plt.subplots(1, 1)
        ax1.plot(self.plot_t, self.plot_Q)
        plt.vlines(self.plot_t[3], self.plot_Q[3], 0,
                   color='DarkOrange', linestyle='dashed', lw=2)
        plt.text(self.plot_t[3], self.plot_Q[3], 'QPR')
        plt.hlines(self.plot_Q[2], self.plot_t[2], self.plot_t[4],
                   color='DarkOrange', linestyle='dashed', lw=2)
        plt.text(self.plot_t[4] + 0.3, self.plot_Q[2], 'W75')
        plt.hlines(self.plot_Q[1], self.plot_t[1], self.plot_t[5],
                   color='DarkOrange', linestyle='dashed', lw=2)
        plt.text(self.plot_t[5] + 0.3, self.plot_Q[1], 'W50')
        plt.hlines(self.QPR + 0.5, 0, self.tr,
                   color='Blue', lw=15)
        plt.hlines(self.QPR + 0.5, self.tr / 2, self.plot_t[3],
                   color='DarkOrange', linestyle='-.', lw=2.5)
        plt.text(0.5, self.QPR, 'tR  ' + str(round(self.tr, 4)) + '  hr')
        plt.text(self.Tb / 2, 0.5,
                 'Base time: ' + str(round(self.Tb, 4)) + ' hr')
        plt.hlines(0, 0, self.Tb,
                   color='DarkOrange', linestyle='dashed', lw=5)
        plt.title('Snyder Synthetic Unit Hydrograph')
        plt.xlabel('t (hr)')
        plt.ylabel('Q m3/sec')
        plt.grid()
        plt.savefig('SUH_{}_{}_tr.png'.format(self.name,self.tR),
                    bbox_inches='tight')
