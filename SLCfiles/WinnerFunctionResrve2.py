import numpy as np
import scipy.stats as stats

from SLCfiles.ShareSettings import ProblemSettings, SCASettings
    
def WinnerFunctionResrve2(League = None,Winner = None,nEval = None): 
    De = ProblemSettings["De"]
    nVar = ProblemSettings["nVar"]
    VarSize = ProblemSettings["VarSize"]
    VarMin = ProblemSettings["VarMin"]
    VarMax = ProblemSettings["VarMax"]
    nMainPlayer = SCASettings["nMainPlayer"]
    nReservePlayer = SCASettings["nReservePlayer"]
    CostFunction = ProblemSettings["CostFunction"]
    for i in np.arange(1,np.rint(nReservePlayer / 1)+1).reshape(-1):
        xxx = 0
        a = np.random.permutation(nMainPlayer)
        Gravity = League(Winner,1).MPlayer(a[-2],1).Position
        x = League(Winner,1).RPlayer(-1,1).Position
        beta = stats.uniform.rvs(0.9,1.1,VarSize)
        rq = np.amin(np.amax(Gravity + (np.multiply(beta,(Gravity - x))),np.amin(De)),np.amax(De))
        NewSol={"Position":[None]*nVar}
        for i2 in np.arange(1,nVar+1).reshape(-1):
            __,index = np.amin(np.abs(De - rq(i2)))
            NewSol["Position"][1,i2] = De(index)
        nEval = nEval + 1
        NewSol.Cost = CostFunction(NewSol["Position"])
        if NewSol.Cost < League(Winner,1).RPlayer(-1,1).Cost:
            League[Winner,1].RPlayer[-1,1] = NewSol
        else:
            beta = stats.uniform.rvs(0.4,0.6,VarSize)
            rq = np.amin(np.amax(Gravity + (np.multiply(beta,(x - Gravity))),np.amin(De)),np.amax(De))
            for i2 in np.arange(1,nVar+1).reshape(-1):
                __,index = np.amin(np.abs(De - rq(i2)))
                NewSol["Position"][1,i2] = De(index)
            nEval = nEval + 1
            NewSol.Cost = CostFunction(NewSol["Position"])
            if NewSol.Cost < League(Winner,1).RPlayer(-1,1).Cost:
                League[Winner,1].RPlayer[-1,1] = NewSol
            else:
                XY = np.round(stats.uniform.rvs(VarMin,VarMax,VarSize))
                zz={"Position":[None]*nVar}
                for k in np.arange(1,nVar+1).reshape(-1):
                    a = XY(k)
                    zz["Position"][1,k] = De(a)
                nEval = nEval + 1
                zz["Cost"] = CostFunction(zz["Position"])
                League[Winner,1].RPlayer[-1,1] = zz
        MainPlayer = League(Winner,1).MPlayer
        RvrsPlayer = League(Winner,1).RPlayer
        Player = np.array([[MainPlayer],[RvrsPlayer]])
        PlayerCost = np.array([Player.Cost])
        a1,SortOrder = sorted(PlayerCost)
        Player = Player(SortOrder)
        League(Winner,1).MPlayer = Player(np.arange(1,nMainPlayer+1))
        League(Winner,1).RPlayer = Player(np.arange(nMainPlayer + 1,nMainPlayer + nReservePlayer+1))
    
    return League,nEval