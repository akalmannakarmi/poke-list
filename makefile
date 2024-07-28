# Makefile

# Linux/MacOS
init:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

run:
	. venv/bin/activate && uvicorn appPokeList.main:app --host 0.0.0.0 --port 8000

dock:
	@docker stop apppokelist || true
	@docker rm apppokelist || true
	@docker rmi apppokelist || true
	@docker build -t apppokelist .
	@docker run -d -p 8000:8000\
		--name apppokelist apppokelist 

clean:
	rm -rf venv
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Windows
win-init:
	python -m venv venv
	venv\Scripts\activate && pip install -r requirements.txt

win-run:
	venv\Scripts\activate && uvicorn appPokeList.main:app --host 0.0.0.0 --port 8000

win-dock:
	@if docker stop apppokelist || true
	@if docker rm apppokelist || true
	@if docker rmi apppokelist || true
	@docker build -t apppokelist .
	@docker run -d -p 8000:8000 --name apppokelist apppokelist

win-clean:
	rmdir /s /q venv
	for /r %%d in (__pycache__) do if exist "%%d" rmdir /s /q "%%d"
