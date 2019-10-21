##EEw382N Security Laboratory Exercise 2 Part 1 Report

Student: Ronghao Zhang

Professor: Mohit Tiwari

TA: Austin Harris

September 29, 2019

##Part 3: Kubernetes

**3a) Orchestration with Kubernetes**

**Docker Applications**

- What IP address and port does the web-service use to connect to the SQL DB? Refer to the source file src/index.php to find the answer. Explain what you see on the homepage http://localhost:8000.

  - web-service uses: 0.0.0.0:8082 which is exposed to port 3306 for the webservice to access. 

- Do necessary changes so that the web-server now serves at localhost:9000. Explain the change and give screenshots.

  - I made changes to the docker-compose.yaml file. And here is the code that I changed:

  ```
  website:
      container_name: php72
      build:
        context: ./
      ports:
        - 9000:80
  ```

  - Here is a screenshot of the web-server after the port is changed to 9000

  ![a3](/Users/Ron/Desktop/NetworkSecurity/Lab2-2/a3.png)

**Install Kubernetes**

- Check the deployment of pods (containers) by microk8s.kubectl get pods. Check the service by microk8s.kubectl get services. You can get all pods and services by adding the keyword --all-namespaces to each of the above commands. Provide screenshots for both. What are the different namespaces you observe?

  - Below is the screen shot of get pods and services from default namespace and all namespaces. I can see that all the deployments installed using the previous yaml files were put into the default namespaces. And the apps such as registry and dashboard were installed in the cube-system namespaces. 

  ![3a-2](/Users/Ron/Desktop/NetworkSecurity/Lab2-2/3a-2.png)

- Explain the output of deployments and services. Where do we specify how many instances of each application is to be deployed?

  -  Below is the output of deployments, and we can see that it is expected to have 3 instances of webserver and 1 instance of mysql running.
  
  ```
  class@class-VirtualBox:~/Desktop/simplePhpSQL_k8s$ sudo kubectl get deployments
  NAME        READY   UP-TO-DATE   AVAILABLE   AGE
  mysql       0/1     1            0           5m45s
  webserver   0/3     3            0           5m46s
  ```
  
  - In order to specify the number of instances of each application, we make changes to the `webserver.yaml` file, and change the replicas.   
  
  ```
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: webserver
    labels:
      app: apache
  spec:
    replicas: 3
  ```
  
- Change the deployment to have 2 instances of web-servers and submit the screenshots.

  - After changing the `replicas`from 3 to 2 and run apply -f command, we get an updated deployment  with 2 instances of web-servers running. Below is the sceenshot:

  ![3a-3](/Users/Ron/Desktop/NetworkSecurity/Lab2-2/3a-3.png)

- Some toubleshoots:

  Q: When I was trying to do docker push, it says `Get http://localhost:32000/v2/: dial tcp 127.0.0.1:32000: connect: connection refused`

  A: But if I comment out the line below from my /etc/hosts `#::1 localhost ip6-localhost ip6-loopback`, it worked. 

**RBAC**

- On what port did you expose the dashboard service and how did you find it?

  -  Port 31234 is where I exposed the dashboard service. I found it from `kubectl -n kube-system get svc` and here is the returned information:
  
    ```
    kubernetes-dashboard        NodePort    10.152.183.245   <none>        443:31234/TCP
    ```
  
- Explain the Dashboard when you login using the user-sa service account. Do you see all the pods that you see when you run microk8s.kubectl get pods --all-namespaces? Why or why not?

  -  No, there was nothing showed up on the dashboard using the user-sa service account for any of the namespaces except for `default` 

  - The reason why I can't get information from any namespace is becasue the way user-role was defined:

    ```
  rules:
    - apiGroups: [""]
    resources: ["pods"]
      verbs: ["get", "watch", "list"]
    ```

  - According to the official RBAC document on the K8s website https://kubernetes.io/docs/reference/access-authn-authz/rbac/ This role only has the clearance to check pods on the `default` namespace. 

