# PodCatch!
This is an python supported web application using the Flask backend. 
## Install
- Clone the repo
``` sh
git clone https://github.com/podcast-ai/podcast-ai-lab
```
- Install Conda: please see https://docs.conda.io/en/latest/miniconda.html
- Create Conda env:


Running following command to install all the dependency packages
``` Linux
conda create -n podcatch python=3.10
conda activate podcatch
pip install -r requirements.txt
```


Then simply run the app.py to render the server. 
``` Linux
python app.py 
```


| variable  |   type |             default             |                                      description | generated method |
|:----------|-------:|:-------------------------------:|-------------------------------------------------:|:-----------------|
| sentence  | string |              none               |                       The user text query input. | automatic        |
| fileName  | string | ./static/data/sample-000000.mp3 |               The file name that chosen to play. | python backend   |
| startTime |  float |              none               | The starting time for the chosen file to render. | python backend      |
| endTime   |  float |              none               |   The ending time for the chosen file to render. | python backend      |


### Main Search Window
<div align="center">
  <img src="./app/static/img/front_UI.png" width = "100%" height = "100%">
</div>

### Result Window
<div align="center">
  <img src="./app/static/img/render_UI.png" width = "100%" height = "100%">
</div>
