from numbers import Number
from typing import Union

import numpy as np
from sklearn.metrics import r2_score


def RMSE(
        Qobs: Union[list, np.ndarray],
        Qsim: Union[list, np.ndarray]
) -> float:
    """
    Root Mean Squared Error. Metric for the estimation of performance of the
    hydrological model.

    Inputs:
    ----------
        1-Qobs :
            [numpy ndarray] Measured discharge [m3/s]
        2-Qsim :
            [numpy ndarray] Simulated discharge [m3/s]

    Outputs:
    -------
        1-error :
            [float] RMSE value
    """
    # convert Qobs & Qsim into arrays
    Qobs = np.array(Qobs)
    Qsim = np.array(Qsim)

    rmse = np.sqrt(np.average((np.array(Qobs) - np.array(Qsim)) ** 2), dtype=np.float64)

    return rmse


def RMSEHF(
        Qobs: Union[list, np.ndarray],
        Qsim: Union[list, np.ndarray],
        WStype: int,
        N: int,
        alpha: Union[int, float]
) -> float:
    """
    Weighted Root mean square Error for High flow

    inputs:
    ----------
        1- Qobs:
            observed flow
        2- Qsim:
            simulated flow
        3- WStype:
            Weighting scheme (1,2,3,4)
        4- N:
            power
        5- alpha:
            Upper limit for low flow weight
    Output:
    ----------
        1- error values
    """
    # input data validation
    # data type
    assert isinstance(WStype, int), (
        f"Weighting scheme should be an integer number between 1 and 4 and you entered {WStype}"
    )
    assert isinstance(alpha, int) or isinstance(alpha, float), \
        "alpha should be a number and between 0 & 1"
    assert isinstance(N, Number), "N should be a number and between 0 & 1"
    # Input values
    assert 1 <= WStype <= 4, (
        f"Weighting scheme should be an integer number between 1 and 4 you have enters {WStype}"
    )
    assert (
            N >= 0
    ), f"Weighting scheme Power should be positive number you have entered {N}"
    assert (
            0 < alpha < 1
    ), f"alpha should be float number and between 0 & 1 you have entered {alpha}"

    # convert Qobs & Qsim into arrays
    Qobs = np.array(Qobs)
    Qsim = np.array(Qsim)

    Qmax = max(Qobs)
    h = Qobs / Qmax  # rational Discharge

    if WStype == 1:
        w = h ** N  # rational Discharge power N
    elif (
            WStype == 2
    ):  # -------------------------------------------------------------N is not in the equation
        w = (h / alpha) ** N
        w[h > alpha] = 1
    elif WStype == 3:
        w = np.zeros(np.size(h))  # zero for h < alpha and 1 for h > alpha
        w[h > alpha] = 1
    elif WStype == 4:
        w = np.zeros(np.size(h))  # zero for h < alpha and 1 for h > alpha
        w[h > alpha] = 1
    else:  # sigmoid function
        w = 1 / (1 + np.exp(-10 * h + 5))

    a = (Qobs - Qsim) ** 2
    b = a * w
    c = sum(b)
    error = np.sqrt(c / len(Qobs))

    return error


