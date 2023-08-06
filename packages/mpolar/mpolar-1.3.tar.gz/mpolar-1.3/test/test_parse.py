import unittest
import logging
logging.basicConfig(level=logging.DEBUG)

from test import common
import mpolar


class ParseTest(unittest.TestCase):
    def test_list(self):
        dst = common.download_resource("dice-test-data", "routage-app/propulsion.csv")
        print(mpolar.list_format.parse(dst))

        dst = common.download_resource("dice-test-data", "satori-api/sfc.csv")
        print(mpolar.list_format.parse(dst))

        dst = common.download_resource("dice-test-data", "satori-api/hotel.csv")
        print(mpolar.list_format.parse(dst))

    def test_table(self):
        dst = common.download_resource("dice-test-data", "routage-app/A6V_EcoPolar_RevE_sent_P0.csv")
        print(mpolar.table_format.parse(dst))

        dst = common.download_resource("dice-test-data", "routage-app/Polaire_vagues.csv")
        print(mpolar.table_format.parse(dst,
                                        variable_name="factor", variable_unit="%",
                                        control_name="tws", control_unit="kn",
                                        column_name="swh", column_unit="m",
                                        row_name="mwd", row_unit="°"))

        dst = common.download_resource("dice-test-data", "routage-app/BPIX_test_moro.csv")
        print(mpolar.table_format.parse(dst))

    def test_generic(self):
        p = mpolar.parse(common.download_resource("dice-test-data", "routage-app/A6V_EcoPolar_RevE_sent_P0.csv"))  # table
        print(p)
        p = mpolar.parse(common.download_resource("dice-test-data", "routage-app/propulsion.csv"))  # list
        print(p)
        p = mpolar.parse(common.download_resource("dice-test-data", "routage-app/Polaire_vagues.csv"),  # vagues
                         variable_name="factor", variable_unit="%",
                         control_name="tws", control_unit="kn",
                         column_name="swh", column_unit="m",
                         row_name="mwd", row_unit="°")
        print(p)

    def test_make_hybrid(self):
        p = mpolar.parse(common.download_resource("dice-test-data", "routage-app/motor-v2.csv"))
        p = mpolar.propulsion.make_hybrid(p)
        print(p)

    def test_parse_with_spaces(self):
        a = common.download_resource("dice-test-data", "routage-app/Exemple_Powerbrake_SATORI.csv")
        p = mpolar.parse(a, sep=",")

    def test_parse_with_empty_column(self):
        a = common.download_resource("dice-test-data", "routage-app/empty_column.csv")
        p = mpolar.parse(a)
        print(p)

    def test_hotel_with_coma(self):
        a = common.download_resource("dice-test-data", "routage-app/hotel_with_coma.csv")
        p = mpolar.parse(a)
        print(p)

    def test_incomplete_polar(self):
        a = common.download_resource("dice-test-data", "routage-app/incomplete_polar.csv")
        p = mpolar.parse(a)
        print(p)

    def test_mship(self):
        # 3D
        prop = mpolar.parse(common.download_resource("dice-test-data", "satori-api/Polaire_Propulsion.csv"))

        # # 4D
        # hotel = mpolar.parse(common.download_resource("dice-test-data", "satori-api/hotel.csv"))
        # print(hotel)
        #
        # # 1D  for SFC curves, we want to extrapolate if possible
        # sfc = mpolar.parse(common.download_resource("dice-test-data", "satori-api/sfc.csv"))
        mpolar.polar.to_mship(prop).to_netcdf("/tmp/polar.nc")
