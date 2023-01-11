from enum import IntEnum
import numpy as np

class Score(IntEnum):
    MATCH = 5
    MISMATCH = -4
    GAP = 4

class Trace(IntEnum):
    STOP = 0
    LEFT = 1 
    UP = 2
    DIAGONAL = 3

s1 = 'GGTCAGCTAAGCTAAC'
s2 = 'GGTACGCATAGCTAAC'

def matrix(s1, s2):
    row = len(s1) + 1
    col = len(s2) + 1
    matrix = np.zeros(shape=(row, col), dtype=np.int)  
    tracing_matrix = np.zeros(shape=(row, col), dtype=np.int)  
    
    max_score = -1
    max_index = (-1, -1)
    
    for i in range(1, row):
        for j in range(1, col):
         
            match_value = Score.MATCH if s1[i - 1] == s2[j - 1] else Score.MISMATCH
            diagonal_score = matrix[i - 1, j - 1] + match_value
            
            vertical_score = matrix[i - 1, j] + Score.GAP
            
            horizontal_score = matrix[i, j - 1] + Score.GAP
            
            matrix[i, j] = max(0, diagonal_score, vertical_score, horizontal_score)
            
            if matrix[i, j] == 0: 
                tracing_matrix[i, j] = Trace.STOP
                
            elif matrix[i, j] == horizontal_score: 
                tracing_matrix[i, j] = Trace.LEFT
                
            elif matrix[i, j] == vertical_score: 
                tracing_matrix[i, j] = Trace.UP
                
            elif matrix[i, j] == diagonal_score: 
                tracing_matrix[i, j] = Trace.DIAGONAL 
                
            if matrix[i, j] >= max_score:
                max_index = (i,j)
                max_score = matrix[i, j]
    
    aligned_s1 = ""
    aligned_s2 = ""   
    current_aligned_s1 = ""   
    current_aligned_s2 = ""  
    (max_i, max_j) = max_index
    

    while tracing_matrix[max_i, max_j] != Trace.STOP:
        if tracing_matrix[max_i, max_j] == Trace.DIAGONAL:
            current_aligned_s1 = s1[max_i - 1]
            current_aligned_s2 = s2[max_j - 1]
            max_i = max_i - 1
            max_j = max_j - 1
            
        elif tracing_matrix[max_i, max_j] == Trace.UP:
            current_aligned_s1 = s1[max_i - 1]
            current_aligned_s2 = '-'
            max_i = max_i - 1    
            
        elif tracing_matrix[max_i, max_j] == Trace.LEFT:
            current_aligned_s1 = '-'
            current_aligned_s2 = s2[max_j - 1]
            max_j = max_j - 1
            
        aligned_s1 = aligned_s1 + current_aligned_s1
        aligned_s2 = aligned_s2 + current_aligned_s2
    
   
    aligned_s1 = aligned_s1[::-1]
    aligned_s2 = aligned_s2[::-1]
    
    return aligned_s1, aligned_s2

    output_1, output_2 = matrix(aligned_s1, aligned_s2)
    
    print(output_1 + '\n' + output_2)