def RMSELF(
        Qobs: Union[list, np.ndarray],
        Qsim: Union[list, np.ndarray],
        WStype: int,
        N: int,
        alpha: Union[int, float]
) -> float:
    """
    Weighted Root mean square Error for low flow

    inputs:
    ----------
        1- Qobs : observed flow
        2- Qsim : simulated flow
        3- WStype : Weighting scheme (1,2,3,4)
        4- N: power
        5- alpha : Upper limit for low flow weight

    Output:
    ----------
        1- error values
    """
    # input data validation
    # data type
    assert type(WStype) == int, (
            "Weighting scheme should be an integer number between 1 and 4 and you entered "
            + str(WStype)
    )
    assert isinstance(alpha, int) or isinstance(alpha, float), \
        "alpha should be a number and between 0 & 1"
    assert isinstance(N, Number), "N should be a number and between 0 & 1"
    # Input values
    assert 1 <= WStype <= 4, (
        f"Weighting scheme should be an integer number between 1 and 4 you have enters {WStype}"
    )
    assert (
            N >= 0
    ), f"Weighting scheme Power should be positive number you have entered {N}"
    assert (
            0 < alpha < 1
    ), f"alpha should be float number and between 0 & 1 you have entered {alpha}"

    # convert Qobs & Qsim into arrays
    Qobs = np.array(Qobs)
    Qsim = np.array(Qsim)

    Qmax = max(Qobs)  # rational Discharge power N
    l = (Qmax - Qobs) / Qmax

    if WStype == 1:
        w = l ** N
    elif WStype == 2:  # ------------------------------- N is not in the equation
        #        w=1-l*((0.50 - alpha)**N)
        w = ((1 / (alpha ** 2)) * (1 - l) ** 2) - ((2 / alpha) * (1 - l)) + 1
        w[1 - l > alpha] = 0
    elif WStype == 3:  # the same like WStype 2
        #        w=1-l*((0.50 - alpha)**N)
        w = ((1 / (alpha ** 2)) * (1 - l) ** 2) - ((2 / alpha) * (1 - l)) + 1
        w[1 - l > alpha] = 0
    elif WStype == 4:
        #        w = 1-l*(0.50 - alpha)
        w = 1 - ((1 - l) / alpha)
        w[1 - l > alpha] = 0
    else:  # sigmoid function
        #        w=1/(1+np.exp(10*h-5))
        w = 1 / (1 + np.exp(-10 * l + 5))

    a = (Qobs - Qsim) ** 2
    b = a * w
    c = sum(b)
    error = np.sqrt(c / len(Qobs))

    return error


def KGE(Qobs: Union[list, np.ndarray], Qsim: Union[list, np.ndarray]):
    """
    (Gupta et al. 2009) have showed the limitation of using a single error
    function to measure the efficiency of calculated flow and showed that
    Nash-Sutcliff efficiency (NSE) or RMSE can be decomposed into three component
    correlation, variability and bias.

    inputs:
    ----------
        1- Qobs : observed flow
        2- Qsim : simulated flow

    Output:
    ----------
        1- error values
    """
    # convert Qobs & Qsim into arrays
    Qobs = np.array(Qobs)
    Qsim = np.array(Qsim)

    c = np.corrcoef(Qobs, Qsim)[0][1]
    alpha = np.std(Qsim) / np.std(Qobs)
    beta = np.mean(Qsim) / np.mean(Qobs)

    kge = 1 - np.sqrt(((c - 1) ** 2) + ((alpha - 1) ** 2) + ((beta - 1) ** 2))

    return kge


def WB(Qobs, Qsim):
    """
    The mean cumulative error measures how much the model succeed to reproduce
    the stream flow volume correctly. This error allows error compensation from
    time step to another and it is not an indication on how accurate is the model
    in the simulated flow. the naive model of Nash-Sutcliffe (simulated flow is
    as accurate as average observed flow) will result in WB error equals to 100 %.
    (Oudin et al. 2006)

    inputs:
    ----------
        1- Qobs : observed flow
        2- Qsim : simulated flow

    Output:
    ----------
        1- error values
    """
    Qobssum = np.sum(Qobs)
    Qsimsum = np.sum(Qsim)
    wb = 100 * (1 - np.abs(1 - (Qsimsum / Qobssum)))

    return wb


def NSE(Qobs: np.ndarray, Qsim: np.ndarray):
    """
    Nash-Sutcliffe efficiency. Metric for the estimation of performance of the
    hydrological model

    Inputs:
    ----------
        1-Qobs: [numpy ndarray]
            Measured discharge [m3/s]
        2-Qsim: [numpy ndarray]
            Simulated discharge [m3/s]

    Outputs
    -------
        1-f: [float]
            NSE value

    examples:
    -------
        Qobs = np.loadtxt("Qobs.txt")
        Qout = Model(prec,evap,temp)
        error = NSE(Qobs,Qout)
    """
    # convert Qobs & Qsim into arrays
    Qobs = np.array(Qobs)
    Qsim = np.array(Qsim)

    a = sum((Qobs - Qsim) ** 2)
    b = sum((Qobs - np.average(Qobs)) ** 2)
    e = 1 - (a / b)

    return e


