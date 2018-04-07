curl http://localhost:8080/scenes && echo
curl -F "file=@../docker/openrave-flask/python-restful-api/tests/test_files/hanoi.env.xml" http://localhost:8080/scenes && echo
curl http://localhost:8080/scenes/hanoi.env.xml && echo
curl http://localhost:8080/scenes && echo
curl -X DELETE http://localhost:8080/scenes/hanoi.env.xml && echo
curl http://localhost:8080/scenes/hanoi.env.xml && echo

