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


## Part 3

1. Now change the code inside `ns-3.29/examples/tutorial/sixth.cc` from the `Third.cc` file submitted.
2. Next put the `tcp-newrenocse.cc` and `tcp-newrenocse.h` file in the `ns-3.29/src/internet/model`
3. Now make the following changes in the `ns-3.29/src/internet/wscript`. Now add "model/tcp-newrenocse.h" in headers.source. Also add "model/tcp-newrenocse.cc" in obj.source.
4. Compile the newly added protocol using
```sh
./waf
```
5. Next run the command
```sh 
./waf configure --enable-example
```
6. Now to run the code, copy the file "Third.cc" into "sizth.cc" as done in the previous parts give the following command
```sh
./waf --run "examples/tutorial/sixth <config_num>"
```
Here config number is 1, 2 and 3


## Plotting script

To run:
```python
python plot.py <ques_num>
```
Here \<ques_num> can be 1, 2, 3  
The input files should be present in `Q{<ques_num>}/outputs/toplot` folder  
The output files will be in `Q{<ques_num>}/outputs/plots` folder   
Please make sure that plots folder is already present, else it will throw an error