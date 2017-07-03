from nose.tools import assert_equal, assert_false, assert_almost_equal, assert_true, assert_greater
import cmsl1t.utils.fit_efficiency as fit
from rootpy.plotting import F1, Hist, Canvas
from rootpy import asrootpy, ROOT


def test_get_asymmetric_formula():
    formula = fit.get_asymmetric_formula()
    assert_false("{" in formula)


def test__create_output_dict_sym():
    test_func = F1("[0] + [1]", 0, 10, name="sym")
    test_func.SetParameters(1, 2)
    test_func.SetParError(0, 3)
    test_func.SetParError(1, 4)
    test_func.SetParNames("mu", "sigma_inv")
    success = False

    params = fit._create_output_dict(success, [test_func], "")

    assert_equal(params["success"], False)
    assert_equal(params["mu"], (1, 3))
    assert_equal(params["sigma_inv"], (2, 4))
    assert_equal(params["sigma"][0], 1. / 2)
    assert_equal(params["symmetric"].name, "sym")
    assert_false("asymmetric" in params)


def FakeEff(in_mean, in_sigma):
    in_func = F1("TMath::Gaus(x,{},{},true)".format(in_mean, in_sigma), 0, 100)
    resolution = Hist(50, 0, 100)
    n_events = 20000000
    resolution.FillRandom(in_func.name, n_events)
    resolution.Scale(1. / n_events)
    hist = resolution.GetCumulative()
    return hist


def test_fit_efficiency_symmetric():
    in_mean = 35.
    in_sigma = 10.
    fake_efficiency = FakeEff(in_mean, in_sigma)

    params = fit.fit_efficiency(fake_efficiency, 30, 10, False)

    mu = params["mu"][0]
    sigma = params["sigma"][0]
    mu_ratio = mu / in_mean if mu > in_mean else in_mean / mu
    sigma_ratio = sigma / in_sigma if sigma > in_sigma else in_sigma / sigma
    assert_greater(1.1, mu_ratio)
    assert_greater(1.5, sigma_ratio)
    assert_true(params["success"])


def test_fit_efficiency_asymmetric():
    in_mean = 35.
    in_sigma = 10.
    fake_efficiency = FakeEff(in_mean, in_sigma)

    params = fit.fit_efficiency(fake_efficiency, 30, 10, True)

    mu = params["mu"][0]
    sigma = params["sigma"][0]
    lamda = params["lambda"][0]
    mu_ratio = mu / in_mean if mu > in_mean else in_mean / mu
    sigma_ratio = sigma / in_sigma if sigma > in_sigma else in_sigma / sigma
    assert_greater(1.1, mu_ratio)
    assert_greater(1.5, sigma_ratio)
    assert_greater(0.5, abs(lamda))
    assert_true(params["success"])
