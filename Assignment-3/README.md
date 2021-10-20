# How to run
Open ns-allinone-3.29 folder and then change to the ns-3.29 folder
```sh
cd ns-3.29
``` 

## Part 1

1. Now change the code inside `ns-3.29/examples/tutorial/sixth.cc` from the `First.cc` file submitted.
2. Make sure you are in the `ns-3.29` folder. Run the following
```sh
./waf configure --enable-example
```
3. To run for different parts of the question, pass the part number as command line argument, as follows
```sh
./waf --run "examples/tutorial/sixth <part_num>"
```
Here <part_num> is:
* a: NewReno
* b: HighSpeed
* c: Veno
* d: Vegas


## Part 2

1. Now change the code inside `ns-3.29/examples/tutorial/sixth.cc` from the `First.cc` file submitted.
2. Make sure you are in the `ns-3.29` folder. Run the following
```sh
./waf configure --enable-example
```
3. To run for different parts of the question, pass the part number and value as command line argument, as follows
```sh
./waf --run "examples/tutorial/sixth <part_num> <value>"
```
Here <part_num> is:
* a: Here we are varying the Data Rate. Application data rate is fixed as 2Mbps.  
\<value> has been varied in the list 2Mbps, 4Mbps, 10 Mbps, 20Mbps, 50 Mbps 
* b: Here we are varying the Application Data Rate. Data rate is fixed as 6Mbps.  
\<value> has been varied in the list 0.5 Mbps, 1Mbps, 2Mbps, 4Mbps, 10 Mbps