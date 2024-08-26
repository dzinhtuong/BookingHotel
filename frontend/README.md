------RUN ON LOCAL-------
1. Install NodeJs
2. Open terminal and cd /frontend
    - run command: `npm install`
    - run command: `npm start`

-----RUN with Docker---------
1. Open terminal and cd /frontend
    - Build Image: 
        `docker build -t [image_name]` .

2. Run a Docker container from image:
        `docker run -p 3000:3000 --name [container_name] [image_name]`

3. `docker exec -it [container_name] /bin/sh`
