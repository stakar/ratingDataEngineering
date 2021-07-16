from tools.tools import *

#get directories with subjects
dir_list = get_subject_dir(PATH)
#get data frame with results
results_df =  get_result_dir(dir_list)
# save results
save_results(results_df)
