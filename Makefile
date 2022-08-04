start_server:
	uvicorn app.main:app --port 3000 --reload yarn dev

start_frontend:
	cd frontend && yarn dev