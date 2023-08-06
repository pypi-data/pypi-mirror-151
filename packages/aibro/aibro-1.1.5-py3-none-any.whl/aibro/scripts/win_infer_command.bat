python -m venv repo_venv
call .\\repo_venv\\Scripts\\activate
pip install -r %1/requirements.txt
echo "Dependencies installed!"
