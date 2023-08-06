from typing import Optional, List, Tuple

import xarray as xr
import numpy as np


def make(name: str,
         content: np.array,
         dimensions: List[Tuple[str, np.array]],
         unit: Optional[str] = None,
         dimension_units: Optional[List[str]] = None) -> xr.Dataset:
    # Note: Force every string to lower case
    attrs = {}
    if unit is not None:
        attrs["units"] = unit

    coords_dict = dict([(name.lower(), value) for name, value in dimensions])
    if dimension_units is not None:
        coords_dict = {}
        for (dim_name, dim_value), dim_unit in zip(dimensions, dimension_units):
            coords_dict[dim_name.lower()] = (dim_name.lower(), dim_value, {'units': dim_unit})

    return xr.DataArray(
        name=name.lower(),
        data=content,
        dims=[name.lower() for name, _ in dimensions],
        coords=coords_dict,
        attrs=attrs
    ).to_dataset()


def coordinates(ds: xr.Dataset) -> List[str]:
    return [str(coord) for coord in ds.coords]


def variables(ds: xr.Dataset) -> List[str]:
    coords = coordinates(ds)
    variables = []
    for v in ds.variables:
        if v in coords:
            continue
        variables.append(v)
    return variables


def to_mship(propulsion: xr.Dataset) -> xr.Dataset:
    if "power" in propulsion.coords:
        raise Exception("MShip only support STW control at the moment")

    stw = propulsion.stw.values
    tws = propulsion.tws.values
    twa = propulsion.twa.values
    wa = np.array([0])
    hs = np.array([0])
    propulsion_power = propulsion.power.transpose("stw", "tws", "twa").values

    propulsion_power = propulsion_power.reshape(stw.shape[0], tws.shape[0], twa.shape[0], wa.shape[0], hs.shape[0])

    return xr.DataArray(
        name="BrakePower",
        data=propulsion_power,
        dims=["STW_kt", "TWS_kt", "TWA_deg", "WA_deg", "Hs_m"],
        coords={
            "STW_kt": stw,
            "TWS_kt": tws,
            "TWA_deg": twa,
            "WA_deg": wa,
            "Hs_m": hs
        },
        attrs={
            "polar_type": "ND",
            "control_variable": "STW_kt"
        }
    ).to_dataset(promote_attrs=True)