- Create another service account which can access just the kube-system namespace. This service should have properties get, list, create, update & delete. Provide code and steps how you achieved this. Provide screenshots of the Dashboard.

  - Create a new Service Account in the namespace `kube-system` using the following command:

    `sudo kubectl create sa pod-operator-sa --namespace kube-system`

  - To make sure the Service Account has been created successfully, tun the following command to see if the `pod-operator` is in the list.

    `sudo kubectl -n kube-system get sa`

  - Create a new role called `system-pod-operator` inside the namespace `kube-system`. Here is the yaml file for the `new-user-role.yaml`.

    ```apiVersion: rbac.authorization.k8s.io/v1
    kind: Role
    metadata:
      namespace: kube-system
      name: system-pod-operator
    rules:
      apiGroups: [""] # "" indicates the core API group
      resources: ["pods"]
      verbs: ["get", "list", "create", "update", "delete"]
    ```

  - To make sure the new role has been created, run the following command to see if `system-pod-operator` is in the list:

    `sudo kubectl -n kube-system get role`

  - Create a role binding to assign Service Account the new Role. Here is the `new-rolebind.yaml` file: 

    ```
    kind: RoleBinding
    apiVersion: rbac.authorization.k8s.io/v1
    metadata:
      name: pod-user-rolebind
      namespace: kube-system
    subjects:
    - kind: ServiceAccount
      name: pod-operator-sa
      namespace: kube-system
    roleRef:
      kind: Role
      name: system-pod-operator
      apiGroup: rbac.authorization.k8s.io
    ```

  - Finally apply all the yaml files to create Role and Role Binding

    ```
    sudo kubectl create -f new-user-role.yaml
    sudo kubectl create -f new-rolebind.yaml
    ```

  - After logging into the dashboard using the token genrated for the `pod-operator-sa` we will be able to view and edit pods in the `kube-system` namespace. Here is a screenshot:

  ![RBAC](/Users/Ron/Desktop/NetworkSecurity/Lab2-2/RBAC.png)

**3b) Creating a kubernetes cluster for DVWA**

- All files used for the lab should be in the github repository. Mention the commands used to transfer the images into kubernetes registry in the README file. Create a commit of all the changes and submit the patch file of the change. You can create a patch by running the following command. `git diff HEAD~1..HEAD > patch.diff` This creates patch file between last two commits. If you have multiple commits, edit the git diff appropriately to encorporate all your changes.

  - I followed the following steps to transfer images to kubernetes registry

    - Enable the registry service on microk8s `microk8s.enable registry`
    - Build the image of DVWA and SQL using the Dockerfiles `docker build -t dvwa:latest` and `docker build -t sql:latest`
    - Tag the image to make sure they are pointing to the registry 
      - `docker tag <image-id> localhost:32000/dvwa:k8s`
      - `docker tag <image-id> localhost:32000/sql:k8s`
    - Push the image to the local registry `docker push localhost:32000/<image-name>`
  
  - Please check the github repo for source code:
  
    [GitHub ]: https://github.com/RonZhang724/DVWA

- Login to DVWA and try to crash the machine using a forkbomb attack. Try to access the webpage again. Does it work? Explain what happened. Show appropriate screenshots to backup your explanation.
  - I tried to run the fork bomb in the DVWA using the command injection with `; forkbomb(){ forkbomb | forkbomb & }; forkbomb`, it worked and hanged the pod as well as the .
  - The fork bomb is a function which gets called recursively from its body and cannot be killed since it is running on the background. The function calls itsself twice in the body. This will consume all resources of of Kubernetes cluster and eventually force the Linux system to crash
  - There is no sceenshot of the crash because the machine was hanged and the screen just froze on its current state (I tried set the resources limit in step 3 and captured the browser when the pod crashed). But here is a pod status after I restarted the VM. 
  
  ![3b](/Users/Ron/Desktop/NetworkSecurity/Lab2-2/3b.png)

