run:
	docker-compose up
	echo "\n\nDB and App running, don't forget to run \"make stop\" or \"docker-compose down\" when you're finished"
first-run:
	docker-compose up -d --build
	echo "Waiting for db to start" && sleep 10
	python clean_data.py
	echo "\n\nDB and App running, don't forget to run \"make stop\" or \"docker-compose down\" when you're finished"
stop:
	docker-compose down
