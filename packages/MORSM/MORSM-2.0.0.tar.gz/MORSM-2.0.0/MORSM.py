#!/usr/bin/env python3


"""
Copyright (C) by Almog Blaer 

   __  __  ____  _____        _____ __  __ 
  |  \/  |/ __ \|  __ \      / ____|  \/  |
  | \  / | |  | | |__) |____| (___ | \  / |
  | |\/| | |  | |  _  /______\___ \| |\/| |
  | |  | | |__| | | \ \      ____) | |  | |
  |_|  |_|\____/|_|  \_\    |_____/|_|  |_|
                                      
                                      
Get ready and fasten your seat belts, we are going to launch a synthetic earthquake at any location you wish.
This code can depict a finite segment that is aimed to be planted in SW4 software.
All you need is to tell us  about your computational domain and  about the segment's kinematic.

parameters list: 

dh: set the grid spacing in your computational domain
Xc: set north-south Cartesian location of the segment's center
Yc: set the location east-west Cartesian location of the segment's center
Zc: set the depth hypocenter in Cartesian location of the segment's center
dip: segment's dip
strike: segment's strike
rake: segment's angle from the horizon
Ga: Shear modulus 
Vr_2:  set the second velocity of stage II
Vr_1: set the first velocity  of stage I
sec_stage1: set how long  the first stage will be with Vr_1
EveMag: set the desired magnitude.

aD: set the max slip location (down-up direction)
bD: set the max slip location (south-north or east-west direction)
aH: set the nucliation location  (down-up direction)
bH: set the nucliation location  (south-north or east-west direction).

bH, aH > 0 segment with northern (+X) diractivity and downwards (+Z)
bH, aH < 0 segment with southern (-X) diractivity and upwnwards (-Z)
bH < 0, aH > 0 segment with southern (-X) diractivity and downwards (+Z)
bH > 0, aH < 0  segment with northern (+X) diractivity and upwnwards (-Z)
aH = bH Simetric segment

"""

import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
import glob
import logging
import itertools

params = {'dh': 171,  # set the grid spacing in your computational domain
          'Xc': 175.489469137e3,  # set north-south Cartesian location of the segment's center
          'Yc': 127683.51375307699,  # set the location east-west Cartesian location of the segment's center
          'Zc': 10000,  # set the depth hypocenter in Cartesian location of the segment's center
          'dip': 90,  # segment's dip
          'strike': 0,  # segment's strike
          'rake': 0,  # # segment's angle from the horizon
          'Ga': 30000000000.0,  # Shear modulus
          'Vr_2': 2300,  # set the second velocity od the segment of stage II
          'Vr_1': 1000,  # set the first velocity od the segment  of stage I
          'aH': -0.4,  # set the max slip location (down-up direction)
          'bH': 0.4,  # set the max slip location (south-north or east-west direction)
          'aD': 0.0,  # set the first pixel location time to operate in the segment (down-up direction)
          'bD': 0.0,  # set the first pixel location time to operate in the segment (south-north or east-west direction)
          'sec_stage1': 4,  # set how long  the first stage will be with Vr_1
          'EveMag': 6.3,  # set the desired magnitude
          'freq': 6.2831,
          'type': 'Gaussian'
          }

_LOG_LEVEL_STRINGS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
loglevel = 'DEBUG'  # any one of: CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET
formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d | %(name)s | %(levelname)s | %(message)s',
                              datefmt='%Y-%m-%dT%H:%M:%S')

log = logging.getLogger('MOR-SM')
log.setLevel(loglevel)

parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=
        '''
        Moment-rate ORriented Slip Model, enables control on 
        earthquakes moment rate timing, as seen from inversions word-wide
        ''',
        epilog='''Created by Almog Blaer (blaer@post.bgu.ac.il), 2021 @ GSI/BGU''')
