# python eval.py

import numpy as np
import warnings

warnings.filterwarnings('ignore')

nInst = 50
currentPos = np.zeros(nInst)

def getMyPosition(prcSoFar):
    global currentPos
    (nins, nt) = prcSoFar.shape
    if (nt < 2):
        return np.zeros(nins)
    threshold = 0.02
    change = 0.5
    
    # Calculate the previous day's return for company 22
    prev_return_22 = prcSoFar[22, -1] / prcSoFar[22, -2] - 1
    prev_return_30 = prcSoFar[30, -1] / prcSoFar[30, -2] - 1
    # prev_return_25 = prcSoFar[25, -1] / prcSoFar[25, -2] - 1
    prev_return_11 = prcSoFar[11, -1] / prcSoFar[11, -2] - 1
    # prev_return_38 = prcSoFar[38, -1] / prcSoFar[38, -2] - 1

    # Determine the desired position for company 38
    if prev_return_22 > threshold and prev_return_30 > threshold: #  and prev_return_25 > threshold
        desired_position_38 = 10000
    elif prev_return_22 < threshold and prev_return_30 < threshold: # and prev_return_25 < threshold
        desired_position_38 = -10000
    else:
        desired_position_38 = 0
    
    # Determine the desired position for company 38
    if prev_return_22 > threshold and prev_return_11 > threshold: #  and prev_return_38 > threshold
        desired_position_27 = 10000
    elif prev_return_22 < threshold and prev_return_11 < threshold: # and prev_return_38 < threshold
        desired_position_27 = -10000
    else:
        desired_position_27 = 0
    
    # Create the new position array
    new_pos = np.zeros(nins)
    new_pos[38] = desired_position_38
    new_pos[27] = desired_position_27
    
    # Calculate the change in positions
    position_changes = new_pos - currentPos
    
    # Apply a maximum change of 20% of the maximum allowed position
    max_change = 10000 * change
    position_changes = np.clip(position_changes, -max_change, max_change)
    
    # Update current positions
    currentPos += position_changes.astype(int)

    return currentPos

# def getMyPosition(prcSoFar):
    
#     (nins, nt) = prcSoFar.shape
#     currentPos = np.zeros(nins)
#     threshold = 0.02
#     change = 0.5
    
#     if (nt < 2):
#         return np.zeros(nins)
    
#     # Calculate the previous day's return for company 22
#     prev_return_22 = prcSoFar[22, -1] / prcSoFar[22, -2] - 1
#     prev_return_30 = prcSoFar[30, -1] / prcSoFar[30, -2] - 1
#     # prev_return_25 = prcSoFar[25, -1] / prcSoFar[25, -2] - 1
#     prev_return_11 = prcSoFar[11, -1] / prcSoFar[11, -2] - 1
#     # prev_return_38 = prcSoFar[38, -1] / prcSoFar[38, -2] - 1

#     # Determine the desired position for company 38
#     if prev_return_22 > threshold and prev_return_30 > threshold: #  and prev_return_25 > threshold
#         desired_position_38 = 10000
#     elif prev_return_22 < threshold and prev_return_30 < threshold: # and prev_return_25 < threshold
#         desired_position_38 = -10000
#     else:
#         desired_position_38 = 0
    
#     # Determine the desired position for company 38
#     if prev_return_22 > threshold and prev_return_11 > threshold: #  and prev_return_38 > threshold
#         desired_position_27 = 10000
#     elif prev_return_22 < threshold and prev_return_11 < threshold: # and prev_return_38 < threshold
#         desired_position_27 = -10000
#     else:
#         desired_position_27 = 0
    
#     # Create the new position array
#     new_pos = np.zeros(nins)
#     new_pos[38] = desired_position_38
#     new_pos[27] = desired_position_27
    
#     # Calculate the change in positions
#     position_changes = new_pos - currentPos
    
#     # Apply a maximum change of 20% of the maximum allowed position
#     max_change = 10000 * change
#     position_changes = np.clip(position_changes, -max_change, max_change)
    
#     # Update current positions
#     currentPos += position_changes.astype(int)

#     return currentPos