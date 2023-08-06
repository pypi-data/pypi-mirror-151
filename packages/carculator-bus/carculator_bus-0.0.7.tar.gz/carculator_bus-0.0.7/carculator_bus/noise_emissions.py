import numexpr as ne
import numpy as np


def pn(cycle, powertrain_type, category):
    cycle = np.array(cycle)

    # Noise sources are calculated for speeds above 20 km/h.
    if powertrain_type in ("combustion", "electric"):
        if category == "medium":
            array = np.tile((cycle - 70) / 70, 8).reshape((8, -1))

            constants = np.array(
                (101, 96.5, 98.8, 96.8, 98.6, 95.2, 88.8, 82.7)
            ).reshape((-1, 1))
            coefficients = np.array((-1.9, 4.7, 6.4, 6.5, 6.5, 6.5, 6.5, 6.5)).reshape(
                (-1, 1)
            )

        if category == "heavy":
            array = np.tile((cycle - 70) / 70, 8).reshape((8, -1))
            constants = np.array(
                (104.4, 100.6, 101.7, 101, 100.1, 95.9, 91.3, 85.3)
            ).reshape((-1, 1))
            coefficients = np.array((0, 3, 4.6, 5, 5, 5, 5, 5)).reshape((-1, 1))

        array = array * coefficients + constants

        if powertrain_type == "electric":
            # For electric cars, we add correction factors
            # We also add a 56 dB loud sound signal when the speed is below 20 km/h.
            correction = np.array((0, 1.7, 4.2, 15, 15, 15, 13.8, 0)).reshape((-1, 1))
            array -= correction
            array[:, cycle.reshape(-1) < 20] = 56
        else:
            array[:, cycle.reshape(-1) < 20] = 0
    else:
        # For non plugin-hybrids, apply electric engine noise coefficient up to 30 km/h
        # and combustion engine noise coefficients above 30 km/h
        electric = pn(cycle, "electric")
        electric_mask = cycle.reshape(-1) < 30

        array = pn(cycle, "combustion")
        array[:, electric_mask] = electric[:, electric_mask]
    return array


