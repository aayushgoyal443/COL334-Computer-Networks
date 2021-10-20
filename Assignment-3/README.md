# How to run
1. Open ns-allinone-3.29 folder and then change to the ns-3.29 folder
```sh
cd ns-3.29
``` 

## Part A

2. Now to change the code inside `ns-3.29/examples/tutorial/sixth.cc` with the `First.cc` file submitted.
3. Make sure you are in the `ns-3.29` folder. Run the following
```sh
./waf configure --enable-example
```
4. To run for different parts of the question, pass the part number as command line argument as follows
```sh
./waf --run "examples/tutorial/sixth <part_num>"
```
Here <part_num> is:
* a: NewReno
* b: HighSpeed
* c: Veno
* d: Vegas