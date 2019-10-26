# Networking

#### Networking Basics

- IP

  - How to get IP address of wikipedia.org?

    `nslookup wikipedia.org`

- DNS (Domain Name System): used to transfer domain names into actual IP addresses

  How does your local DNS server know where to go? It goes through three layers:

  - Root DNS server (13 labeled A-M)
  - Top Level Domain (TLD) server (com, org, edu)
  - Authoritative DNS server (amazon.com, utexas.edu)

- IPv4: 

  Limitations of IPv4:

  - allows only 4 billion unique addresses (32bit address)

- IPv6:

  Compared to IPv4:

  - allows 300 tri-tri-trillion addresses (128bit address)

- CIDR: Classless Inter-Domain Routing

  - Notation for talking about ranges of IP address.

  ```
  192.168.60.55 /20
  Network ID:		| | | | |
  Broadcast ID:	| | | | |
  Usable IPs: 	
  128 64 32 16 8 4 2 1
  (1) /20 means 20 bits are turned on
  (2) 8 bit rotation that represent 20 bits turned on:
  		11111111.11111111.11110000.00000000
  (3) so the subnet for this IP is
  		255.255.240.0
  (4) represent 60 in the IP in binary
  		xxxxxxxx.xxxxxxxx.00111100.xxxxxxxx
  (5) AND the above binarys from step (2) and (4) will give us Network ID:
  		11111111.11111111.00110000.00000000
  		Network ID = 192.168.48.0
  (6) To find braodcast ID, get last bit that was turned on from step (2)
  		Broadcast ID[2] = 48 + 16 - 1 = 63
  		Broadcast ID = 192.168.63.255
  (7) Actual range we can use: (notice we can't assign .0 or .255)
  		192.168.48.1 - 192.168.63.254 
  
  172.10.85.60/22
  11111111.11111111.11111100.00000000
  subnet: 255.255.253.0
  xxxxxxxx.xxxxxxxx.01010101.xxxxxxxx
  11111111.11111111.01010100.00000000
  network id: 172.10.84.0
  broadcast id: 172.10.87.255
  ```

  

- Tor (The Onion Router): secure browser

  - The Tor network disguises your identity by moving your traffic across different Tor servers, and encrypting that traffic so it isn't traced back to you.
  - It is not perfect because attackers can block users' cooncetion to tor by:
    -  blocking the directory authorities
    - blocking all relay IP addresses in the directory
    - filtering based on Tor's network fingerprint
    - preventing users form finding the Tor software
    - collecting data from the Tor exit node

- VPN (Virtual Private Network): a private network that uses a public network to connect remote sites or users together

  - Mask your IP address to provide privacy
  - Protect private data over public wifi
  - Allow access to geo-restricted content

- SSL (Secure Sockets Layer): secured protocol developed for sending info over internet

  - Protects data by encrypting every bit of information
  - Affirms website identity by enforcing validation process through Certificate Authority (CA)

- HTTP protocol:

  - An HTTP response has the following components:
    - Status line that contains status code and reason message
    - Response header files (content-typr: text/html)
    - An empty line
    - An optional message body

  

#### Networking Tools

- whois: gives additional inforamtion about the IP address from whois database
  - `whois 23.185.0.4 `
- nslookup: 
- Wireshark 
  - What is happening in the following `pcap` file https://drive.google.com/open?id=1qAbSRA5Y1zdDlZN-1k1bmDMfRVZyoGCg
- traceroute: 
  - Tries to find all the intermediary machines to a host
  - `-T`: Use TCP SYN for tracerouting (default port is 80)
  - `-I`: Use ICMP ECHO for tracerouting

####Networking Layers

- What does each networking layer do (Physical, Ethernet, IP, TCP, HTTP)? 

  [check this out]: https://www.webopedia.com/quick_ref/OSI_Layers.asp#OSI-1	"Check this out"

  - Physical (Ehternet):
  - Network (IP):
  - Transport (TCP, UDP):
  - Application (HTTP):



#Osquery

####OS Basics

- OS: <u>system software that manages computer hardware, software resources, and provides common services for computer programs. (I/O, Memory allocation, etc.)</u>
- System calls: <u>a way user space applications interact with OS, hardware, privileged applications, and data structures on the prgramming level</u>
  - Network: socket, accept, bind, listen
  - File I/O: read, write, open, close
  - CPU/Process: execve, fork, clone
  - Memory: 
    - brk: Set the end of the data segment to the value specified by address
    - sbrk: Increments the programs's data space by increment bytes
    - mmap: Map files or devices into memory
- Users:
  - UID: <u>user's unique identification number (UID)</u>
    - To see your UID: `id -u`
    - See all UIDs: `cat /etc/passwd` (username:password:user ID: group ID: user ID info: home directory: command/shell)
    - See all hashed passwords for the system: `cat /etc/shadow` 
- Users and Groups:
  - `ls -alhs` (-a sees all the file started with . -l list long format -h use unit suffixes, -s display number of system blocks used by file)
  - To add user to the group: `usermod -aG <groupname> <username>`
  - To view all groups: `cat /etc/group`
  - Change ownership: `chown Ron <file_name>`
- Processes: an instance of a specific running program
  - PID: <u>the way to refer to a specific process</u>
  - To lookup PID: `ps ` or `ps aux | grep firefox`
  - Kill program by ID: `kill -9 PID`
  - Investigate program: `strace -p PID`
- Block Devices: <u>Devices that are read in chunks or blocks and can be mounted and read</u>
  - Hard drive, flash drive, DVD, card reader, etc. 
  - To display bd: `lsblk`
    - To read bd, mount them to file system: `mount /dev/sdb1 /mnt` then `unmount /mnt`
