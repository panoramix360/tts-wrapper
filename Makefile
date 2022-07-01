.PHONY: api_tests tests publish act-build cov.xml mypy

tests:
	pytest -s -m "not slow"

all_tests:
	source .secrets/.env && \
	export POLLY_REGION POLLY_AWS_ID POLLY_AWS_KEY && \
	export MICROSOFT_KEY && \
	export GOOGLE_SA_PATH && \
	export WATSON_API_KEY WATSON_API_URL && \
	pytest -s

publish:
	poetry publish --build

act-build:
	act --secret-file .secrets/.env -a build

requirements.txt: pyproject.toml
	poetry export --without-hashes -E google -E watson -E polly -E microsoft -f requirements.txt -o requirements.txt
	# it seems like sapi dependencies are not being generated correctly, so we'll manually add them here
	echo "pyttsx3==2.90" >> requirements.txt

requirements.dev.txt: pyproject.toml requirements.txt
	poetry export --dev --without-hashes -f requirements.txt -o requirements.dev.txt

cov.xml:
	poetry run pytest --cov-report xml:cov.xml --cov=tts_wrapper -m "not slow"

mypy:
	poetry run mypy $$(git ls-files '*.py')