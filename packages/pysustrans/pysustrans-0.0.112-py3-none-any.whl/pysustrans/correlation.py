import scipy.stats as ss
import pandas as pd
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt
import seaborn as sns

"""
Calculate the correlation among two numeric variables

Parameters:
------------
dataframe : DataFrame
    A pandas DataFrame object.
    
method: str 
    Avilable methods are "pearson", "spearman" and "kendalltau". (default = “pearson”)
    
Returns:
-------
Displays a pair-wise correlation heatmap.
corr_mat: A pair-wise correlation (matrix) pandas DataFrame object {"corr_mat"}
corr_df: A pair-wise correlation matrix with associated p-values in pandas DataFrame object format {"corr_df"} 
ax: A matplotlib axis object ("ax")
"""

# Class definition
class Correlation:
    def __init__(self, dataframe, method = "pearson"):
        self.dataframe = dataframe
        self.method = method
        self.matrix = None
        self.corr_list = []
        self.pval_list = []
        self.comb_list = []
        
        
        
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
        self.obj_columns = self.data.select_dtypes(include = ["number"]).columns
        
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
            
            if self.method == "pearson":
            # Computing correlation value based on pearson's method
                val, p_val = ss.pearsonr(x = self.data[i],
                                               y = self.data[j])
            
            elif self.method == "spearman":
            # Computing correlation value based on spearman method
                val, p_val = ss.spearmanr(a = self.data[i],
                                                b = self.data[j])
                
            elif self.method == "kendalltau":
            # Computing correlation value based on kendalltau method
                val, p_val = ss.kendalltau(x = self.data[i],
                                                y = self.data[j])
            
            else:
                 raise KeyError("Mtheod not found")
                
            # Adding value to the matrix
            self.matrix[i][j], self.matrix[j][i] = round(val, 2), round(val, 2)
            
            # Added values of combination, corr and p-val to list 
            self.comb_list.append(comb)
            self.corr_list.append(round(val, 3))
            self.pval_list.append(round(p_val, 3))
            
            # Generated a dataframe
            corr_df = pd.DataFrame({"Variable-Pair":self.comb_list,
                                    "Correlation (r)": self.corr_list,
                                    "p-val": self.pval_list})
              
        
        return (self.matrix, corr_df.loc[0:(corr_df.shape[0]/2)-1, :])
        
        
                     
    def generate_plot(self):
        
        """
        This function generates a heatmap.
        
        """
        
        tempdf = self.compute_pair()[0]
        ax = sns.heatmap(tempdf,
                         annot = True,
                         cbar = True,
                         vmin = -1,
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
        return {"corr_mat":self.compute_pair()[0],
                "corr_df":self.compute_pair()[1],
                "ax":self.generate_plot()}
       