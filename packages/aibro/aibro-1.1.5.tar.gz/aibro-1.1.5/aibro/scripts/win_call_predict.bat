call .\\repo_venv\\Scripts\\activate
cd %1
python3 -c """ from predict import *; model = load_model(); result = run(model) """
echo "Prediction finished without error"