parser.version = '2.0'
parser.add_argument('-v', '--verbose', help='verbose - print log messages to screen?', action='store_true',
                        default=False)
parser.add_argument('-l', '--log_level', choices=_LOG_LEVEL_STRINGS, default=loglevel,
                        help=f"Log level (Default: {loglevel}). see Python's Logging module for more details")
parser.add_argument('--logfile', metavar='log file name', help='log to file', default=None)
parser.add_argument('-p', '--paramfile', metavar='parameter-file', help='Parameter file.', default=None)
parser.add_argument('-o', '--outfile', metavar='output-file',
                        help='Output SW4 source commands file (see Chapter 11.2 in SW4 manual)',
                        default='MORSM.txt')
parser.add_argument('--slip', default=False, help="shows nice slip model to have",
                        action=argparse.BooleanOptionalAction)
parser.add_argument('--database', default=False, help="depicts SCARDERC database and MORSM event on it",
                    action=argparse.BooleanOptionalAction)
parser.add_argument('--stf', default=False, help="shows accumulated seismic moment and source time function (STF)",
                        action=argparse.BooleanOptionalAction)

args = parser.parse_args()



def purge(dir, pattern):
    """
    deletes the output files, to avoid duplicates
    :param dir: path to dir
    :param pattern: output files
    """
    for f in glob.glob(f'{dir}/{pattern}'):
        os.remove(os.path.join(dir, f))


