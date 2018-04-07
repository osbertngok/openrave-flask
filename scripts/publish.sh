CURR_FILE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR=${CURR_FILE_DIR}/..

cd $PROJECT_DIR/docker/openrave-flask
docker build -t openrave-flask .
docker tag openrave-flask osbertngok/openrave-flask
docker push osbertngok/openrave-flask
cd $PROJECT_DIR
docker-compose up -d
