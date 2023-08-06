"""
Copyright 2022 Dr. David Woodburn

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
--------------------------------------------------------------------------------
This library is designed to read version 2.11 RINEX navigation ('N') and
observation ('O') files, specifically for GPS ('G') system data.

Reading Data
------------
First import the library::

    import rnx

To read a RINEX file, call the `read` function passing the name of the file::

    nav = rnx.read("ohdt0710.22n")
    obs = rnx.read("ohdt0710.22o")

The type of file (navigation or observation) is determined automatically by the
first line of file, not the extension.  You can also read both a navigation file
and its corresponding observation file in one command::

    nav, obs = rnx.read("ohdt0710.22n", "ohdt0710.22o")

This has the added advantage of mapping the ephemeris data from the navigation
object to the corresponding moments in time and space vehicles of the
observation object.  It creates a new attribute in the observation object called
`ephs`.

Navigation Objects
------------------
The navigation (`nav`) object has three main attributes: the array of times of
clock `t_oc` in GPS week seconds, the array of PRN numbers for all GPS space
vehicles found in the navigation file, and the matrix of ephemerides `ephs`
corresponding to each pairing of time and PRN.  The relationship of these three
attributes can be visualized as follows::

            .--------------.
            |    |    |    | prns
            '--------------'
    .----.  .--------------.
    |    |  |    |    |    |
    |----|  |----|----|----|
    |    |  |    |    |    |
    |----|  |----|----|----|
    |    |  |    |    |    |
    '----'  '--------------'
     t_oc                   ephs

Not all elements of the `ephs` matrix are populated.  In such cases, the value
of that element of the matrix is `None`.

Suppose we wish to get the ephemeris for the 3rd space vehicle at the first
moment in time.  Then we would do ::

    t = nav.t[0]
    prn = nav.prns[2]
    eph = nav.ephs[0, 2]

The attributes of eph are listed in the EphG class.  As an example, if we wanted
to get the square root of the orbit semi-major axis radius, we would do ::

    eph.sqrtA

The navigation object has an additional property which stores the date and time
stamp of the beginning of the GPS week corresponding to the first record in the
file: `ts_bow`.  So, if we wanted to get the timestamp of the kth moment in
time, we would do ::

    ts = nav.ts_bow + datetime.timedelta(seconds=nav.t_oc[k])

Observation Objects
-------------------
The observation (`obs`) objects are organized in a manner similar to navigation
objects.  The arrays of receiver times `t` in GPS week seconds and event flags
`events` have as many elements as there are rows in any of the observation
matrices and the arrays of space vehicle names `svs`, system letters `sys`, and
space vehicle numbers `prns` have as many elements as there are columns in the
observation matrices::

                  .--------------.
                  |    |    |    | sys
                  :==============:
                  |    |    |    | prns
                  :==============:
                  |    |    |    | svs
                  '--------------'
    .----..----.  .--------------.
    |    ||    |  |    |    |    |
    |----||----|  |----|----|----|
    |    ||    |  |    |    |    |
    |----||----|  |----|----|----|
    |    ||    |  |    |    |    |
    '----''----'  '--------------'
      t   events                   C1, L2, D5, etc.

As an example, GPS satellite 5 would have a `sys` value of 'G', a `prns` value
of 5, and a `svs` value of "G05".  You can find the column index of a space
vehicle by name with the `sv_ind` dictionary::

    j = obs.sv_ind["G05"]

A RINEX observation file does not necessarily hold every possible type of
observation.  The types are labeled with a letter and a frequency band number.
The possible band numbers are 1, 2, 5, 6, 7, and 8.  The possible letters are ::

    Letter | Meaning           | Units
    ------ | ----------------- | ------
    'C'    | C/A pseudorange   | m
    'P'    | P(Y) pseudorange  | m
    'L'    | Carrier phase     | cycles
    'D'    | Doppler frequency | Hz
    'S'    | Signal strength   | dB-Hz

So, to access the C/A pseudorange from the L1 frequency of the jth space vehicle
at the kth moment in time, we would do ::

    rho = obs.C1[k, j]

Observation types which are no where defined within the RINEX file will still
exist as attributes of the observation object but will have a value of `None`.

To see if a space vehicle has any observation data at a given moment in time,
we can use the `is_vis` matrix::

    obs.is_vis[k, j]

This is a matrix of boolean values (`True` or `False`).  Very similar to this,
the `vis_prn` matrix is `NaN` wherever `is_vis` is `False` and is equal to the
PRN of the space vehicle wherever `is_vis` is `True`.  So, we could plot the
visibility of space vehicles by PRN with ::

    import matplotlib.pyplot as plt
    plt.plot(obs.t, obs.vis_prn)

Like with the navigation object, we can get the timestamp of the kth moment in
time by ::

    ts = obs.ts_bow + datetime.timedelta(seconds=obs.t[k])

When a navigation file is read in the same command as an observation file, the
observation object will get an additional attribute called `ephs`.  So, to get
the `C1` pseudorange and corresponding ephemeris for space vehicle `j` at time
`k`, we would do ::

    C1 = obs.C1[k, j]
    eph = obs.ephs[k, j]

Additional attributes are described in the Obs class.

Finding Data
------------
Some sites from which RINEX files can be downloaded for free are ::

    https://geodesy.noaa.gov/UFCORS/
    https://gssc.esa.int/portal/
"""

