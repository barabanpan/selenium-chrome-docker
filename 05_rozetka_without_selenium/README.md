# selenium-chrome-docker
Automation with selenium and docker

# RUN
1. Create .env with credentials for rozetka as in .env.example.
2. For remote first run ```docker-compose up --remove-orphans```
3. ```python run.py remote``` OR ```python run.py local```
4. ```chmod 755 bot/driver/chromedriver_96_linux``` if there are any problems with linux driver
