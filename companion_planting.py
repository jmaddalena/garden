import pandas as pd
import numpy as np

def fill_row(adj_df, row_list, row_length):
    """ recursive function to combine squares into rows only if rows compatable side-by-side"""

    new_row_list = []
    
    for squares in row_list:
        
        current_square_row = adj_df.loc[squares[-1]]
        next_squares = current_square_row.loc[current_square_row == 1].index
        
        if len(next_squares) > 0:

            for next_square in next_squares:
                
                new_row = squares + [next_square]
                
                new_row_list.append(new_row)
    
        else:
            new_row = []
            
    if len(new_row) == 0:
        return []
    elif len(new_row) == row_length:    
        return new_row_list
    else: 
        return fill_row(adj_df, new_row_list, row_length)    
    
def get_all_rows(adj_df, row_length):
    """ get all possible rows of specified length using `fill_row()` for each possible starting square"""
    all_start_squares = adj_df.index
    
    all_rows = []
    
    for start_square in all_start_squares:
        start_square_rows = fill_row(adj_df, [[start_square]], row_length)
    
        if len(start_square_rows) > 0:
            all_rows = all_rows + start_square_rows
        
    return all_rows
    
def compatable_rows(adj_df, row1, row2):
    
    # if row1 is actually a bed
    if len(np.array(row1).shape) > 1:
        row1 = row1[-1]
    
    compatability_list = []

    for i in range(len(row1)):
        item1 = row1[i] 
        item2 = row2[i]

        if (adj_df.loc[item1, item2] == 1 or adj_df.loc[item2, item1] == 1) and item1 != item2:
            compatable = True
        else:
            compatable = False
            
        compatability_list.append(compatable)
        
    return all(compatability_list)


def fill_bed(adj_df, all_rows, bed_list, bed_height):
    """ recursive function to combine rows into bads of certain height only if rows compatable side-by-side"""
    
    new_bed_list = []

    for bed in bed_list:
        
        remaining_rows = [row for row in all_rows if row not in bed]

        if len(remaining_rows) > 0:
            
            for next_row in remaining_rows:

                if compatable_rows(adj_df, bed, next_row):
                    
                    new_bed = bed + [next_row]
                    
                    new_bed_list.append(new_bed)
        
        else:
            new_bed = []
           
        if len(new_bed_list) == 0:
            return []
        elif len(new_bed) == 0:
            return []
        elif len(new_bed) == bed_height:
            return new_bed_list
        else:
            return fill_bed(adj_df, all_rows, new_bed_list, bed_height)
    
def get_beds_from_rows(adj_df, all_rows, bed_height):
    """ get all possible beds of specified height using `fill_bed()` for each possible starting row"""

    all_beds = []
    
    for start_row in all_rows:
        start_row_beds = fill_bed(adj_df, all_rows, [[start_row]], bed_height)
    
        if len(start_row_beds) > 0:
            all_beds = all_beds + start_row_beds
        
    return all_beds

def get_all_beds(adj_df, row_length, bed_height):

    all_rows = get_all_rows(adj_df, row_length)        

    all_beds = get_beds_from_rows(adj_df, all_rows, bed_height)

    return all_beds
