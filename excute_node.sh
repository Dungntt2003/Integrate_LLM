#!/bin/bash

cd /media/dell/"New Volume"/lib_python
source llm_env/bin/activate

cd /home/dell/Crawl/explore

python manyLinks.py
python chunk_clean.py
python transform.py
