import numpy as np
from scipy import stats
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import warnings

warnings.filterwarnings('ignore')

nInst = 50
currentPos = np.zeros(nInst)

def getMyPosition(prcSoFar):
    global currentPos, model
    (nins, nt) = prcSoFar.shape
    
    if nt < 50:
        return np.zeros(nins)
    
    if not model.is_trained and nt >= 100:
        model.train(prcSoFar)
    
    if model.is_trained:
        predictions = model.predict(prcSoFar)
        
        # Convert predictions to desired positions
        desired_positions = predictions * 5000  # Scale predictions to position sizes
        
        # Apply position limits ($10k per instrument)
        max_positions = 10000 / prcSoFar[:, -1]
        desired_positions = np.clip(desired_positions, -max_positions, max_positions)
        
        # Risk management: reduce exposure in high volatility regime
        volatility = np.std(np.log(prcSoFar[:, -20:] / prcSoFar[:, -21:-1]), axis=1)
        volatility_factor = 1 / (1 + np.exp(10 * (volatility - np.mean(volatility))))  # Sigmoid function
        desired_positions *= volatility_factor
        
        # Convert to integer positions
        desired_positions = np.round(desired_positions).astype(int)
        
        # Calculate the change in positions
        position_changes = desired_positions - currentPos
        
        # Apply a maximum change of 20% of the maximum allowed position
        max_change = 0.2 * max_positions
        position_changes = np.clip(position_changes, -max_change, max_change)
        
        # Update current positions
        currentPos += position_changes.astype(int)
    
    return currentPos