class MORSM:
    """ Creates kinematic slip model"""

    def __init__(self, args):
        self.params = params
        if args.verbose:
            # create console handler
            ch = logging.StreamHandler()
            ch.setLevel(args.log_level)
            ch.setFormatter(formatter)
            if logging.StreamHandler not in [h.__class__ for h in self.log.handlers]:
                self.log.addHandler(ch)
            else:
                self.log.warning('log Stream handler already applied.')
        if args.logfile:
            # create file handler
            fh = TimedRotatingFileHandler(args.logfile,
                                          when='midnight',
                                          utc=True)
            fh.setLevel(args.log_level)
            fh.setFormatter(formatter)
            if TimedRotatingFileHandler not in [h.__class__ for h in self.log.handlers]:
                self.log.addHandler(fh)
            else:
                self.log.warning('Log file handler already applied.')

    def run(self):
        sum_slip = 0
        i_s, j_s, _, _ = self.scalars()
        pro = itertools.product(i_s, j_s)
        while True:
            try:
                i, j = next(pro)
                x, y, z = self.point(i=i, j=j)
                slip_m, m0 = self.slip_func(i=i, j=j)
                sum_slip += m0
                t0 = self.time_func(i=i, j=j)
                with open(args.outfile, 'a') as f:
                    f.writelines(f'source x={x} y={y} z={z} m0={m0} t0={t0} '
                                 f'strike={params["strike"]} dip={params["dip"]} '
                                 f'freq={params["freq"]} type={params["type"]}\n')
                with open('fig.txt', 'a') as fig:
                    fig.writelines(f'{i} {j} {t0} {m0} {slip_m}\n')
            except StopIteration:
                break

        self.write_header(args.outfile, sum_slip)
        if args.slip:
            self.slipfigure()

    def write_header(self, FILENAME, sum_slip):
        """
        writes the params that where set and calculated to the
        SW4 outpu4 file
        :param filename: outpit file (default MORSM.txt)
        :return: None
        """

        M0 = sum_slip * self.params['dh'] ** 2
        Mw = MORSM.moment2mag(M0)
        max_slip, mean_slip, W, Y, faultarea = self.mag2fault_goda(self.params['EveMag'])
        faultarea = faultarea / 1e6
        header = (f''' \

##############################################
#  Copyright (C) by Almog Blaer              #
#   __  __  ____  _____        _____ __  __  #
#  |  \/  |/ __ \|  __ \      / ____|  \/  | #
#  | \  / | |  | | |__) |____| (___ | \  / | #
#  | |\/| | |  | |  _  /______\___ \| |\/| | #
#  | |  | | |__| | | \ \      ____) | |  | | #
#  |_|  |_|\____/|_|  \_\    |_____/|_|  |_| #
##############################################                                      
                             

# Fault area [km^2] {faultarea:.2f}
# Magnitude [Mw] {Mw:.2f}
# Seismic moment [Nm] {M0:.2f}
# Total Slip [m] {sum_slip:.2f}
# length [m] {Y:.2f}
# width [m] {W:.2f}
# Mean Slip [m] {mean_slip:.2f}

# Vr_1 [m/sec]={params["Vr_1"]}
# Vr_2 [m/sec]={params["Vr_2"]}
# dh [m]={params["dh"]}
# Xc={params["Xc"]}
# Yc={params["Yc"]}
# Zc={params["Zc"]}
# dip [deg]={params["dip"]}
# strike [deg]={params["strike"]}
# rake [deg]={params["rake"]}
# Ga [Pa]={params["Ga"]}
# aH={params["aH"]}
# bH={params["bH"]}
# aD={params["aD"]}
# bD={params["bD"]}
##############################

''')
        with open(FILENAME, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(header.rstrip('\r\n') + '\n' + content)

    def moment2mag(moment):
        """
        converts magnitude to seismic  moment
        :param moment:, Nm units
        :return: madnitude, Mw
        """

        return (2 / 3) * (np.log10(moment) - 9.1)

    def mag2fault_goda(self, EveMag):
        """
        This function define the segment kinematics by Goda (2016),
        using empirical equations magnitude-features.

        :param EveMag: event manitude from the params dictionary
        :return: falut features: max_slip; mean_slip; W; Y; faultarea
        """

        max_slip = 10 ** (-3.7393 + 0.615 * EveMag) + 0.2249  # Segment's max slip, meters
        mean_slip = 10 ** (-4.3611 + 0.6238 * EveMag) + 0.2502  # Segment's average slip, meters
        W = (10 ** (-0.6892 + 0.2893 * EveMag) + 0.1464) * 1000  # Segment's width, meters
        Y = (10 ** (-2.1621 + 0.5493 * EveMag) + 0.1717) * 1000  # Segment's length, meters
        faultarea = W * Y
        return max_slip, mean_slip, W, Y, faultarea

    def vector(self):
        """
        define the vector space span, using fault
        parameters-based: strike, rake and dip
        """
        strike, rake, dip = (self.params['strike'],
                             self.params['rake'],
                             self.params['dip'])
        vec1 = np.array([np.cos(strike * np.pi / 180),
                         np.sin(strike * np.pi / 180),
                         np.sin(rake * np.pi / 180)])
        vec2 = np.array([np.sin(rake * np.pi / 180),
                         np.cos(dip * np.pi / 180),
                         np.sin(dip * np.pi / 180)])

        return vec1, vec2

    def scalars(self):
        """
        find the surfaces' scalars
        """
        _, _, W, Y, _ = self.mag2fault_goda(EveMag=self.params['EveMag'])
        dh = self.params['dh']
        # example No.1 : i_s and j_s = 0 -->
        # the point would be the fault center (Xc, Yc and Zc)
        # example No.2 : i_s and j_s = W/2 and Y/2 respectively  -->
        # the point would be the fault's bottom right edge (north or east, depends on the faults strike)
        i_s = (i for i in np.arange(-W / 2, W / 2, dh))
        j_s = (j for j in np.arange(-Y / 2, Y / 2, dh))
        i_len, j_len = (len(np.arange(-W / 2, W / 2, dh)),
                        len(np.arange(-Y / 2, Y / 2, dh)))
        return i_s, j_s, i_len, j_len

    def point(self, i, j):
        """
        find the surface cartesian coordinates x, y and z
        """
        Xc, Yc, Zc = (self.params['Xc'],
                      self.params['Yc'],
                      self.params['Zc'])
        vec1, vec2 = self.vector()
        # finds the point in the surface with x, y and z
        x, y, z = np.array([Xc, Yc, Zc]) + i * vec2 + j * vec1
        return x, y, z

    def slip_func(self, i, j):
        """generate the slip function on the coordinates"""
        max_slip, _, W, Y, _ = self.mag2fault_goda(EveMag=self.params['EveMag'])
        aD, bD, dh, Ga = (self.params['aD'],
                          self.params['bD'],
                          self.params['dh'],
                          self.params['Ga'])
        slip_m = max_slip * np.exp(-((i) / (W / 2) + aD) ** 2 - ((j) / (Y / 2) + bD) ** 2)
        return slip_m, slip_m * (dh ** 2) * Ga

    def velocitytotime(self):
        """
        add paper name
        :return:
        """
        _, _, _, _, faultarea = self.mag2fault_goda(EveMag=self.params['EveMag'])
        Vr_1, Vr_2 = (self.params['Vr_1'],
                      self.params['Vr_2'])
        Ts_1 = 2 * np.sqrt(faultarea) / (3 * Vr_1)  # compute the first stage long time with Vr_1
        Ts_2 = 2 * np.sqrt(faultarea) / (3 * Vr_2)  # compute the second stage long time with Vr_2

        return Ts_1, Ts_2

    def time_func(self, i, j):
        """generate the time function on the fault's coordinates"""
        _, _, W, Y, _ = self.mag2fault_goda(EveMag=self.params['EveMag'])
        aH, bH, Vr_1, Vr_2, sec_stage1 = (self.params['aH'],
                                          self.params['bH'],
                                          self.params['Vr_1'],
                                          self.params['Vr_2'],
                                          self.params['sec_stage1'])
        Ts_1, Ts_2 = self.velocitytotime()
        time_INV_1 = ((Ts_1 / (2 ** 0.5)) * (
                (((i) / (W / 2)) + aH) ** 2 + (((j) / (Y / 2)) + bH) ** 2) ** 0.5)
        time_INV_2 = (Ts_2 / (2 ** 0.5)) * (
                (((i) / (W / 2)) + aH) ** 2 + (((j) / (Y / 2)) + bH) ** 2) ** 0.5
        stage2 = (Vr_2 * sec_stage1 - (Vr_1 * sec_stage1)) / Vr_2 + time_INV_2
        return time_INV_1 if time_INV_1 <= sec_stage1 else stage2

    def read_fig():
        try:
            data = np.loadtxt('fig.txt')
            return data[:, 0], data[:, 1], data[:, 2], data[:, 3], data[:, 4]
        except OSError:
            raise OSError("fig.txt not found")

    def slipfigure(self, size=(10, 7)):
        i, j, time, _, slip = MORSM.read_fig()
        _, _, i_s_len, j_s_len = self.scalars()
        i = i.reshape(i_s_len, j_s_len)
        j = j.reshape(i_s_len, j_s_len)
        slip = slip.reshape(i_s_len, j_s_len)
        time = time.reshape(i_s_len, j_s_len)

        fig, ax = plt.subplots(figsize=(10, 5))
        cm = plt.cm.get_cmap('jet')
        sc = ax.contourf(j, i, slip, vmin=slip.min(), vmax=slip.max(), cmap=cm)
        cbar = fig.colorbar(sc, ax=ax, shrink=0.9)
        cbar.set_label(r'Slip, m')

        contours = plt.contour(j, i, time, 10, colors='black')
        plt.clabel(contours, inline=True, fontsize=8, fmt='%1.1f')
        ax.set_xlabel('Length, km')
        ax.set_ylabel('Width, km')
        plt.show()


class Valle:
    """
    Generates a graph that describes SCARDEC database (Valle et al. 2011)
    and MORSM model on it
    """

    def __init__(self, args):
        self.dict_events = {}

    def run(self):

        files = Valle.gen()
        while True:
            try:
                file = next(files)
                header, data, name = Valle.read_file(file)
                mw, m0, t_m, f_m, obs_rupture, x_m, m0_acc_2sec, r_t = self.main(header=header, data=data)
                self.dict_events[name] = (mw, m0, t_m, f_m, obs_rupture, x_m, m0_acc_2sec, r_t)
            except StopIteration:
                break
        if args.database:
            self.databasefigure()
        if args.stf:
            self.stfigure()

    def gen():
        """
        creates iterator object with SCARDEC files
        """
        files = glob.glob('Valle2021/fctop*')
        return iter(files)

    def read_file(file):
        """
        reads event, time by time
        :return: header, data, event's name
        """
        lines = []
        data = []
        with open(f'{file}', 'r') as f:
            for line in f.readlines(60):
                lines.append(line.rstrip())
                header = [float(j) for i in [x.split() for x in lines] for j in i]
            f.seek(80)
            lst = [x.split() for x in f.readlines()]
            for line in [list(map(float, sublist)) for sublist in lst]:
                if len(line) >= 2:
                    data.insert(-1, line)
                else:
                    pass
        return header, data, f.name

    def read_columns(self):
        """
        read fig.txt columns
        :return: list of lists of MORSM data
        """
        lines = []
        with open(f'fig.txt', 'r') as f:
            for line in f.readlines():
                lines.append(line.split()[2:4])
        data = [list(map(float, sublist)) for sublist in lines]
        return data

    def moment2accumulatedmoment(self):
        data = self.read_columns()
        data.sort(key=lambda x: x[0])
        moment = []
        time = []
        for item in data:
            moment.append(item[1])
            time.append(item[0])
        moment = list(itertools.accumulate(moment))
        return time, moment, list(zip(time, moment))

    def stfunction(self):
        time, moment, _ = self.moment2accumulatedmoment()
        resmapledtime = np.linspace(min(time), max(time), 50)
        itermoment = np.interp(resmapledtime, time, moment)
        stf = np.gradient(itermoment, resmapledtime[1] - resmapledtime[0])
        return resmapledtime, itermoment, stf, list(zip(resmapledtime, stf))

    def stfigure(self):

        resmapledtime, itermoment, stf, _ = self.stfunction()
        fig, (ax, ax2) = plt.subplots(2, 1, sharex=True)
        ax.plot(resmapledtime, itermoment, 'rx-')
        ax.set_ylabel(r'$cumulative\,\,seismic\,\,moment,\,\,Nm$')
        ax2.plot(resmapledtime, stf, label='Source Time Function (STF)')
        ax2.legend()
        ax2.set_xlabel(r'$Time\,\,since\,\,OT,\,\,sec$')
        ax2.set_ylabel(r'$Moment\,\,rate,\,\,Nm/sec$')
        plt.show()

    def headerparams(self, header):
        mw = header[10]
        m0 = header[9]
        return mw, m0

    def two_sec(data):
        for line in data:
            if line[0] >= 2:
                return line
            else:
                None

    def typical_rup(self, header=None, m0=None):

        if header is not None:
            _, m0 = self.headerparams(header)
            return 10 ** (0.308 * np.log10(m0) - 4.8375)
        elif m0 is not None:
            return 10 ** (0.308 * np.log10(m0) - 4.8375)

    def stfmaxvalues(self, data):
        try:
            maxmomentrate = max(data, key=lambda x: x[1])
            t_m = maxmomentrate[0]
            f_m = maxmomentrate[1]
            return t_m, f_m
        except IndexError:
            return None, None

    def calcrupruretime(self, data):
        try:
            return list(filter(lambda x: (x[1] > 0), data))[-1][0]
        except IndexError:
            return None

    def stfsymmetry(self, t_m, obs_rupture):

        try:
            return (t_m / obs_rupture) * 100
        except TypeError:
            return None

    def calc_accmomentrate(self, data):
        try:
            return Valle.two_sec(data=data)[1] / 2
        except IndexError:
            return None

    def meier(self, obs_rupture, header=None, m0=None):

        if header is not None:
            try:
                typ_rupture = self.typical_rup(header)
                return (obs_rupture / typ_rupture) * 100
            except TypeError:
                return None

        elif m0 is not None:
            try:
                typ_rupture = self.typical_rup(m0=m0)
                return (obs_rupture / typ_rupture) * 100
            except TypeError:
                return None

    def main(self, header, data):
        mw, m0 = self.headerparams(header=header)
        t_m, f_m = self.stfmaxvalues(data=data)
        obs_rupture = self.calcrupruretime(data=data)
        x_m = self.stfsymmetry(t_m, obs_rupture=obs_rupture)
        m0_acc_2sec = self.calc_accmomentrate(data=data)
        r_t = self.meier(obs_rupture=obs_rupture, header=header)
        return mw, m0, t_m, f_m, obs_rupture, x_m, m0_acc_2sec, r_t

    def colorcondition(self, v):
        color = [0 if t_m <= 2 else r_t for t_m, r_t in zip(v[2], v[-1])]
        return color

    def sizecondition(self, v):
        size = [1 if t_m <= 2 else 50 for t_m in v[2]]
        return np.array(size)

    def transcondition(self, v):
        return np.array([1 if t_m <= 2 else 0.2 for t_m in v[2]])

    def arraylike(self, v):
        return np.array(v[-1])

    def databasefigure(self):
        v = list(zip(*self.dict_events.values()))
        color = self.colorcondition(v)
        size = self.sizecondition(v)
        trans = self.transcondition(v)
        r_t = self.arraylike(v)
        fig, (ax, ax2) = plt.subplots(1, 2, figsize=(20, 7))
        cm_ax = plt.cm.get_cmap('jet')
        cm_ax2 = plt.cm.get_cmap('jet')
        ax2.set_yscale('log')
        ax.set_yscale('log')
        ax.set_xlabel(r'$Mw, Nm$')
        ax.set_ylabel(r'$Observed\,\,rupture\,\,time - T_r,\,\,sec$')
        ax2.set_xlabel(r'$Mw ,Nm$')
        ax2.set_ylabel(r'$\ddot M_0 ^2,\,\, Nm/S^2$')

        # Global params from SCARDEC database
        ax.scatter(v[0], v[4], c=r_t, vmin=50, vmax=150,
                   alpha=0.2, edgecolors='k', cmap=cm_ax)
        sc = ax2.scatter(v[0], v[6], c=color, vmin=50, vmax=150,
                         edgecolors='k', alpha=trans, s=size, cmap=cm_ax2)

        # MORSM params
        _, _, _, data = self.stfunction()
        t_m, _ = self.stfmaxvalues(data=data)
        mw = params['EveMag']
        obs_rupture, accumoment = (data[-1][0],
                                   data[-1][1])
        m0_acc_2sec = self.calc_accmomentrate(data=data)
        r_t = self.meier(obs_rupture=obs_rupture, m0=accumoment)
        ax.scatter(mw, obs_rupture, c=r_t, marker='s',
                   s=80, vmin=50, vmax=150, edgecolors='white', cmap=cm_ax)
        ax2.scatter(mw, m0_acc_2sec, c='k' if t_m <= 2 else r_t, marker='s',
                    s=80, vmin=50, vmax=150, edgecolors='white', cmap=cm_ax2)
        cbar = fig.colorbar(sc, ax=ax2, pad=0.1)
        cbar.set_label(r'$r_t$ [%]')
        plt.show()


if __name__ == '__main__':
    purge('.', "*.txt")
    slipmodel = MORSM(args=args)
    slipmodel.run()
    database = Valle(args=args)
    database.run()
