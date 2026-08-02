# Reusable, safe deploy command
# To re-run it any time you change code in main.py, extract.py, chunk_utils.py, store.py, config.py or clean_text.py

cd C:\Users\lisaf\Documents\Thesis\Thesis-project\smart_study_companion\cloud_function

gcloud functions deploy smartstudy-ingest --gen2 --region=europe-west1 --trigger-location=eu --runtime=python312 --source=. --entry-point=process_pdf --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" --trigger-event-filters="bucket=smartstudy-thesis-competition" --set-env-vars="GOOGLE_CLOUD_PROJECT=smartstudy-thesis" --update-secrets="MONGODB_URI=mongodb-uri:latest" --memory=1Gi --timeout=300s

# If the Mongo PW ever needs to change again, the process is different from redeploying, but you need to update the secret's value
echo "mongodb+srv://lisafadelli:NEW_PASSWORD@smartstudy.tjnlu1j.mongodb.net/?appName=smartstudy" | gcloud secrets versions add mongodb-uri --data-file=-
# Then redeploy with the same command above

# Next actual step, test it: upload a PDF to the bucket and watch the logs
gcloud storage cp path\to\some-test.pdf gs://smartstudy-thesis-competition/some-test.pdf
gcloud functions logs read smartstudy-ingest --region=europe-west1 --limit=50

# Redeploy and re-trigger
gcloud functions deploy smartstudy-ingest --gen2 --region=europe-west1 --trigger-location=eu --runtime=python312 --source=. --entry-point=process_pdf --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" --trigger-event-filters="bucket=smartstudy-thesis-competition" --set-env-vars="GOOGLE_CLOUD_PROJECT=smartstudy-thesis" --update-secrets="MONGODB_URI=mongodb-uri:latest" --memory=1Gi --timeout=300s

gcloud storage cp "C:\Users\lisaf\Documents\Thesis\Thesis-project\docs\How_the_European_Union_works_2023.pdf" gs://smartstudy-thesis-competition/
gcloud functions logs read smartstudy-ingest --region=europe-west1 --gen2 --limit=15 --format="value(log)"