- File Structure:
  - `/` - called slash, the root directory
  - `/boot` - static files for the boot loader
  - `/home` - user directories 
  - `/etc` - configuration files
  - `/dev` - device files, HD, disk, etc.
  - `/proc` - not actually on the disk
    - a pseudo-filesystem which provides an interface to kernel data structures.
- Access Control: confidentiality (consealment of resources/information), integrity (trustworthiness of resource)
  - Discretionary Access Control: Linux standard
    - Subjects can determine how other subjects can use(modify,view,execute) files they own at their discretion.
  - Mandatory Access Control: SELinux
    - Access control is delegated by an administrator.
    - Subjects do not have control over their row of the matrix.
    - Owner of an object can not change access control of that object.
  - Role Based Access Control: K8s 
    - Subjects have roles and those roles have permissions associated with them.
    - The permission is bound to the role the user has not the user itself.

####OSquery Installation and Setup

To install osquery

```
export OSQUERY_KEY=1484120AC4E9F8A1A577AEEE97A80C63C9D8B80B
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys $OSQUERY_KEY
sudo add-apt-repository 'deb [arch=amd64] https://pkg.osquery.io/deb deb main'
sudo apt install osquery -y
```

To access osquery

` sudo osqueryi`	

A list of viewing options for osquery:

```
.mode csv
.mode list
.mode column
.mode line
.mode pretty
```

Get a list of all available tables in the osquery: `.tables`

Get the schema(columns, types) of the tables: `.schema users` `.schema routes`

####Make Queries

Be able to use osquery to: 

- Find the command used to start a process

  `SELECT pid, cmdline FROM processes WHERE pid=9838;`

- Find the shell used by username class 

  `SELECT username, shell FROM users;`

- Find the memory location of the kernel module ip_tables. (must `sudo osqueryi` for memory address)

  `SELECT name, address FROM kernel_modules;`

- Find all IP address associated with a docker container.

  `SELECT name, ip_address FROM docker_container_networks;`

  - This address can be used to access the docker service without having to map the port.
  - i.e., if you run docker run --rm -it vulnerables/web-dvwa and find the IP address associated with the container you don’t have to run the container with the -p flag as suggested docker run --rm -it -p 80:80 vulnerables/web-dvwa, in order to access dvwa.

- Other useful queries:

  - Track all the containers that are running as **privileged**.

    `SELECT name, image, status FROM docker_containers WHERE privileged=1;`



# Sysdig

Be able to read a file with sysdig-inspect.

- Record, with sysdig running on your VM, the sql injection attack on your DVWA setup from lab 2 part 2. 

  - `sudo sysdig -w test.scap`
  - `docker run --rm -it -p 80:80 vulnerables/web-dvwa`
  - Go to `localhost:80` and login to the DVWA 
  - SQL Injection: `%' and 1=0 union select null, concat(user,':',password) from users #`

- Find evidence of the injection attack in your sysdig file. 

- Find the system call associated with your attack.  

- Find the network traffic associated with your attack. 

- Use filters with sysdig (ex `proc.pid=4594`). 

- Use `sysdig -l | less` to see other filters apply filters. 

  - For all of the above tasks, we can use the following commands to inspect scap file

  - `sudo sysdig -r test.scap container.type=docker`, then find pid for apache2

  - `sudo sysdig -r test.scap proc.pid = 25237 | grep sendto`

  - To access the sysdig UI, run the following script in the same directory as the `test.scap` file

    `docker run -it -v $(pwd):/captures -p8085:3000 sysdig/sysdig-inspect:latest`

# Containers

Containers are a way to provide isolation.

- chroot: <u>a way to isolate a directory to restrict access to filesystem</u>
  - cannot access anything not contained in the directory (no `ls, bash, vim...`)
- cgroups: <u>control groups restrics access to system resources</u>
  - resource limiting: groups can be set to not exceed a configured memory limit
  - prioritization: some groups may have larger share of CPU utilization or disk I/O throughput
  - accounting: measures a group's resource usage
  - control: freezing groups of processes, their checkpointing and restarting
- namespaces: <u>provide isolation and enable a process to have a different view of the system than other processes</u>

# Kubernetes

For this course we use microk8s



# SELinux

You are given a sample wikipedia policy file `wiki_messed.te`

Wiki files are allowed to **view, read, write, and create**, only `wiki_var_t` type files.

The wikipedia application has a label of `wiki_t` and hence whenever we create a new file they are created with `wiki_var_t` type. 

Look at the given policy file and find out all the mistakes that has been made in the given file and correct them. Note: You can assume all lines of code before the comment are fine. Init and socket lines of code are assumed to be correctly configured.

```
policy_module(wiki, 1.0)
userdom_unpriv_user_template(wiki)
type wiki_var_t;
files_type(wiki_var_t)
require {
	type home_root_t;
	type user_home_t;
	type init_t;
	class file { create execute open read write getattr execute_no_trans};
	type http_cache_port_t;
}

########################################
# messed up wiki local policy
type_transition wiki_t wiki_exec_t:file wiki_exec_t;				mistake #1
type_transition wiki_t wiki_var_t:dir wiki_var_t;
#============= socket ==============
allow wiki_t http_cache_port_t:tcp_socket name_bind;
#============= init_t ==============
allow init_t wiki_var_t:file execute;
allow init_t home_root_t:file execute;
allow init_t user_home_t:file execute;
#============= wiki_t ==============
allow wiki_t wiki_var_t:file {execute read write getattr};	mistake #2
allow wiki_t wiki_var_t:dir {search add_name};							mistake #3
```

Fixes:

```
type_transition wiki_t wiki_var_t:file wiki_var_t;
allow wiki_t wiki_var_t:file {read write create};
allow wiki_t wiki_var_t:dir {read write create};
```



# Web Vulnerabilities 

- CSP Bypass
- SQL Injection
- etc