Read-Host -Prompt "Did you adapt the Dockerfile?"
docker build -t portamento_test_model ../
docker run --env-file ../.env -it portamento_test_model bash