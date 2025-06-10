# upathway-robot-facade

## Deploy

## SUBMODULES
- Add submodules
    ```
    git submodule add --force -b develop https://dev-git.labs.gmv.com/industry-hub/tools/wrappers/apirest-fastapi-wrapper.git src/apirest-fastapi-wrapper
    git submodule add --force -b develop https://dev-git.labs.gmv.com/industry-hub/tools/wrappers/logger.git src/logger 
    git submodule add --force -b develop https://dev-git.labs.gmv.com/industry-hub/tools/wrappers/mqtt-wrapper-v2.git src/mqtt-wrapper
    ```
- Init submodules
    ```
    git submodule init
    git submodule update
    ```
### Makefile
- Build image
    ```
    make build
    make build-no-cache
    ```

- Run container
    ```
    make up
    ```
- Stop container
    ```
    make down
    ```
- Logs 
    ```
    make logs
    make logs-f
    ```
### Direct Docker Commands

- Build image
    ```
    sudo docker build --tag upathway-robot-facade:0.0.0 -f docker/Dockerfile .
    sudo docker build --tag upathway-robot-facade:0.0.0 --no-cache -f docker/Dockerfile .
    ```

- Run container
    ```
    docker-compose up -d
    ```
- Stop container
    ```
    docker-compose down
    ```
- Logs 
    ```
    docker logs -f --tail 200 upathway-robot-facade
    docker compose logs -f
    ```


