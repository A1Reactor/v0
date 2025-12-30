install:
	python -m pip install -r requirements.txt
	python -m pip install -e .

api:
	uvicorn a1_reactor.server.api:app --host 0.0.0.0 --port 8080

demo:
	python -m a1_reactor.cli demo --prompt "cinematic street shot, shallow depth of field"

test:
	pytest -q

self-check:
	python -m a1_reactor.tools.self_check