- Edit the web-app deployment to launch multiple instances of the service instead of just one. You might want to delete the existing web-app pod by either deleting using the deployment yaml or force delete of pod using `microk8s.kubectl delete pods -n --grace-period=0 --force` Reapply the deployment yaml for the effects to take place.
  
  -  In order to scale the deployment, I ran the scale command `microk8s.kubectl scale deployment dvwa --replicas=3`
  - Here is the result returned from getting pods
  
  ![3b-2](/Users/Ron/Desktop/NetworkSecurity/Lab2-2/3b-2.png)
  
- Repeat the forkbomb and try to re-connect to the application. Does it work? Explain and provide appropritate screenshots. What could be the various DevOps use-cases of using kubernetes that you learnt from this experiment?
  
  - After dumping a fork bumb into the DVWA, same thing happened, and the VM crashed.
  - I tried changing the resource limits on the deployment as follows:
  
  ```
  ---
  resources:
    limits:
      cpu: 100m
      memory: 70Mi
  ---
  ```
  
  - After I tried the fork bomb on the DVWA, the VM is not hanged. After 10 seconds, the browser lost connection to the server. Here is a screenshot
  
  ![3b-3](/Users/Ron/Desktop/NetworkSecurity/Lab2-2/3b-3.png)
  
  - After waiting for another 30 seconds, the server was back up. Here is what I got after trying to get logs from the running pod. I noticed that all of the previous logs that contain the GET request were gone. And it seems like the cluster restarted the pod to deal with the fork bomb.
  
    ```
    [+] Starting mysql...
    Starting MariaDB database server: mysqld . . ..
    [+] Starting apache
    AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 10.1.10.55. Set the 'ServerName' directive globally to suppress this message
    Starting Apache httpd web server: apache2.
    ==> /var/log/apache2/access.log <==
    
    ==> /var/log/apache2/error.log <==
    [Fri Oct 04 04:13:59.012216 2019] [mpm_prefork:notice] [pid 311] AH00163: Apache/2.4.25 (Debian) configured -- resuming normal operations
    [Fri Oct 04 04:13:59.012334 2019] [core:notice] [pid 311] AH00094: Command line: '/usr/sbin/apache2'
    
    ==> /var/log/apache2/other_vhosts_access.log <==
    
    ==> /var/log/apache2/access.log <==
    10.1.10.1 - - [04/Oct/2019:04:14:30 +0000] "GET / HTTP/1.1" 302 337 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0"
    10.1.10.1 - - [04/Oct/2019:04:14:30 +0000] "GET /login.php HTTP/1.1" 200 1050 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0"
    10.1.10.1 - - [04/Oct/2019:04:14:32 +0000] "POST /login.php HTTP/1.1" 302 336 "http://localhost:31540/login.php" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0"
    10.1.10.1 - - [04/Oct/2019:04:14:32 +0000] "GET /setup.php HTTP/1.1" 200 2042 "http://localhost:31540/login.php" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0"
    ```

##Feedback

- What did you like/dislike about this lab? 
- I like the fact that there is not much setup steps in this lab other than pulling the image from github and installing the microk8s. 
  - I don't like the firrst question of 3b where we need to seperate the Dockerfile and create two seperate images. Not only because we haven't covered much about the Dockerfile in class, but also because we are not really familiar with the source code for sql and dvwa server. 
- Was it helpful in learning the material? 
- Yes, it is a pretty good hands on experience with the kubernetes. But the length of this lab is too long for me to actually dive into specifc topic that I am interested in. 
- Which sections were most/least helpful?
- In my opinion, the RBAC part adds a handy tool to my toolbelt, and I can myself using that tool when I work for industry clusters for security purposes. 
  - The seperating Dockfile part is the least helpful because I don't really understand 90% of the code in the Dockerfile, and it is really hard for me to find documents specific to that Dockerfile such as how it was constructed, what is the reason behind each line, etc.
- Additional comments
  - I hope we could learn more about dockerhub. How to properly use it? How to understand the tags, image history, etc. 