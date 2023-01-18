#!/bin/bash

# python3 main.py -pf -v N -vv 100 200 300 400 500 -df 1 -rp 'result_remote/tp-ct-var-N' -fop 'paper_figs/tp-ct-var-N' -st CT

# python3 main.py -pf -v S -vv 0 0.2 0.4 0.6 0.8 1.0 1.2 -df 1 -rp 'result_remote/ww-ct-var-zipf-n1000' -fop 'paper_figs/ww-ct-var-zipf-n1000' -st CT -rt 10

python3 main.py -pf -v BS -vv 5 10 15 20 25 30 32 -df 2 -rp 'result_remote/bait-and-switch-wo-fpcs-s2' -fop 'paper_figs/bait-and-switch-wo-fpcs-s2' -st DS -rt 100

# python3 main.py -pf -v BS -vv 5 10 15 20 25 30 32 -df 2 -rp 'result_remote/bait-and-switch-wo-fpcs-s2' -fop 'paper_figs/bait-and-switch-wo-fpcs-s2' -st DS -rt 100

# python3 main.py -pf -v N -vv 100 -df 1 -rp 'result/ds-s0.9-n100' -fop 'paper_figs/ds-s0.9-n100' -st DS -rt 1