sudo kill -9 `sudo lsof -t -i:5000` 2> /dev/null
sudo kill -9 `sudo lsof -t -i:5001` 2> /dev/null
sudo kill -9 `sudo lsof -t -i:5002` 2> /dev/null

echo "Web Application Shutdown"