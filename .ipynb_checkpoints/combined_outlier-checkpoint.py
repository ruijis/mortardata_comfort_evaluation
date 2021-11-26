def combined_outlier(ro, dr):
    """
    Calculate the combined index of range outlier and daily range outlier.
    
    Parameters
    ----------
    ro : float
         range outlier index value
    dr : float
         daily range outlier index value

    Returns
    ----------
    p : float
        percentage of combined index
    """
    p = (ro + dr)/2
    return round(p, 2)
    
    