def NSEHF(Qobs: Union[list, np.ndarray], Qsim: Union[list, np.ndarray]):
    """NSEHF.

    Modified Nash-Sutcliffe efficiency. Metric for the estimation of performance of the
    hydrological model

    reference:
    Hundecha Y. & Bárdossy A. Modeling of the effect of land use
    changes on the runoff generation of a river basin through
    parameter regionalization of a watershed model. J Hydrol
    2004, 292, (1–4), 281–295

    Inputs:
    ----------
    1-Qobs :
        [numpy ndarray] Measured discharge [m3/s]
    2-Qsim :
        [numpy ndarray] Simulated discharge [m3/s]

    Outputs
    -------
    1-f :
        [float] NSE value

    examples:
    -------
        Qobs=np.loadtxt("Qobs.txt")
        Qout=Model(prec,evap,temp)
        error=NSE(Qobs,Qout)
    """
    # convert Qobs & Qsim into arrays
    Qobs = np.array(Qobs)
    Qsim = np.array(Qsim)

    a = sum(Qobs * (Qobs - Qsim) ** 2)
    b = sum(Qobs * (Qobs - np.average(Qobs)) ** 2)
    e = 1 - (a / b)

    return e


def NSELF(Qobs: Union[list, np.ndarray], Qsim: Union[list, np.ndarray]):
    """NSELF.

    Modified Nash-Sutcliffe efficiency. Metric for the estimation of performance of the
    hydrological model

    reference:
    Hundecha Y. & Bárdossy A. Modeling of the effect of land use
    changes on the runoff generation of a river basin through
    parameter regionalization of a watershed model. J Hydrol
    2004, 292, (1–4), 281–295

    Inputs:
    ----------
    1-Qobs :
        [numpy ndarray] Measured discharge [m3/s]
    2-Qsim :
        [numpy ndarray] Simulated discharge [m3/s]

    Outputs
    -------
    1-f :
        [float] NSE value

    examples:
    -------
        Qobs=np.loadtxt("Qobs.txt")
        Qout=Model(prec,evap,temp)
        error=NSE(Qobs,Qout)
    """
    # convert Qobs & Qsim into arrays
    Qobs = np.array(np.log(Qobs))
    Qsim = np.array(np.log(Qsim))

    a = sum(Qobs * (Qobs - Qsim) ** 2)
    b = sum(Qobs * (Qobs - np.average(Qobs)) ** 2)
    e = 1 - (a / b)

    return e


def MBE(Qobs: Union[list, np.ndarray], Qsim: Union[list, np.ndarray]):
    """
    MBE (mean bias error)
    MBE = (Qsim - Qobs)/n

    Parameters
    ----------
        1-Qobs : [list]
            list of the first time series.
        2-Qsim : [list]
            list of the first time series.

    Returns
    -------
        [float]
            mean bias error.

    """

    return (np.array(Qsim) - np.array(Qobs)).mean()


def MAE(Qobs: Union[list, np.ndarray], Qsim: Union[list, np.ndarray]):
    """
    MAE (mean absolute error)
    MAE = |(Qobs - Qsim)|/n

    Parameters
    ----------
        1-Qobs : [list]
            list of the first time series.
        2-Qsim : [list]
            list of the first time series.

    Returns
    -------
        [float]
            mean absolute error.

    """

    return np.abs(np.array(Qobs) - np.array(Qsim)).mean()


def PearsonCorre(Qobs: Union[list, np.ndarray], Qsim: Union[list, np.ndarray]):
    """
    Pearson correlation coefficient r2 is independent of the magnitude of the numbers;
    it is sensitive to relative changes only.
    """
    return (np.corrcoef(np.array(Qobs), np.array(Qsim))[0][1]) ** 2


def R2(Qobs: Union[list, np.ndarray], Qsim: Union[list, np.ndarray]):
    """R2.

        the coefficient of determination measures how well the predicted
        values match (and not just follow) the observed values.
        It depends on the distance between the points and the 1:1 line
        (and not the best-fit line)
        Closer the data to the 1:1 line, higher the coefficient of determination.
        The coefficient of determination is often denoted by R². However,
        it is not the square of anything. It can range from any negative number to +1
        - R² = +1 indicates that the predictions match the observations perfectly
        - R² = 0 indicates that the predictions are as good as random guesses around
            the mean of the observed values
        - Negative R² indicates that the predictions are worse than random

    Since R² indicates the distance of points from the 1:1 line, it does depend
    on the magnitude of the numbers (unlike r² peason correlation coefficient).
    """

    return r2_score(np.array(Qobs), np.array(Qsim))
