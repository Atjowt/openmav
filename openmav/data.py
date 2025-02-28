from ctypes import BigEndianStructure, c_int, c_uint, c_float, c_double

VERSION = 24
MAX_ENGINES = 4
MAX_WHEELS = 3
MAX_TANKS = 4

class FlightData(BigEndianStructure):

    @property
    def version(self) -> int: return self._version

    @property
    def longitude(self) -> float: return self._longitude

    @property
    def latitude(self) -> float: return self._latitude

    @property
    def altitude(self) -> float: return self._altitude

    @property
    def agl(self) -> float: return self._agl

    @property
    def phi(self) -> float: return self._phi

    @property
    def theta(self) -> float: return self._theta

    @property
    def psi(self) -> float: return self._psi

    @property
    def alpha(self) -> float: return self._alpha

    @property
    def beta(self) -> float: return self._beta

    @property
    def phidot(self) -> float: return self._phidot

    @property
    def thetadot(self) -> float: return self._thetadot

    @property
    def psidot(self) -> float: return self._psidot

    @property
    def vcas(self) -> float: return self._vcas

    @property
    def climb_rate(self) -> float: return self._climb_rate

    @property
    def v_north(self) -> float: return self._v_north

    @property
    def v_east(self) -> float: return self._v_east

    @property
    def v_down(self) -> float: return self._v_down

    @property
    def v_wind_body_north(self) -> float: return self._v_wind_body_north

    @property
    def v_wind_body_east(self) -> float: return self._v_wind_body_east

    @property
    def v_wind_body_down(self) -> float: return self._v_wind_body_down

    @property
    def A_X_pilot(self) -> float: return self._A_X_pilot

    @property
    def A_Y_pilot(self) -> float: return self._A_Y_pilot

    @property
    def A_Z_pilot(self) -> float: return self._A_Z_pilot

    @property
    def stall_warning(self) -> float: return self._stall_warning

    @property
    def slip_deg(self) -> float: return self._slip_deg

    @property
    def num_engines(self) -> int: return self._num_engines

    @property
    def eng_state(self) -> tuple: return tuple(self._eng_state)

    @property
    def rpm(self) -> tuple: return tuple(self._rpm)

    @property
    def fuel_flow(self) -> tuple: return tuple(self._fuel_flow)

    @property
    def fuel_px(self) -> tuple: return tuple(self._fuel_px)

    @property
    def egt(self) -> tuple: return tuple(self._egt)

    @property
    def cht(self) -> tuple: return tuple(self._cht)

    @property
    def mp_osi(self) -> tuple: return tuple(self._mp_osi)

    @property
    def tit(self) -> tuple: return tuple(self._tit)

    @property
    def oil_temp(self) -> tuple: return tuple(self._oil_temp)

    @property
    def oil_px(self) -> tuple: return tuple(self._oil_px)

    @property
    def num_tanks(self) -> int: return self._num_tanks

    @property
    def fuel_quantity(self) -> tuple: return tuple(self._fuel_quantity)

    @property
    def num_wheels(self) -> int: return self._num_wheels

    @property
    def wow(self) -> tuple: return tuple(self._wow)

    @property
    def gear_pos(self) -> tuple: return tuple(self._gear_pos)

    @property
    def gear_steer(self) -> tuple: return tuple(self._gear_steer)

    @property
    def gear_compression(self) -> tuple: return tuple(self._gear_compression)

    @property
    def cur_time(self) -> int: return self._cur_time

    @property
    def warp(self) -> int: return self._warp

    @property
    def visibility(self) -> float: return self._visibility

    @property
    def elevator(self) -> float: return self._elevator

    @property
    def elevator_trim_tab(self) -> float: return self._elevator_trim_tab

    @property
    def left_flap(self) -> float: return self._left_flap

    @property
    def right_flap(self) -> float: return self._right_flap

    @property
    def left_aileron(self) -> float: return self._left_aileron

    @property
    def right_aileron(self) -> float: return self._right_aileron

    @property
    def rudder(self) -> float: return self._rudder

    @property
    def nose_wheel(self) -> float: return self._nose_wheel

    @property
    def speedbrake(self) -> float: return self._speedbrake

    @property
    def spoilers(self) -> float: return self._spoilers

    _fields_ = [
        ('_version', c_uint), # increment when data values change
        ('_padding', c_uint), # padding

        # Positions
        ('_longitude', c_double), # geodetic (radians)
        ('_latitude', c_double), # geodetic (radians)
        ('_altitude', c_double), # above sea level (meters)
        ('_agl', c_float), # above ground level (meters)
        ('_phi', c_float), # roll (radians)
        ('_theta', c_float), # pitch (radians)
        ('_psi', c_float), # yaw or true heading (radians)
        ('_alpha', c_float), # angle of attack (radians)
        ('_beta', c_float), # side slip angle (radians)

        # Velocities
        ('_phidot', c_float), # roll rate (radians/sec)
        ('_thetadot', c_float), # pitch rate (radians/sec)
        ('_psidot', c_float), # yaw rate (radians/sec)
        ('_vcas', c_float), # calibrated airspeed
        ('_climb_rate', c_float), # feet per second
        ('_v_north', c_float), # north velocity in local/body frame, fps
        ('_v_east', c_float), # east velocity in local/body frame, fps
        ('_v_down', c_float), # down/vertical velocity in local/body frame, fps
        ('_v_wind_body_north', c_float), # north velocity in local/body frame
        ('_v_wind_body_east', c_float), # east velocity in local/body frame
        ('_v_wind_body_down', c_float), # down/vertical velocity in local/body

        # Accelerations
        ('_A_X_pilot', c_float), # X accel in body frame ft/sec^2
        ('_A_Y_pilot', c_float), # Y accel in body frame ft/sec^2
        ('_A_Z_pilot', c_float), # Z accel in body frame ft/sec^2

        # Stall
        ('_stall_warning', c_float), # 0.0 - 1.0 indicating the amount of stall
        ('_slip_deg', c_float), # slip ball deflection

        ('_num_engines', c_uint), # Number of valid engines
        ('_eng_state', c_uint * MAX_ENGINES), # Engine state (off, cranking, running)
        ('_rpm', c_float * MAX_ENGINES), # Engine RPM rev/min
        ('_fuel_flow', c_float * MAX_ENGINES), # Fuel flow gallons/hr
        ('_fuel_px', c_float * MAX_ENGINES), # Fuel pressure psi
        ('_egt', c_float * MAX_ENGINES), # Exhuast gas temp deg F
        ('_cht', c_float * MAX_ENGINES), # Cylinder head temp deg F
        ('_mp_osi', c_float * MAX_ENGINES), # Manifold pressure
        ('_tit', c_float * MAX_ENGINES), # Turbine Inlet Temperature
        ('_oil_temp', c_float * MAX_ENGINES), # Oil temp deg F
        ('_oil_px', c_float * MAX_ENGINES), # Oil pressure psi

        # Consumables
        ('_num_tanks', c_uint), # Max number of fuel tanks
        ('_fuel_quantity', c_float * MAX_TANKS),

        # Gear status
        ('_num_wheels', c_uint),
        ('_wow', c_uint * MAX_WHEELS),
        ('_gear_pos', c_float * MAX_WHEELS),
        ('_gear_steer', c_float * MAX_WHEELS),
        ('_gear_compression', c_float * MAX_WHEELS),

        # Environment
        ('_cur_time', c_uint), # current unix time
        ('_warp', c_int), # offset in seconds to unix time
        ('_visibility', c_float), # visibility in meters (for env. effects)

        # Control surface positions (normalized values)
        ('_elevator', c_float),
        ('_elevator_trim_tab', c_float),
        ('_left_flap', c_float),
        ('_right_flap', c_float),
        ('_left_aileron', c_float),
        ('_right_aileron', c_float),
        ('_rudder', c_float),
        ('_nose_wheel', c_float),
        ('_speedbrake', c_float),
        ('_spoilers', c_float),
    ]
