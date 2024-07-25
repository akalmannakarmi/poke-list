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