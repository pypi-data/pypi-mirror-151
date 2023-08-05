"""

Computing features about accelerometer orientations

Author: Qu Tang

Date: Jul 10, 2018
"""
import numpy as np
from numpy.linalg import norm
from SWaN_accel.utils import *
from math import *

class OrientationFeature:
    def __init__(self, X, subwins=4):
        self._X = X
        self._subwins = subwins

    @staticmethod
    def orientation_xyz(X, unit='rad'):
        X = as_float64(X)
        if not has_enough_samples(X):
            print(
                '''One of sub windows do not have enough samples, will ignore in
                feature computation''')
            orientation_xyz = np.array([np.nan, np.nan, np.nan])
        else:


            mdn_val = np.median(X, axis=0)
            x_mdn, y_mdn, z_mdn = mdn_val[0], mdn_val[1], mdn_val[2]

            denom = np.sqrt(x_mdn * x_mdn + y_mdn * y_mdn + z_mdn * z_mdn)
            x_mdn_norm, y_mdn_norm, z_mdn_norm = x_mdn / denom, y_mdn / denom, z_mdn / denom

            x_ang = acos(x_mdn_norm) * (180 / pi)
            y_ang = acos(y_mdn_norm) * (180 / pi)
            z_ang = acos(z_mdn_norm) * (180 / pi)
            orientation_xyz = np.array([x_ang, y_ang, z_ang])

        return vec2rowarr(orientation_xyz)

    def estimate_orientation(self, unit='rad'):
        result = apply_over_subwins(
            self._X, OrientationFeature.orientation_xyz, subwins=self._subwins, unit=unit)
        self._orientations = np.concatenate(result, axis=0)
        return self

    def median_angles(self):
        median_angles = np.nanmedian(self._orientations, axis=0)
        result = vec2rowarr(np.array(median_angles))
        result = add_name(result, self.median_angles.__name__)
        return result

    def median_x_angle(self):
        median_angles = np.nanmedian(self._orientations, axis=0)
        result = vec2rowarr(np.array([median_angles[0]]))
        result = add_name(result, self.median_x_angle.__name__)
        return result

    def ori_x_median(self):
        median_angles = np.nanmedian(self._orientations, axis=0)
        result = vec2rowarr(np.array([median_angles[0]]))
        result = add_name(result, self.ori_x_median.__name__)
        return result

    def ori_y_median(self):
        median_angles = np.nanmedian(self._orientations, axis=0)
        result = vec2rowarr(np.array([median_angles[1]]))
        result = add_name(result, self.ori_y_median.__name__)
        return result

    def ori_z_median(self):
        median_angles = np.nanmedian(self._orientations, axis=0)
        result = vec2rowarr(np.array([median_angles[2]]))
        result = add_name(result, self.ori_z_median.__name__)
        return result

    def median_y_angle(self):
        median_angles = np.nanmedian(self._orientations, axis=0)
        result = vec2rowarr(np.array([median_angles[1]]))
        result = add_name(result, self.median_y_angle.__name__)
        return result

    def median_z_angle(self):
        median_angles = np.nanmedian(self._orientations, axis=0)
        result = vec2rowarr(np.array([median_angles[2]]))
        result = add_name(result, self.median_z_angle.__name__)
        return result

    def range_angles(self):
        range_angles = abs(np.nanmax(
            self._orientations, axis=0) - np.nanmin(self._orientations, axis=0))
        result = vec2rowarr(np.array(range_angles))
        result = add_name(result, self.range_angles.__name__)
        return result

    def range_x_angle(self):
        range_angles = np.nanmax(
            self._orientations, axis=0) - np.nanmin(self._orientations, axis=0)
        result = vec2rowarr(np.array([range_angles[0]]))
        result = add_name(result, self.range_x_angle.__name__)
        return result

    def range_y_angle(self):
        range_angles = np.nanmax(
            self._orientations, axis=0) - np.nanmin(self._orientations, axis=0)
        result = vec2rowarr(np.array([range_angles[1]]))
        result = add_name(result, self.range_y_angle.__name__)
        return result

    def range_z_angle(self):
        range_angles = np.nanmax(
            self._orientations, axis=0) - np.nanmin(self._orientations, axis=0)
        result = vec2rowarr(np.array([range_angles[2]]))
        result = add_name(result, self.range_z_angle.__name__)
        return result

    def std_angles(self):
        std_angles = np.nanstd(self._orientations, axis=0)
        result = vec2rowarr(np.array(std_angles))
        result = add_name(result, self.std_angles.__name__)
        return result

    def std_x_angle(self):
        std_angles = np.nanstd(self._orientations, axis=0)
        result = vec2rowarr(np.array([std_angles[0]]))
        result = add_name(result, self.std_x_angle.__name__)
        return result

    def std_y_angle(self):
        std_angles = np.nanstd(self._orientations, axis=0)
        result = vec2rowarr(np.array([std_angles[1]]))
        result = add_name(result, self.std_y_angle.__name__)
        return result

    def std_z_angle(self):
        std_angles = np.nanstd(self._orientations, axis=0)
        result = vec2rowarr(np.array([std_angles[2]]))
        result = add_name(result, self.std_z_angle.__name__)
        return result

    def zerocross_x_angle(self):
        ar = self._orientations[:,0]
        asign = np.sign(ar)
        sz = asign == 0
        while sz.any():
            asign[sz] = np.roll(asign, 1)[sz]
            sz = asign == 0
        signchange = ((np.roll(asign, 1) - asign) != 0).astype(np.int32)
        signchange[0] = 0
        if 1 in signchange:
            zcross = 1
        else:
            zcross = 0

        result = vec2rowarr(np.array([zcross]))
        result = add_name(result, self.zerocross_x_angle.__name__)
        return result

    def zerocross_y_angle(self):
        ar = self._orientations[:,1]
        asign = np.sign(ar)
        sz = asign == 0
        while sz.any():
            asign[sz] = np.roll(asign, 1)[sz]
            sz = asign == 0
        signchange = ((np.roll(asign, 1) - asign) != 0).astype(np.int32)
        signchange[0] = 0
        if 1 in signchange:
            zcross = 1
        else:
            zcross = 0

        result = vec2rowarr(np.array([zcross]))
        result = add_name(result, self.zerocross_y_angle.__name__)
        return result

    def zerocross_z_angle(self):
        ar = self._orientations[:,2]
        asign = np.sign(ar)
        sz = asign == 0
        while sz.any():
            asign[sz] = np.roll(asign, 1)[sz]
            sz = asign == 0
        signchange = ((np.roll(asign, 1) - asign) != 0).astype(np.int32)
        signchange[0] = 0
        if 1 in signchange:
            zcross = 1
        else:
            zcross = 0

        result = vec2rowarr(np.array([zcross]))
        result = add_name(result, self.zerocross_z_angle.__name__)
        return result

    def ori_var_sum(self):
        var_angles = np.nanvar(self._orientations, axis=0)
        result = vec2rowarr(np.array([np.sum(var_angles)]))
        result = add_name(result, self.ori_var_sum.__name__)
        return result
    
        
    def ori_range_max(self):
        range_angles = abs(np.nanmax(
            self._orientations, axis=0) - np.nanmin(self._orientations, axis=0))
        result = vec2rowarr(np.array([np.sum(range_angles)]))
        result = add_name(result, self.ori_range_max.__name__)
        return result