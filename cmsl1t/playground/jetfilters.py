
def jetFilterNoHF(jet):
    '''
        also a lot of potential for simplification
    '''
    if jet.muMult != 0:
        return False
    if abs(jet.eta) > 3.0:
        return False
    if jet.nhef >= 0.9:
        return False
    if jet.pef >= 0.9:
        return False
    if jet.mef >= 0.8:
        return False
    if jet.allMult <= 1:
        return False
    if abs(jet.eta) > 2.4:
        return True
    if jet.sumMult <= 0:
        return False
    if jet.chef <= 0:
        return False
    if jet.eef >= 0.9:
        return False
    return True

def defaultJetFilter(jet):
    return (abs(jet.eta) > 3.0 or jetFilterNoHF(jet)) and jet.etCorr > 30.