class NoiseEmissionsModel:
    """
    Calculate propulsion and rolling noise emissions for combustion, hybrid and electric trucks, based on CNOSSOS model.

    :param cycle: Driving cycle. Pandas Series of second-by-second speeds (km/h) or name (str)
        of cycle e.g., "WLTC","WLTC 3.1","WLTC 3.2","WLTC 3.3","WLTC 3.4","CADC Urban","CADC Road",
        "CADC Motorway","CADC Motorway 130","CADC","NEDC".
    :type cycle: pandas.Series

    """

    def __init__(self):
        pass

    def rolling_noise(self, category, cycle):
        """Calculate noise from rolling friction.
        Model from CNOSSOS-EU project
        (http://publications.jrc.ec.europa.eu/repository/bitstream/JRC72550/cnossos-eu%20jrc%20reference%20report_final_on%20line%20version_10%20august%202012.pdf)

        :param category: "medium" or "heavy" duty vehicles.
        :type category: str.

        :returns: a_matrix numpy array with rolling noise (dB) for each 8 octaves, per second of driving cycle
        :rtype: numpy.array

        """

        if category == "medium":
            array = np.tile(
                np.log10(cycle / 70, out=np.zeros_like(cycle), where=(cycle != 0)), 8
            ).reshape((8, -1))

            constants = np.array(
                (84, 88.7, 91.5, 96.7, 97.4, 90.9, 83.8, 80.5)
            ).reshape((-1, 1))
            coefficients = np.array(
                (30, 35.8, 32.6, 23.8, 30.1, 36.2, 38.3, 40.1)
            ).reshape((-1, 1))

        else:
            array = np.tile(
                np.log10(cycle / 70, out=np.zeros_like(cycle), where=(cycle != 0)), 8
            ).reshape((8, -1))
            constants = np.array(
                (87, 91.7, 94.1, 100.7, 100.8, 94.3, 87.1, 82.5)
            ).reshape((-1, 1))
            coefficients = np.array(
                (30, 33.5, 31.3, 25.4, 31.8, 37.1, 38.6, 40.6)
            ).reshape((-1, 1))
        array = array * coefficients + constants

        return array

    def propulsion_noise(self, powertrain_type, category, cycle):
        """Calculate noise from propulsion engine and gearbox.
        Model from CNOSSOS-EU project
        (http://publications.jrc.ec.europa.eu/repository/bitstream/JRC72550/cnossos-eu%20jrc%20reference%20report_final_on%20line%20version_10%20august%202012.pdf)

        For electric cars, special coefficients are applied from
        (`Pallas et al. 2016 <https://www.sciencedirect.com/science/article/pii/S0003682X16301608>`_ )

        Also, for electric cars, a warning signal of 56 dB is added when the car drives at 20 km/h or lower.

        Although we deal here with trucks, we reuse the coefficeint for electric cars

        :param powertrain_type:
        :param category: "medium" or "heavy" duty vehicles.
        :type category: str.
        :returns: a_matrix numpy array with propulsion noise (dB) for all 8 octaves, per second of driving cycle
        :rtype: numpy.array

        """

        # Noise sources are calculated for speeds above 20 km/h.
        if powertrain_type in ("combustion", "electric"):

            if category == "medium":
                array = np.tile((cycle - 70) / 70, 8).reshape((8, -1))

                constants = np.array(
                    (101, 96.5, 98.8, 96.8, 98.6, 95.2, 88.8, 82.7)
                ).reshape((-1, 1))
                coefficients = np.array(
                    (-1.9, 4.7, 6.4, 6.5, 6.5, 6.5, 6.5, 6.5)
                ).reshape((-1, 1))

            if category == "heavy":
                array = np.tile((cycle - 70) / 70, 8).reshape((8, -1))
                constants = np.array(
                    (104.4, 100.6, 101.7, 101, 100.1, 95.9, 91.3, 85.3)
                ).reshape((-1, 1))
                coefficients = np.array((0, 3, 4.6, 5, 5, 5, 5, 5)).reshape((-1, 1))

            array = array * coefficients + constants

            if powertrain_type == "electric":
                # For electric cars, we add correction factors
                # We also do so for trucks, as these are correction factors, not absolute values
                # TODO: find better correction factors for trucks

                # We also add a 56 dB loud sound signal when the speed is below 20 km/h.
                correction = np.array((0, 1.7, 4.2, 15, 15, 15, 13.8, 0)).reshape(
                    (-1, 1)
                )
                array -= correction

                # Warming signal for electric cars of 56 dB at 20 km/h or lower
                array[:, cycle.reshape(-1) < 20] = 56

        else:
            if category == "medium":
                cycle = cycle[:, :4]
                # For non plugin-hybrids, apply electric engine noise coefficient up to 30 km/h
                # and combustion engine noise coefficients above 30 km/h
                electric = pn(cycle, "electric", category)
                electric_mask = cycle < 30

                array = pn(cycle, "combustion", category)
                array[:, electric_mask.reshape(-1)] = electric[
                    :, electric_mask.reshape(-1)
                ]
            else:
                cycle = cycle[:, 4:]
                # For non plugin-hybrids, apply electric engine noise coefficient up to 30 km/h
                # and combustion engine noise coefficients above 30 km/h
                electric = pn(cycle, "electric", category)
                electric_mask = cycle < 30

                array = pn(cycle, "combustion", category)
                array[:, electric_mask.reshape(-1)] = electric[
                    :, electric_mask.reshape(-1)
                ]

        return array

    def get_sound_power_per_compartment(self, powertrain_type, category, cycle, size):
        """
        Calculate sound energy (in J/s) over the driving cycle duration from sound power (in dB).
        The sound energy sums are further divided into `geographical compartments`: urban, suburban and rural.

        :return: Sound energy (in Joules) per km driven, per geographical compartment.
        :rtype: numpy.array
        """

        if powertrain_type not in ("combustion", "electric", "hybrid"):
            raise TypeError("The powertrain type is not valid.")

        # rolling noise, in dB, for each second of the driving cycle
        if category == "medium":
            rolling = self.rolling_noise(category, cycle).reshape(
                8, cycle.shape[-1], -1
            )
            # propulsion noise, in dB, for each second of the driving cycle
            propulsion = self.propulsion_noise(
                powertrain_type, category, cycle
            ).reshape(8, cycle.shape[-1], -1)
            c = cycle.T
        elif category == "heavy":
            rolling = self.rolling_noise(category, cycle).reshape(
                8, cycle.shape[-1], -1
            )
            # propulsion noise, in dB, for each second of the driving cycle
            propulsion = self.propulsion_noise(
                powertrain_type, category, cycle
            ).reshape(8, cycle.shape[-1], -1)
            c = cycle.T
        else:
            raise TypeError("The category type is not valid.")

        # sum of rolling and propulsion noise sources
        total_noise = ne.evaluate(
            "where(c != 0, 10 * log10((10 ** (rolling / 10)) + (10 ** (propulsion / 10))), 0)"
        )

        # convert dBs to Watts (or J/s)
        sound_power = ne.evaluate("(10 ** -12) * (10 ** (total_noise / 10))")

        # If the driving cycle selected is one of the driving cycles for which carculator has specifications,
        # we use the driving cycle "official" road section types to compartmentalize emissions.
        # If the driving cycle selected is instead specified by the user (passed directly as an array), we used
        # speed levels to compartmentalize emissions.

        distance = c.sum(axis=1) / 3600

        urban = np.zeros((8, c.shape[0]))
        suburban = np.zeros((8, c.shape[0]))
        rural = np.zeros((8, c.shape[0]))

        for s, x in enumerate(size):
            if x in ["9m", "13m-city", "13m-city-double"]:

                urban[:, s] = (np.sum(sound_power, axis=2) / distance)[:, s]

            else:

                urban[:, s] = (np.sum(sound_power[:, :, :500], axis=2) / distance)[:, s]
                urban[:, s] += (
                    np.sum(sound_power[:, :, 6000:6800], axis=2) / distance
                )[:, s]
                urban[:, s] += (
                    np.sum(sound_power[:, :, 7600:8800], axis=2) / distance
                )[:, s]
                urban[:, s] += (
                    np.sum(sound_power[:, :, 10600:11500], axis=2) / distance
                )[:, s]
                urban[:, s] += (
                    np.sum(sound_power[:, :, 12500:14000], axis=2) / distance
                )[:, s]

                rural[:, s] = (np.sum(sound_power[:, :, 500:6000], axis=2) / distance)[
                    :, s
                ]
                rural[:, s] += (
                    np.sum(sound_power[:, :, 6800:7600], axis=2) / distance
                )[:, s]
                rural[:, s] += (
                    np.sum(sound_power[:, :, 8800:10600], axis=2) / distance
                )[:, s]
                rural[:, s] += (
                    np.sum(sound_power[:, :, 11500:12500], axis=2) / distance
                )[:, s]
                rural[:, s] += (np.sum(sound_power[:, :, 14000:], axis=2) / distance)[
                    :, s
                ]

        res = np.vstack([urban, suburban, rural]).T
        return res.reshape(-1, 1, 24, 1, 1)
