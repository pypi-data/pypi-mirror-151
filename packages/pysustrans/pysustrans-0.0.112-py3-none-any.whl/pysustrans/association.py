# Dependencies
# Import all of them to execute the class methods
from logging import raiseExceptions
from scipy.stats.contingency import association
import pandas as pd
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt
import seaborn as sns

"""
Calculate the association among two nominal variables

Parameters:
------------
dataframe : DataFrame
    A pandas DataFrame object.
    
method: str 
    Avilable methods are “cramer”, “tschuprow” and “pearson”. (default = “cramer”)
    
Returns:
-------
Displays a pair-wise association heatmap.
asso: A pair-wise association (matrix) pandas DataFrame object {"asso"}.
ax: A matplotlib axis object ("ax").
"""

# Class definition
class Association:
    def __init__(self, dataframe, method = "cramer"):
        self.dataframe = dataframe
        self.method = method
        self.matrix = None
        
        
    def check_df(self):
        """
        Given a dataset it checks whether the dataset is an instance of pandas DataFrame, if not then
        raises a TypeError
        """
        if isinstance(self.dataframe, pd.DataFrame):
            self.data = self.dataframe
        else:
            raise TypeError("data frame must be an instance of pd.DataFrame")
        
    def select_variable(self):
        """
        Given a dataframe it selects the "object" columns and if the DataFrame is empty it raises an 
        KeyError
        """
        self.obj_columns = self.data.select_dtypes(include = ["object"]).columns
        
        if len(self.obj_columns) == 0:
            raise KeyError("No object variables found")
        
        
        
    def pairwise_mat(self):
        """
        - Creating a 2-D array with ones on the diagonal and zeros elsewhere [np.eye( )].
        - Converting it to a pandas DataFrame
        """
        self.matrix = pd.DataFrame(
            np.eye(len(self.obj_columns)),
            columns = self.obj_columns,
            index = self.obj_columns
        )
        
        
        
    def compute_pair(self):
        """
        combinations from itertools used for generating pair-wise combination
        Example:
            col_names = ["sex", "smoker", "day", "time"]
            
            # size of combination is set to 2
            a = combinations(col_names, 2) 
            y = [(i, j) for i, j in a]
            print(y)
            
            Output: [('sex', 'smoker'), ('sex', 'day'), ('sex', 'time'), ('smoker', 'day'), ('smoker', 'time'), ('day', 'time')]
        """
    
        n = len(self.obj_columns)
        all_combination = combinations(self.obj_columns, r = 2) # `r`: size of combination; here set to 2
        
        # Iterating through combinations
        for comb in all_combination:
            i = comb[0]
            j = comb[1]
            
            # crosstab calculation
            ctab = pd.crosstab(self.data[i], self.data[j])
            # Computing association value based on supplied method
            val = round(association(ctab, method = self.method), 2)
            # Adding value to the matrix
            self.matrix[i][j], self.matrix[j][i] = val, val  
        
        return self.matrix
        
        
                    
    def generate_plot(self):
        
        """
        This function generates a heatmap.
        
        """
        
        tempdf = self.compute_pair()
        ax = sns.heatmap(tempdf,
                         annot = True,
                         cbar = True,
                         vmin = 0,
                         vmax = 1,
                         cmap = "Blues")

        
        # Changing tick parameters size and rotation.
        ax.tick_params(axis = "x", labelsize = 12, labelrotation = 90)
        ax.tick_params(axis = "y", labelsize = 12, labelrotation = 0)
        
        return ax         
        
             
                
    def fit(self):
        """
        After calling the Association class on dataset, the user need to call the .fit() method.
        - 1. check_df( ): It will check for the dataframe.
        - 2. select_variables( ): Then selecting the object variables
        - 3. pairwise_mat( ): Creating pairwise empty matrix.
        - 4. compute_pair( ): Calculating pair-wise association matrix
        - 5. generate_plot( ): Generates a pair-wise heatmap.
        The fit( ) method returns the association matrix and axis object
        - {"asso":self.compute_pair(), "ax":self.generate_plot()}
        
        """
        self.check_df()
        self.select_variable()
        self.pairwise_mat()
        
        # The method returns a pair-wise matrix and am axis plot object
        return {"asso":self.compute_pair(), "ax":self.generate_plot()}
       