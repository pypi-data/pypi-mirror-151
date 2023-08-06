# -*- coding: utf-8 -*-

import numpy as np
import math

import xarray as xr

import metpy.calc as mpcalc
from metpy.units import units

from metdig.cal.lib import utility as utl
import metdig.utl as mdgstda

__all__ = [
    'lcl',
    'parcel_profile',
]


# def lcl(pres, tmp, td, max_iters=50, eps=1e-5):
#     pres_p = utl.stda_to_quantity(pres)  # hpa
#     tmp_p = utl.stda_to_quantity(tmp)  # degC
#     td_p = utl.stda_to_quantity(td)  # degC

#     lcl_pres, lcl_tmp = mpcalc.lcl(pres_p, tmp_p, td_p, max_iters=max_iters, eps=eps)

#     lcl_pres = utl.quantity_to_stda_byreference('pres', lcl_pres, pres)
#     lcl_tmp = utl.quantity_to_stda_byreference('tmp', lcl_tmp, pres)

#     return lcl_pres, lcl_tmp

def lfc(pres,tmp,td,psfc=None,t2m=None,td2m=None,parcel_temperature_profile=None,dewpoint_start=None, which='top'):
    #如果psfc=None,t2m=None,td2m=None，则默认从pres的最低层抬升
    #如果psfc、t2m、td2m都不为None 则默认从模式地面开始抬升
    lfc_pres=xr.zeros_like(pres.isel(level=[0])).copy()
    lfc_pres.level.values[0]=0
    lfc_pres.attrs['var_cn_name']='自由对流气压'
    lfc_tmp=xr.zeros_like(tmp.isel(level=[0])).copy()
    lfc_tmp.level.values[0]=0
    lfc_tmp.attrs['var_cn_name']='自由对流温度'
    for imember in pres.member.values:
        for idtime in pres.dtime.values:
            for itime in pres.time.values:
                for ilon in pres.lon.values:
                    for ilat in pres.lat.values:
                        pres1d=pres.sel(member=[imember],dtime=[idtime],time=[itime],lon=[ilon],lat=[ilat])
                        tmp1d=tmp.sel(member=[imember],dtime=[idtime],time=[itime],lon=[ilon],lat=[ilat])
                        td1d=td.sel(member=[imember],dtime=[idtime],time=[itime],lon=[ilon],lat=[ilat])
                        try:
                            if((psfc is not None) and (t2m is not None) and (td2m is not None)):
                                psfc1d=psfc.sel(member=[imember],dtime=[idtime],time=[itime],lon=[ilon],lat=[ilat])
                                t2m1d=t2m.sel(member=[imember],dtime=[idtime],time=[itime],lon=[ilon],lat=[ilat])
                                td2m1d=td2m.sel(member=[imember],dtime=[idtime],time=[itime],lon=[ilon],lat=[ilat])

                                pres1d=pres1d.where(pres1d<psfc1d.values,drop=True)
                                tmp1d=tmp1d.where(pres1d<psfc1d.values,drop=True)
                                td1d=td1d.where(pres1d<psfc1d.values,drop=True)

                                pres1d_p=xr.concat([pres1d,psfc1d],dim='level').stda.quantity
                                tmp1d_p=xr.concat([tmp1d,t2m1d],dim='level').stda.quantity
                                td1d_p=xr.concat([td1d,td2m1d],dim='level').stda.quantity
                                lfc_pres1d_p,lfc_tmp1d_p=mpcalc.lfc(pres1d_p,tmp1d_p,td1d_p)
                            else:
                                pres1d_p=xr.stda.quantity
                                tmp1d_p=xr.stda.quantity
                                td1d_p=xr.stda.quantity
                                lfc_pres1d_p,lfc_tmp1d_p=mpcalc.lfc(pres1d_p,tmp1d_p,td1d_p)
                            lfc_pres.loc[dict(member=[imember],dtime=[idtime],time=[itime],lon=[ilon],lat=[ilat])]=[lfc_pres1d_p.magnitude]
                            lfc_tmp.loc[dict(member=[imember],dtime=[idtime],time=[itime],lon=[ilon],lat=[ilat])]=[lfc_tmp1d_p.magnitude]
                        except:
                            lfc_pres.loc[dict(member=[imember],dtime=[idtime],time=[itime],lon=[ilon],lat=[ilat])]=[np.nan]
                            lfc_tmp.loc[dict(member=[imember],dtime=[idtime],time=[itime],lon=[ilon],lat=[ilat])]=[np.nan]
    return lfc_pres,lfc_tmp

def lcl(pres, tmp, td, max_iters=50, eps=1e-5):
    pres_p = utl.stda_to_quantity(pres)  # hpa
    tmp_p = utl.stda_to_quantity(tmp)  # degC
    td_p = utl.stda_to_quantity(td)  # degC

    lcl_pres, lcl_tmp = mpcalc.lcl(pres_p, tmp_p, td_p, max_iters=max_iters, eps=eps)

    lcl_pres = utl.quantity_to_stda_byreference('pres', lcl_pres, pres)
    lcl_tmp = utl.quantity_to_stda_byreference('tmp', lcl_tmp, pres)

    return lcl_pres, lcl_tmp


def parcel_profile(pres, tmp, td):
    pres_p = utl.stda_to_quantity(pres)  # hpa
    tmp_p = utl.stda_to_quantity(tmp)  # degC
    td_p = utl.stda_to_quantity(td)  # degC

    profile = mpcalc.parcel_profile(pres_p, tmp_p, td_p)

    profile = utl.quantity_to_stda_byreference('tmp', profile, pres)

    return profile
