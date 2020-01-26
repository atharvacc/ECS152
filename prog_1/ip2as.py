
#Import libraries
import numpy as np
import pandas as pd 
from netaddr import *
import sys






### Helper Functions
def clean_prefix(prefix_string):
    """
    clean_prefix: Takes in the prefix string, removes the "."s and returns an int.
            Args:
                (String) prefix_string: string to be cleant
            Returns:
                (int) clean_string: int with values of the prefix string
    """
    clean_string = int(prefix_string.replace(".",""))
    return clean_string

    

def prefix_match(input_string, DB):
    """
    prefix_match: Takes in an input string, and finds the longest prefix match
            Args:
                (String) input_string: input from for which to find the longest prefix match
                (DataFrame) DB: DataBase containg a column prefix that contains all of the possible
                                prefixes
            Returns:
                (DatFrame) output_df: Output DataFrame containing the closest prefix match
                                      and its AS Number
    """
    str_len = len(input_string)  # Find length of input string
    output_df = DB[DB.Prefix.str.match(input_string[0])].reset_index(drop = True)  # Initialize DataFrame
    m,_ = output_df.shape
    if (m == 1):
        return output_df
    idx = 1
    while( not(output_df.empty) and (idx<str_len+1)):
        output_df = DB[DB.Prefix.str.match(input_string[0:idx])].reset_index(drop = True)
        idx = idx +1
    output_df = DB[DB.Prefix.str.match(input_string[0:idx-2])].reset_index(drop = True)
    m,_ = output_df.shape
    if (m == 1):
        return output_df
    output_df = distance_match(input_string, output_df)      
    return output_df

def distance_match(input_string, df_bestmatch):
    """
    distance_match: Find the best match to input_string from df_bestmatch
                Args:
                     input_string: string for which to find the best match
                     df_bestmatch: DataFrame with a prefix column containg the
                                   potential candidates
               Returns:
                      output_df:  Row in dataframe with the best match 
    """
    clean_input = clean_prefix(input_string)
    int_bestmatch = np.array(list(map(clean_prefix, df_bestmatch.Prefix.values.tolist())))
    dist = int_bestmatch - clean_input
    idx = np.where(dist == min(dist))[0]
    if (len(idx) == 1):
        return df_bestmatch[idx].reset_index(drop=True)
    else:
        df_bestmatch = df_bestmatch.iloc[idx,:]
        temp = []
        for prefix, prefix_length in zip(df_bestmatch.Prefix, df_bestmatch.Prefix_length):
            temp.append(prefix + "/" + str(prefix_length))
        df_bestmatch["Prefix_full"] = temp
        prefix_list = df_bestmatch.Prefix_full.tolist()
        df_bestmatch = df_bestmatch[[isIn(p, input_string) for p in prefix_list]].reset_index(drop = True)
        best_prefix = df_bestmatch.Prefix_length.idxmax()
        return df_bestmatch.iloc[best_prefix:best_prefix+1].reset_index(drop = True)
        
def convert_ip(ip):
    return '.'.join([bin(int(x)+256)[3:] for x in ip.split('.')])

def isIn(prefix_full, input_string):
    ip = IPNetwork(prefix_full)
    list_1 =  list(map(str,list(ip)))
    if input_string in list_1:
        return True
    else:
        return False
    
def iplist_convert(iplist,DB):
    """
    iplist_convert: Takes in a list of string to be matched and performs longest prefix match
            Args:
                (numpyarray) iplist: numpy array with all of the iplists
                (DataFrame) DB     : Dataframe with prefixes, prefix length, and AS number
            Returns: 
                    output: output in the format expected
    """
    m,_ = iplist.shape
    cols = ["Prefix", "AS", "Input"]
    output_df = pd.DataFrame(columns=cols)
    for i in range(m):
        match = prefix_match(iplist[i][0], DB)
        match.Prefix = match.Prefix[0] + "/" + str(match.Prefix_length[0])
        match["Input"] = iplist[i][0]
        match = match[cols]
        output_df = pd.concat((output_df,match))
    return output_df
        
        
        

def main():
    args = sys.argv
    db_file = args[1]
    iplist_file = args[2]
    df = pd.read_csv(db_file, sep=" ", header=None)
    iplist = pd.read_csv(iplist_file, sep=" ", header=None).values
    df.columns = ["Prefix", "Prefix_length", "AS"]
    out = iplist_convert(iplist, df)
    out.to_csv('student_output.txt', sep=' ', index = False, header=False)

main()