__author__ = "David Woodburn"
__credits__ = []
__license__ = "MIT"
__date__ = "2022-05-06"
__maintainer__ = "David Woodburn"
__email__ = "david.woodburn@icloud.com"
__status__ = "Development"

import datetime
import copy
import os
import numpy as np

# constants (from IS-GPS-200M)
c = 299792458.0             # speed of light [m/s] (p. 98)
F1 = 1575.42e6              # L1 carrier frequency for GPS [Hz] (p. 14)
F2 = 1227.6e6               # L2 carrier frequency for GPS [Hz] (p. 14)
PI = 3.1415926535898        # pi as defined for GPS calculations (p. 109)
W_IE = 7.2921151467e-5      # sidereal Earth rate [rad/s] (p. 106)


class EphG:
    """
    A class for storing the ephemeris data of a GPS space vehicle for a
    particular moment in time.

    Attributes
    ----------
    prn : int
        The pseudorandom noise value.
    t_oc : float
        Time of clock since start of the GPS week [s].
    t_oe : float
        Time of ephemeris since start of the GPS week [s].
    t_sv : float
        Time of transmission since start of the GPS week [s].
    a_f0 : float
        Clock bias correction coefficient [s].
    a_f1 : float
        Clock drift [s/s].
    a_f2 : float
        Clock drift rate [s/s^2].  It is often just zero.
    T_GD : float
        Group delay differential [s].
    T_fit : float, default 14400.0
        Fit interval [s].
    sqrtA : float
        Square root of orbit semi-major axis radius [sqrt(m)].
    M_0 : float
        Mean anomaly at time of ephemeris, `t_oe`, [rad].
    Delta_n : float
        Mean motion correction [rad/s].
    e : float
        Orbit eccentricity [ND].
    omega : float
        Argument of perigee [rad].
    i_0 : float
        Inclination angle at time of ephemeris, `t_oe`, [rad].
    Di : float
        Rate of inclination [rad/s].
    Omega_0 : float
        Longitude of ascending node at the beginning of the GPS week [rad].
    DOmega : float
        Rate of right ascension [rad/s].
    C_uc : float
        Argument of latitude cosine factor [rad].
    C_us : float
        Argument of latitude sine factor [rad].
    C_rc : float
        Orbit radius cosine factor[m].
    C_rs : float
        Orbit radius sine factor[m].
    C_ic : float
        Inclination angle cosine factor [rad].
    C_is : float
        Inclination angle sine factor [rad].
    WN : int
        Week number [wk].
    health : int
        Health flag.
    acc : float
        Accuracy of space vehicle [m].
    IODE : int
        Issue of data, ephemeris [counter].
    IODC : int
        Issue of data, clock [counter].
    cL2 : float
        Codes on L2 channel.
    pL2 : float
        P data flag on L2 channel.
    """

    def __init__(self):
        self.prn = None             # pseudorandom noise value

        self.t_oc = None            # time of clock since week start [s]
        self.t_oe = None            # time of ephemeris since week start [s]
        self.t_sv = None            # time of transmission since week start [s]
        self.a_f0 = None            # clock bias correction coefficient [s]
        self.a_f1 = None            # clock drift [s/s]
        self.a_f2 = None            # clock drift rate [s/s^2]
        self.T_GD = None            # group delay differential [s]
        self.T_fit = None           # fit interval [s]

        self.sqrtA = None           # sqrt of orbit semi-major axis [sqrt(m)]
        self.M_0 = None             # mean anomaly at t_oe [rad]
        self.Delta_n = None         # mean motion correction [rad/s]
        self.e = None               # orbit eccentricity [ND]
        self.omega = None           # argument of perigee [rad]
        self.i_0 = None             # inclination angle at t_oe [rad]
        self.Di = None              # rate of inclination [rad/s]
        self.Omega_0 = None         # lon. of ascending node at ts_bow [rad]
        self.DOmega = None          # rate of right ascension [rad/s]

        self.C_uc = None            # argument of latitude cosine factor [rad]
        self.C_us = None            # argument of latitude sine factor [rad]
        self.C_rc = None            # orbit radius cosine factor[m]
        self.C_rs = None            # orbit radius sine factor[m]
        self.C_ic = None            # inclination angle cosine factor [rad]
        self.C_is = None            # inclination angle sine factor [rad]

        self.WN = None              # week number [wk]
        self.health = None          # health flag
        self.acc = None             # accuracy of space vehicle [m]

        self.IODE = None            # issue of data, ephemeris [counter]
        self.IODC = None            # issue of data, clock [counter]
        self.cL2 = None             # codes on L2 channel
        self.pL2 = None             # P data flag on L2 channel


