```bash

 python3 ../Bonsai-data-representation-main/bonsai/create_config_file.py \           
  --new_yaml_path   /Users/aliyz/Documents/Personal/Masters/2nd-structure-all/2nd-structure/run_bonsai/my_config.yaml \
  --dataset         my_data \                                                                                                                    
  --data_folder     /Users/aliyz/Documents/Personal/Masters/2nd-structure-all/2nd-structure/run_bonsai/data_folder/ \
  --results_folder  /Users/aliyz/Documents/Personal/Masters/2nd-structure-all/2nd-structure/run_bonsai/results/my_data/ \
  --input_is_sanity_output False \
  --filenames_data  features.txt
  --verbose True \
  --input_is_sanity_output False \
  --zscore_cutoff 1.0 \
  --UB_ellipsoid_size 1.0 \
  --skip_greedy_merging False \
  --skip_redo_starry False \
  --skip_opt_times False \
  --skip_nnn_reordering False \
  --nnn_n_randommoves 200 \
  --nnn_n_randomtrees 2 \
  --pickup_intermediate False \
  --use_knn 10

python3 ../Bonsai-data-representation-main/bonsai/bonsai_main.py \                  
  --config_filepath /Users/aliyz/Documents/Personal/Masters/2nd-structure-all/2nd-structure/run_bonsai/my_config.yaml \                                                                                   
  --step all

python3 ../Bonsai-data-representation-main/bonsai_scout/bonsai_scout_preprocess.py \
--results_folder /Users/aliyz/Documents/Personal/Masters/2nd-structure-all/2nd-structure/run_bonsai/results/my_data/ \ 
--annotation_path /Users/aliyz/Documents/Personal/Masters/2nd-structure-all/2nd-structure/run_bonsai/labels.tsv \
--take_all_genes False \
--config_filepath ''

python3 ../Bonsai-data-representation-main/bonsai_scout/run_bonsai_scout_app.py \   
--results_folder /Users/aliyz/Documents/Personal/Masters/2nd-structure-all/2nd-structure/run_bonsai/results/my_data/ \ 
--settings_filename /Users/aliyz/Documents/Personal/Masters/2nd-structure-all/2nd-structure/run_bonsai/results/my_data/bonsai_vis_settings.json \
--port 1234
```
