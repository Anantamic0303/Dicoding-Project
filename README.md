# Setup Environment - Anaconda
```
bash
conda create --dashboard python=3.9
conda activate dashboard
pip install -r requirements.txt
```
# Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```
# Run Streamlit App
```
streamlit run dashboard.py
