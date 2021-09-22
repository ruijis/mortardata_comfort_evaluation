def qualify_plus(df, sub):
    """
    group a pandas dataframe by a column
    
    Parameters
    ----------
    df : object
         a pandas dataframe that stores metadata information
    sub: str
         a column name of the dataframe for grouping
         
    Returns
    ----------
    l : list
        a list of qualifed names for the sub-category
    """
    g = df.groupby([sub])
    l = list(g.groups)
    return l 
    
    