class NavG:
    """
    Class for creating RINEX GPS navigation objects.

    Attributes
    ----------
    ts_bow : datetime.datetime
        Date and timestamp of the beginning of the week relative to the earliest
        observation in the file.
    len : int
        Number of points in time.
    t_oc : (K,) float np.ndarray
        Array of K time of clock values since beginning of week in seconds.
    prns : (J,) int np.ndarray
        Array of J space vehicle pseudorandom noise values.
    ephs : (K, J) EphG np.ndarray
        A matrix of EphG objects, each storing an ephemeris data set for a
        particular moment in time and space vehicle.  If there is no data for
        the given space vehicle at the given time, the value will be `None`.
    """

    def __init__(self, file_name):
        """
        Read a navigation RINEX file into a NavG object.

        Parameters
        ----------
        file_name : str
            Name of navigation file, including extension.

        Returns
        -------
        self : NavG
            GPS navigation object.
        """

        # function to parse datetime stamp
        def parse_datetime(line):
            """
            Parse the date and time of a GPS navigation epoch.
            """
            year = int(line[3:5])
            year += 2000 if year < 80 else 1900
            t_stamp = datetime.datetime(year,                   # year
                    int(line[6:8]),   int(line[9:11]),          # M, d
                    int(line[12:14]), int(line[15:17]),         # h, m
                    int(line[18:20]), int(line[21])*100000)     # s, us
            return t_stamp

        def parse_3(line):
            """
            Parse one line into three values.
            """
            if not line[22:41].isspace():
                b = float(line[22:37] + 'e' + line[38:41])
            else:
                b = 0.0
            if not line[41:60].isspace():
                c = float(line[41:56] + 'e' + line[57:60])
            else:
                c = 0.0
            if not line[60:79].isspace():
                d = float(line[60:75] + 'e' + line[76:79])
            else:
                d = 0.0
            return b, c, d

        def parse_4(line):
            """
            Parse one line into four values.
            """
            if not line[3:22].isspace():
                a = float(line[3:18] + 'e' + line[19:22])
            else:
                a = 0.0
            b, c, d = parse_3(line)
            return a, b, c, d

        def parse_2(line):
            """
            Parse one line into two values.
            """
            if not line[3:22].isspace():
                a = float(line[3:18] + 'e' + line[19:22])
            else:
                a = 0.0
            if not line[22:41].isspace():
                b = float(line[22:37] + 'e' + line[38:41])
            else:
                b = 0.0
            return a, b

        # constants
        SPACE_SIZE = 1024

        # states
        STATE_INIT = 0              # initial state
        STATE_HEADER = 1            # looking for header values
        STATE_EPOCH = 2             # after header, expecting new epoch
        STATE_ORBITS = 3            # after header, reading orbital data
        state = STATE_INIT

        # file-level variables
        version = 0.0               # 2.11, 3.00, 3.01, etc.
        file_type = ''              # one of O, N, M, G, L, H, B, C, S
        ts_bow = None               # timestamp of beginning of week
        n_line = 0                  # RINEX file line number (base 1)
        t_oc = None                 # array of times of ephemeris [s]
        prns = None                 # space vehicle PRN for each epoch
        eph_list = None             # list of EphG objects
        list_space = SPACE_SIZE     # rows allocated to `eph_list` list
        list_rows = 0               # rows used in `eph_list` list

        # epoch-level variables
        ts_epoch = None             # timestamp of an epoch
        orbit_set = 0               # orbital set counter

        # Check the input.
        if not isinstance(file_name, str) or not os.path.exists(file_name):
            raise Exception("rnx: nonexistent navigation file!")

        # Open the file.
        file = open(file_name, "r")

        # Read each line of the file.
        for line in file:
            # Increment the RINEX file line number.
            n_line += 1

            # Remove the newline character and pad with spaces to 80 chars.
            line = line.rstrip().ljust(80)

            # Get the label.
            label = line[60:80]

            # State machine
            if state == STATE_INIT:
                if label != "RINEX VERSION / TYPE":
                    raise Exception("rnx: expected version in first line!")

                # RINEX version number
                version = float(line[0:9])
                if version != 2.11:
                    raise Exception("rnx: NavG can only process version 2.11!")

                # file-type letter: 'O', 'N', 'M', 'G', 'L', 'H', 'B', 'C', 'S'
                file_type = line[20]
                if (file_type != 'N'):
                    raise Exception("rnx: NavG can only read navigation files!")

                state = STATE_HEADER
            elif state == STATE_HEADER:
                if label == "END OF HEADER       ":
                    # Initialize the time and prn arrays and the ephemeris list.
                    t_oc = np.zeros(list_space, dtype=float)
                    prns = np.zeros(list_space, dtype=int)
                    eph_list = [None]*list_space

                    state = STATE_EPOCH
                else:
                    state = STATE_HEADER
            elif state == STATE_EPOCH:
                if label[0].isalpha() or label[0] == '#':
                    continue

                # Create new navigation object.
                eph = EphG()

                # pseudorandom noise value and timestamp of epoch (clock)
                eph.prn = int(line[0:3])
                ts_epoch = parse_datetime(line)

                # Get the timestamp of the beginning of the week.
                if ts_bow is None:
                    day_of_week = ts_epoch.isoweekday() % 7
                    ts_bow = ts_epoch - datetime.timedelta(days=day_of_week)
                    ts_bow = ts_bow.replace(hour=0, minute=0, second=0,
                            microsecond=0)

                # Get the time of clock relative to start of week.
                eph.t_oc = (ts_epoch - ts_bow).total_seconds()

                # Read clock bias, drift, and drift rate.
                eph.a_f0, eph.a_f1, eph.a_f2 = parse_3(line)

                state = STATE_ORBITS
            elif state == STATE_ORBITS:
                if label[0].isalpha() or label[0] == '#':
                    continue

                # Parse the numbers depending on the orbital set counter.
                orbit_set += 1
                if orbit_set == 1:
                    IODE, eph.C_rs, eph.Delta_n, eph.M_0 = parse_4(line)
                    eph.IODE = int(IODE)
                elif orbit_set == 2:
                    eph.C_uc, eph.e, eph.C_us, eph.sqrtA = parse_4(line)
                elif orbit_set == 3:
                    eph.t_oe, eph.C_ic, eph.Omega_0, eph.C_is = parse_4(line)
                elif orbit_set == 4:
                    eph.i_0, eph.C_rc, eph.omega, eph.DOmega = parse_4(line)
                elif orbit_set == 5:
                    eph.Di, eph.cL2, WN, eph.pL2 = parse_4(line)
                    eph.WN = int(WN)
                elif orbit_set == 6:
                    eph.acc, health, eph.T_GD, IODC = parse_4(line)
                    eph.health = int(health)
                    eph.IODC = int(IODC)
                elif orbit_set == 7:
                    eph.t_sv, T_fit = parse_2(line)
                    if T_fit > 0.0:
                        eph.T_fit = 3600.0*T_fit # Scale to seconds from hours.
                    else:
                        eph.T_fit = 4*3600.0 # Default to four hours.

                    # Add rows to the list space if needed.
                    if list_rows + 1 >= list_space:
                        t_oc = np.concatenate((t_oc,
                                np.zeros(SPACE_SIZE, dtype=float)))
                        prns = np.concatenate((prns,
                                np.zeros(SPACE_SIZE, dtype=int)))
                        eph_list.extend([None]*SPACE_SIZE)
                        list_space += SPACE_SIZE

                    # Store data from this epoch and PRN.
                    t_oc[list_rows] = eph.t_oc
                    prns[list_rows] = eph.prn
                    eph_list[list_rows] = copy.copy(eph)
                    list_rows += 1

                    # Reset the orbital set counter.
                    orbit_set = 0
                    state = STATE_EPOCH

        # Close the file.
        file.close()

        # Drop the extra space.
        t_oc = t_oc[:list_rows]
        prns = prns[:list_rows]
        eph_list = eph_list[:list_rows]

        # Build navigation list of lists of EphG objects.
        t_oc, kk = np.unique(t_oc, return_inverse=True)
        prns, jj = np.unique(prns, return_inverse=True)
        K = len(t_oc)
        J = len(prns)
        M = np.empty((K, J), dtype=EphG)
        M[kk, jj] = eph_list

        # Load properties of object.
        self.ts_bow = ts_bow
        self.len = len(t_oc)
        self.t_oc = t_oc.copy()
        self.prns = prns.copy()
        self.ephs = M.copy()


