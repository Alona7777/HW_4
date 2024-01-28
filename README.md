1. Built image 
```docker build . -t alona7777/hw_4:0.0.2 ```
2. Push to dockerhub
```docker push alona7777/hw_4:0.0.2```
3. run docker container
```docker run --name hw_4 -d -p 3000:3000 -v /Users/ALONA/Desktop/Go_IT/HW/WEB/HW_4/front-init/HW_4/storage:/storage alona7777/hw_4:0.0.2```
