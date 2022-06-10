build-image:
	docker build -t telegram-music-bot:v0.1 ./

start-container:
	docker run  --name telegram-music-bot -p --env-file .env - 