docker rmi -f portamento_test_model
docker build -t portamento_test_model ../
docker run --env-file ../.env -it portamento_test_model bash
Read-Host -Prompt "Press Enter to exit"