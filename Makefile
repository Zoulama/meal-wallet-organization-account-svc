setup: ##@Install Dependencies
	python3 -m venv ~/.virtualenvs/meal-wallet-organization-account-svc
	source ~/.virtualenvs/meal-wallet-organization-account-svc/bin/activate
	pip3 install -r requirements.txt
up: ##@Run locally
	docker-compose up --build
down: ##@Stop containers
	docker-compose down
deploy: ##@Build and deploy to Cloud Run
	gcloud builds submit --tag gcr.io/meal-wallet-test-256011/meal-wallet-organization-account-svc
	gcloud beta run deploy --image gcr.io/meal-wallet-test-256011/meal-wallet-organization-account-svc --platform managed --allow-unauthenticated
