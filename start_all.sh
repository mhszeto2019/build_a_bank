#!/bin/bash
declare -A fast
fast[account]=8000
fast[transaction]=8001
fast[ledger]=8002

for i in "${!fast[@]}"
do
    echo "fastapi ${i} ${fast[$[i]]}"
    tmux new-session -d -s ${i}_fast "bash"
    tmux send-keys -t ${i}_fast "source ~/environments/cdc_env/bin/activate" ENTER
    # tmux send-keys -t ${i}_fast "cd ../" C-m
    tmux send-keys -t ${i}_fast "uvicorn app.${i}:app --reload  --port ${fast[${i}]} --host 0.0.0.0" ENTER
    


done