class Obs:
    """
    Class for creating RINEX observation objects.

    Attributes
    ----------
    pos : (3,) float np.ndarray
        ECEF position coordinates from the RINEX file.
    tz_approx : int
        Approximate time zone offset based only on the longitude [hr].
    ts_bow : datetime.datetime
        Date and timestamp of the beginning of the week based on the earliest
        observation in the file.
    types : (I,) str np.ndarray
        Array of `I` observation type names: "L1", "C5", "S2", etc.
    len : int
        Number of points in time.
    t : (K,) float np.ndarray
        Array of K receiver time values since beginning of GPS week in seconds.
    T_os : (K,) float np.ndarray
        Array of K receiver clock offsets in seconds.
    events : (K,) int np.ndarray
        Event flags (integers from 0 to 6), a row per moment in time.
    sys : (J,) str np.ndarray
        Array of `J` space vehicle system letters: 'G' for GPS, 'R' for GLONASS,
        and 'E' for Galileo.
    prns : (J,) int np.ndarray
        Array of `J` space vehicle pseudorandom noise values starting from 1.
    svs : (J,) str np.ndarray
        Array of `J` space vehicle names: the system letters (`sys`) with their
        pseudorandom noise values (`prns`).
    sv_ind : (J,) int dict
        Dictionary for all `J` space vehicles.  The keys are the space vehicle
        names (`svs`) and the values are the column indices to the observation
        matrices (L1, C5, S2, etc.).
    n_E : int np.ndarray
        Array of column indices to the observation matrices, which columns
        correspond to the Galileo system space vehicles.  If none of the space
        vehicles are part of this system, then the array will be empty.
    n_G : int np.ndarray
        Array of column indices to the observation matrices, which columns
        correspond to the GPS system space vehicles.  If none of the space
        vehicles are part of this system, then the array will be empty.
    n_R : int np.ndarray
        Array of column indices to the observation matrices, which columns
        correspond to the GLONASS system space vehicles.  If none of the space
        vehicles are part of this system, then the array will be empty.
    n_S : int np.ndarray
        Array of column indices to the observation matrices, which columns
        correspond to the geostationary system space vehicles.  If none of the
        space vehicles are part of this system, then the array will be empty.
    is_vis : (K, J) bool np.ndarray
        Matrix of boolean values indicating the visibility of the space vehicles
        with a row for each of the `K` moments in time and a column for each of
        the `J` space vehicles found in the file.
    vis_prn : (K, J) float np.ndarray
        Matrix of floats.  Where the given space vehicle (column) at the given
        moment in time (row) has any observation data, the PRN of the space
        vehicle as a float is provided.  Where the space vehicle has no data,
        NAN is provided.
    Cx : (K, J) float np.ndarray
        Possible matrix of C/A pseudoranges in meters from frequency band `x`
        with a row for each of the `K` moments in time and a column for each of
        the `J` space vehicles found in the file.
    Px : (K, J) float np.ndarray
        Possible matrix of P(Y) pseudoranges in meters from frequency band `x`
        with a row for each of the `K` moments in time and a column for each of
        the `J` space vehicles found in the file.
    Lx : (K, J) float np.ndarray
        Possible matrix of carrier-phase values in cycles from frequency band
        `x` with a row for each of the `K` moments in time and a column for each
        of the `J` space vehicles found in the file.
    Dx : (K, J) float np.ndarray
        Possible matrix of Doppler frequencies in Hz from frequency band `x`
        with a row for each of the `K` moments in time and a column for each of
        the `J` space vehicles found in the file.
    Sx : (K, J) float np.ndarray
        Possible matrix of signal strengths in dB-Hz from frequency band `x`
        with a row for each of the `K` moments in time and a column for each of
        the `J` space vehicles found in the file.

    Notes
    -----
    Some observation types are claimed to be observed in the header but have no
    actual data anywhere in the RINEX file.  Such observation types are defined
    as `None`.  Any observation types which are not actually observed in the
    file are defined as `None`.
    """

    def __init__(self, file_name):
        """
        Read an observation RINEX file into an Obs object.

        Parameters
        ----------
        file_name : str
            Name of observation file, including extension.

        Returns
        -------
        self : Obs
            Observation object.
        """

        # constants
        SPACE_SIZE = 1024
        FILLER = np.nan

        # states
        STATE_INIT = 0              # initial state
        STATE_HEADER = 1            # looking for header values
        STATE_MORE_TYPES = 2        # expecting more observation types
        STATE_EPOCH = 3             # after header, expecting new epoch
        STATE_MORE_SVS = 4          # expecting more SVs
        STATE_OBS = 5               # expecting observations in epoch
        state = STATE_INIT

        # file-level variables
        version = 0.0               # 2.11, 3.00, 3.01, etc.
        file_type = ''              # one of O, N, M, G, L, H, B, C, S
        system = ''                 # ' ', 'G', 'R', 'S', 'E', or 'M'
        types_cnt = 0               # number of observation types in file
        types_list = None           # array of observation types: "L1", etc.
        pos = np.zeros(3)           # calculated ECEF position of receiver
        ts_bow = None               # timestamp of beginning of week
        n_line = 0                  # RINEX file line number (base 1)
        t = None                    # times of week [s] for each epoch
        T_os = None                 # receiver clock offsets [s] for each epoch
        events = None               # event flags for each epoch
        svs = None                  # space vehicle labels for each epoch
        data = None                 # matrix of observations
        data_space = SPACE_SIZE     # rows allocated to `data` matrix
        data_rows = 0               # rows used in `data` matrix

        # epoch-level variables
        ts_epoch = None             # timestamp of an epoch
        T_os_epoch = 0.0            # receiver clock offset [s]
        types_epoch_left = 0        # observation types left for an epoch
        event_epoch = 0             # the epoch flag (integer from 0 to 6)
        svs_epoch_cnt = 0           # number of space vehicles in epoch
        svs_epoch_list = [0]*99     # list of space vehicles in epoch
        svs_epoch_left = 0          # space vehicles left to read in epoch
        obs_epoch_cnt = 0           # number of observations in epoch
        obs_epoch_list = [0]*26*98  # list of observations in epoch
        obs_epoch_left = 0          # observations left in epoch

        # Check the input.
        if not isinstance(file_name, str) or not os.path.exists(file_name):
            raise Exception("rnx: nonexistent observation file!")

        # Open the file.
        file = open(file_name, "r")

        # Read each line of the file.
        for line in file:
            # Increment the RINEX file line number.
            n_line += 1

            # Remove the newline character and pad with spaces to 80 chars.
            line = line.rstrip().ljust(80)

            # Get the label.
            label = line[60:80]

            # State machine
            if state == STATE_INIT:
                if label != "RINEX VERSION / TYPE":
                    raise Exception("rnx: expected version in first line!")

                # RINEX version number
                version = float(line[0:9])
                if version != 2.11:
                    raise Exception("rnx: Obs can only process version 2.11!")

                # file-type letter: 'O', 'N', 'M', 'G', 'L', 'H', 'B', 'C', 'S'
                file_type = line[20]
                if (file_type != 'O'):
                    raise Exception("rnx: Obs can only read observation files!")

                # system letter: ' ', 'G', 'R', 'S', 'E', or 'M'
                system = line[40]
                if (system != ' ') and (system != 'G') and (system != 'M'):
                    raise Exception("rnx: can only process GPS system!")

                state = STATE_HEADER
            elif state == STATE_HEADER:
                if label == "APPROX POSITION XYZ ":
                    pos[0] = float(line[0:14])
                    pos[1] = float(line[14:28])
                    pos[2] = float(line[28:42])
                    state = STATE_HEADER
                elif label == "# / TYPES OF OBSERV ":
                    if types_cnt != 0:
                        raise Exception("rnx: observations over-defined!" +
                                "  line %d" % (n_line))

                    # Read the observation types.
                    types_cnt = int(line[0:6])
                    types_list = np.empty(types_cnt, dtype="U2")
                    N = types_cnt if types_cnt < 9 else 9
                    for n in range(N):
                        m = 10 + n*6
                        types_list[n] = line[m:(m + 2)]

                    # Initialize time, svs, and observation data matrix.
                    t = np.zeros(data_space, dtype=float)
                    T_os = np.zeros(SPACE_SIZE, dtype=float)
                    events = np.zeros(data_space, dtype=int)
                    svs = np.empty(data_space, dtype="U3")
                    data = np.full((data_space, types_cnt), FILLER)

                    # Decide if more observation types need to be read.
                    if types_cnt <= 9:
                        state = STATE_HEADER
                    else:
                        types_epoch_left = types_cnt - 9
                        state = STATE_MORE_TYPES
                elif label == "TIME OF FIRST OBS   ":
                    # Get the timestamp of the beginning of the week.
                    t_start = datetime.datetime(
                            int(line[2:6]), int(line[10:12]),   # year, month
                            int(line[16:18]), int(line[22:24]), # day, hour
                            int(line[28:30]), int(line[30:35]), # minute, sec.
                            int(line[36:43])//10)               # microsecond
                    day_of_week = t_start.isoweekday() % 7
                    ts_bow = t_start - datetime.timedelta(days=day_of_week)
                    ts_bow = ts_bow.replace(hour=0, minute=0, second=0,
                            microsecond=0)
                    state = STATE_HEADER
                elif label == "END OF HEADER       ":
                    state = STATE_EPOCH
                else:
                    state = STATE_HEADER
            elif state == STATE_MORE_TYPES:
                # Read more observation type labels.
                N = types_epoch_left if types_epoch_left < 9 else 9
                for n in range(N):
                    m = 10 + n*6
                    types_list[types_cnt - types_epoch_left] = line[m:(m + 2)]
                    types_epoch_left -= 1

                # Decide if more observation type labels need to be read.
                if types_epoch_left > 0:
                    state = STATE_MORE_TYPES
                else:
                    state = STATE_HEADER
            elif state == STATE_EPOCH:
                if label[0].isalpha() or label[0] == '#':
                    state = STATE_EPOCH
                    continue

                # Read the date and time as a timestamp.
                year = int(line[1:3])
                year += 2000 if year < 80 else 1900
                ts_epoch = datetime.datetime(year,                  # year
                        int(line[4:6]),   int(line[7:9]),           # M, d
                        int(line[10:12]), int(line[13:15]),         # h, m
                        int(line[15:18]), int(line[19:26])//10)     # s, us

                # Get the event flag (integer from 0 to 6).
                if line[28] == ' ':
                    event_epoch = 0
                else:
                    event_epoch = int(line[28])

                # Get the number of space vehicles in this epoch.
                svs_epoch_cnt = int(line[29:32])
                svs_epoch_left = svs_epoch_cnt

                # Prepare for reading observations.
                obs_epoch_cnt = svs_epoch_cnt*types_cnt
                obs_epoch_left = obs_epoch_cnt

                # Read the space vehicle PRNs.
                N = svs_epoch_cnt if svs_epoch_cnt < 12 else 12
                for n in range(N):
                    m = 32 + n*3 # every three characters
                    if line[m] == ' ':
                        svs_epoch_list[n] = 'G' + line[(m + 1):(m + 3)]
                    else:
                        svs_epoch_list[n] = line[m:(m + 3)]
                    svs_epoch_left -= 1

                # Receiver clock offset [s]
                if line[68:80].isspace():
                    T_os_epoch = 0.0
                else:
                    T_os_epoch = float(line[68:80])

                # Decide if more space vehicle PRNs need to be read.
                if svs_epoch_left > 0:
                    state = STATE_MORE_SVS
                else:
                    state = STATE_OBS

                # NOTE Receiver clock offset is ignored.
            elif state == STATE_MORE_SVS:
                # Read more space vehicle PRNs.
                N = svs_epoch_left if svs_epoch_left < 12 else 12
                for n in range(N):
                    m = 32 + n*3 # every three characters
                    n_sv = svs_epoch_cnt - svs_epoch_left
                    if line[m] == ' ':
                        svs_epoch_list[n_sv] = 'G' + line[(m + 1):(m + 3)]
                    else:
                        svs_epoch_list[n_sv] = line[m:(m + 3)]
                    svs_epoch_left -= 1

                # Decide if more space vehicle PRNs need to be read.
                if svs_epoch_left > 0:
                    state = STATE_MORE_SVS
                else:
                    state = STATE_OBS

            elif state == STATE_OBS:
                if label[0].isalpha() or label[0] == '#':
                    raise Exception("rnx: expected observations!  line %d" %
                            (n_line))

                # Read the observations.
                N = obs_epoch_left if obs_epoch_left < 5 else 5
                for n in range(N):
                    m = n*16
                    n_obs = obs_epoch_cnt - obs_epoch_left
                    obs_str = line[m:(m + 14)]
                    if obs_str.isspace():
                        obs_epoch_list[n_obs] = FILLER
                    else:
                        obs_epoch_list[n_obs] = float(obs_str)
                    obs_epoch_left -= 1

                    # Break early.  Observations for a space vehicle start on a
                    # new line.
                    if (obs_epoch_cnt - obs_epoch_left) % types_cnt == 0:
                        break

                # Decide if more observations need to be read.
                if obs_epoch_left > 0:
                    state = STATE_OBS
                else:
                    # Add rows to the data space if needed.
                    if data_rows + svs_epoch_cnt >= data_space:
                        t = np.concatenate((t,
                                np.zeros(SPACE_SIZE, dtype=float)))
                        T_os = np.concatenate((T_os,
                                np.zeros(SPACE_SIZE, dtype=float)))
                        events = np.concatenate((events,
                                np.zeros(SPACE_SIZE, dtype=int)))
                        svs = np.concatenate((svs,
                                np.empty(SPACE_SIZE, dtype="U3")))
                        data = np.vstack((data,
                                np.full((SPACE_SIZE, types_cnt), FILLER)))
                        data_space += SPACE_SIZE

                    # Get the indices of the observations list.
                    ma = 0
                    mb = types_cnt

                    # Get the time of week for this set of observations.  The
                    # total_seconds method returns a floating-point value
                    # including microsecond precision.
                    t_rx_epoch = (ts_epoch - ts_bow).total_seconds()

                    # Store the time, space vehicle label, and observations.
                    for n_sv in range(svs_epoch_cnt):
                        t[data_rows] = t_rx_epoch
                        T_os[data_rows] = T_os_epoch
                        events[data_rows] = event_epoch
                        svs[data_rows] = svs_epoch_list[n_sv]
                        data[data_rows, :] = obs_epoch_list[ma:mb]
                        data_rows += 1
                        ma = mb
                        mb += types_cnt

                    # Resume looking for a new epoch.
                    state = STATE_EPOCH

        # Close the file.
        file.close()

        # Drop the extra space.
        t = t[:data_rows]
        T_os = T_os[:data_rows]
        events = events[:data_rows]
        svs = svs[:data_rows]
        data = data[:data_rows, :]

        # Remove unused observation types (columns of `data`).
        n_col_keep = ~np.all(np.isnan(data), axis=0)
        data = data[:, n_col_keep]
        types_list = types_list[n_col_keep]
        types_cnt = len(types_list)

        # Find the unique moments in time and the unique space vehicles.
        t, ii, kk = np.unique(t, return_index=True, return_inverse=True)
        svs, jj = np.unique(svs, return_inverse=True)
        K = len(t)
        J = len(svs)

        # Keep only one clock offset and event flag per moment in time.
        T_os = T_os[ii]
        events = events[ii]

        # Build objects with the observation data matrix, one object for each
        # type.  Build the visibility matrix.
        is_vis = np.full((K, J), False)
        for n_type in range(types_cnt):
            M = np.full((K, J), FILLER)
            M[kk, jj] = data[:, n_type]
            is_vis += ~np.isnan(M)
            setattr(self, types_list[n_type], M.copy())

        # Build the space vehicle dictionary.
        sv_ind = dict((svs[n], n) for n in range(J))

        # Parse the `svs` array into the system letter and pseudorandom noise.
        sys = np.array([sv[0] for sv in svs], dtype="U1")
        prns = np.array([int(sv[1:]) for sv in svs], dtype=int)

        # Build the prn visibility matrix.  It is the same as the visibility
        # matrix, except that instead of `False` it has FILLER, and instead of
        # `True` it has the space vehicle's number.
        vis_prn = np.full((K, J), FILLER)
        for j in range(J):
            vis_prn[is_vis[:, j], j] = float(prns[j])

        # Set all unused observation types to `None`.
        all_types = ["C1", "D1", "L1", "S1", "C2", "D2", "L2", "S2",
                "C5", "D5", "L5", "S5", "C6", "D6", "L6", "S6",
                "C7", "D7", "L7", "S7", "C8", "D8", "L8", "S8", "P1", "P2"]
        for type_str in all_types:
            if not hasattr(self, type_str):
                setattr(self, type_str, None)

        # Load remaining properties of object.
        self.pos = pos.copy()
        self.tz_approx = round(np.arctan2(pos[1], pos[0])*12/np.pi)
        self.ts_bow = ts_bow
        self.types = types_list.copy()
        self.len = len(t)
        self.t = t.copy()
        self.T_os = T_os.copy()
        self.events = events.copy()
        self.sys = sys.copy()
        self.prns = prns.copy()
        self.svs = svs.copy()
        self.sv_ind = sv_ind.copy()
        self.n_E = np.nonzero(sys == 'E')[0].copy()
        self.n_G = np.nonzero(sys == 'G')[0].copy()
        self.n_R = np.nonzero(sys == 'R')[0].copy()
        self.n_S = np.nonzero(sys == 'S')[0].copy()
        self.is_vis = is_vis.copy()
        self.vis_prn = vis_prn.copy()


def read(file_one, file_two=None, file_ref=None):
    """
    Read in RINEX data.

    Parameters
    ----------
    file_one : str
        Name of first RINEX file.  Can be a navigation or an observation file.
    file_two : str, default None
        Name of second RINEX file.  Can be a navigation or an observation file.
    file_ref : str, default None
        Name of reference RINEX observation file.

    Returns
    -------
    NavG or Obs objects corresponding to the order of the file names.
    """

    def get_file_type(file_name):
        """
        Open the RINEX file by name `file_name` and check the file type from the
        first line.  Options include ::

            O: Observation file
            N: GPS Navigation file
            M: Meteorological data file
            G: GLONASS Navigation file
            L: Future Galileo Navigation file
            H: Geostationary GPS payload nav mess file
            B: Geo SBAS broadcast data file
            C: Clock file
            S: Summary file (used e.g., by IGS, not a standard!)

        Returns
        -------
        file_type : str
            Letter of the file type.
        """

        file = open(file_name, "r")
        line = file.readline()
        line = line.rstrip().ljust(80)
        file.close()

        if line[60:80] != "RINEX VERSION / TYPE":
            raise Exception("rnx: expected version in first line!")
        file_type = line[20]

        return file_type

    def map_nav_to_obs(nav, obs):
        """
        Map the EphG navigation objects to the correct observations.  This function
        adds the attribute `ephs` to the Obs object.  An ephemeris fits the time
        period defined by the time of ephemeris, `t_oe`, +/- half of the fit
        interval, `T_fit`.  The closer ephemeris will be applied to the given space
        vehicle for the given observation time.  If no matching ephemeris data
        exists, the corresponding element of the `ephs` property matrix will be
        `None`.  The `ephs` matrix will have the same dimensions as any of the
        observation type matrices (e.g., C1, L1, P2, etc.).

        Parameters
        ----------
        nav : NavG
            GPS navigation object.
        obs : Obs
            Observation object.
        """

        # Get the times from the NavG and Obs objects.
        t_oc = nav.t_oc.copy()
        t = obs.t

        # Shift the copy of nav times if nav and obs do not share the same beginning
        # of week timestamp.
        if nav.ts_bow != obs.ts_bow:
            t_oc += (nav.ts_bow - obs.ts_bow).total_seconds()

        # Find the intersection of the two PRN arrays.
        obs_gps_prns = np.zeros(len(obs.prns), dtype=int)
        n_G = (obs.sys == 'G')
        obs_gps_prns[n_G] = obs.prns[n_G]
        prns, j_nav, j_obs = np.intersect1d(nav.prns, obs_gps_prns,
                return_indices=True)

        # Initialize the ephemeris mapping.
        setattr(obs, "ephs", np.empty((len(t), len(obs.prns)), dtype=EphG))

        # Check if there is no overlap.
        if (t_oc[0] - 3600 > t[-1]) or (t_oc[-1] + 3600 < t[0]):
            Warning("rnx: times of NavG and Obs data sets do not overlap.")
            return
        if len(prns) == 0:
            Warning("rnx: PRNs of NavG and Obs data sets do not overlap.")

        # For each PRN that matches,
        for j in range(len(prns)):
            # Initialize an array of time differences to a large number.
            del_t = np.full(len(t), 604800.0) # a week of seconds

            # For each moment in the nav time array,
            for k in range(len(t_oc)):
                # Get the ephemeris data for this space vehicle at this moment in
                # time.  Skip if there is no data.
                eph = nav.ephs[k, j_nav[j]]
                if eph is None:
                    continue

                # Get the beginning and ending of the fit interval.
                t_a = t_oc[k] - 0.5*eph.T_fit
                t_b = t_oc[k] + 0.5*eph.T_fit

                # Find the indices of the receiver's time array which fall withing
                # the fit interval.  Skip is there is no match.
                n_ab = np.nonzero((t >= t_a) * (t <= t_b))[0]
                if len(n_ab) == 0:
                    continue

                # Save this ephemeris data for those moments where the time fit is
                # the best.
                del_t_ab = np.abs(t_oc[k] - t[n_ab])
                is_better = (del_t_ab <= del_t[n_ab])
                obs.ephs[n_ab[is_better], j_obs[j]] = eph
                del_t[n_ab[is_better]] = del_t_ab[is_better]

        # TODO Maybe clear any ephemeris data for which there are no observations.

    def map_ref_to_obs(ref, obs):
        """
        Find the intersection of the `ref` and `obs` observation times and svs.
        Four new attributes are added to the Obs object::

            j_ref   array of indices to the intersected ref SV columns
            j_obs   array of indices to the intersected obs SV columns
            k_ref   array of indices to the intersected ref time rows
            k_obs   array of indices to the intersected obs time rows
        """

        svs, j_ref, j_obs = np.intersect1d(ref.svs, obs.svs,
                return_indices=True)
        t, k_ref, k_obs = np.intersect1d(ref.t, obs.t,
                return_indices=True)
        setattr(obs, "j_ref", j_ref)
        setattr(obs, "k_ref", k_ref)
        setattr(obs, "j_obs", j_obs)
        setattr(obs, "k_obs", k_obs)

    # Initialize the objects.
    nav = None
    obs = None
    ref = None

    # Read in file one.
    if not isinstance(file_one, str):
        raise Exception("rnx: file_one must be a string!")
    file_one_type = get_file_type(file_one)
    if file_one_type == 'N':
        nav = NavG(file_one)
    elif file_one_type == 'O':
        obs = Obs(file_one)

    # Read in file two.
    if file_two is not None:
        if not isinstance(file_two, str):
            raise Exception("rnx: file_two must be a string!")
        file_two_type = get_file_type(file_two)
        if file_two_type == 'N':
            if file_one_type == 'N':
                raise Exception("rnx: cannot read two navigation files!")
            nav = NavG(file_two)
        elif file_two_type == 'O':
            if file_one_type == 'O':
                raise Exception("rnx: cannot read two observation files!")
            obs = Obs(file_two)
        map_nav_to_obs(nav, obs)

    # Read in reference file.
    if file_ref is not None:
        if not isinstance(file_ref, str):
            raise Exception("rnx: file_ref must be a string!")
        file_ref_type = get_file_type(file_ref)
        if file_ref_type != 'O':
            raise Exception("rnx: reference file must be an observation type!")
        ref = Obs(file_ref)
        map_ref_to_obs(ref, obs)

    # Return the objects in the order the files were specified.
    if file_two is None:
        if file_ref is None:
            if nav is not None:
                return nav
            elif obs is not None:
                return obs
        else:
            if nav is not None:
                return nav, ref
            elif obs is not None:
                return obs, ref
    else:
        if file_ref is None:
            if file_one_type == 'N':
                return nav, obs
            else:
                return obs, nav
        else:
            if file_one_type == 'N':
                return nav, obs, ref
            else:
                return obs, nav, ref
