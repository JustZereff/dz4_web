Docker билдить так: docker build . -t my_site
Docker запускать такой строкой: docker run -d -p 3000:3000 -v my_data_volume:/app/storage my_site
И все равно, не получилось сделать сохранение локальным в папку с проектом, файл Json обновляется только в контейнере Docker
