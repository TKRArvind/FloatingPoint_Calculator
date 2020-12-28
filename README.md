# Floating-Point Calculator

> Feature Summary :  
> 1. Computing addition/subtraction on N-bit floating point numbers with E-bit exponent
> 2. Conversion from decimal to floating point (N,E) and vice versa.

This program performs floating point computation (add/sub) and format conversion operations. It is mainly written to verify the result produced by the hardware implementation of floating point unit. So part of this code's result or operations are shown/done as bit wise computations. It also tries to minimise the use of advanced library functions. It supports Inf, MInf, NaN, denormals and Normal numbers.
As it is generic it can be used for any floating point formats including **IEEE-754 format**  and of any length like FLP64, FLP32, FLP16 etc. \
This Floating point program has four main functionality and some additional features. All these functionality can be invoked from command line by turing on appropriate switches. 

> A function f doing task A is denoted with *A@f*

## A. Main Functions:

### 1. Addition *@FLPADD*
  This function computes the addition of two floating point numbers given ashex numbers like 0xABCD/0xabcd. It also needs width of the exponent the given floating point has as it can vary. It doesn't require any specification on the number of bits the floating point has i.e 32,16 bit. It automaticallly considers the N bit from the given Hex and computes the addition for the given exponent width. \
	`FLP.py --add -exponentWidth 5 --floata 0x0000 --floatb 0x0000`

### 2. Subtraction *@FLPADD*
   The same addition function when given *'sign as 1'* computes the difference of two floating point numbers. \
	 `FLP.py -s -ew 5 -fa 0x0000 -fb 0x0000`
   
### 3. Float to Decimal Conversion *@FLP2DEC*
   This function converts the float given to its decimal value. It requires exponent width and auto considers the floating point bitwidth. \
   `FLP.py -ew 5 -f2d 0x0000`

### 4. Decimal to Float Conversion *@DEC2FLP*
   This function converts the decimal to N bit floatinng point representation with Ebit exponents. It can take **Inf, MInf, NaN** and can even take numbers like 0.001 or 1E-3. \
   `FLP.py -ew 5 -n 16 -d2f 1E-7`

> Note : This program doesn't differentiate between qNan or sNan. It simply consider all ones as NaN.

## B. Supporting Functions:

### 1. Count Leading zero *@LEAD0FINDER*
  This function takes in fraction and maximum bits the fraction needs to be expanded in binary. It returns the bit position where first '1' occurs and fraction value left to compute further bits.

### 2. Fraction to Binary conversion *@FRAC2BIN*
  It is very similar to *@LEAD0FINDER* except it returns complete N-bit number representing the fractions along with error value(can be used to compute further bits).
	
### 3. Rounding *@RND2EVNTIE20*
   This function takes in the N+(K>3) bit binary floating point number and returns N-bit number. It uses Gaurd,Round and sticky bit for making round to even tie to zero decision for rounding.



## C. Useful Features:

### 1. Default :
   By default `python3 FLP.py`  invokes `FLP.py -h`   and displays information about all the switches it has with a small description about them.


### 2. DisplayStep :
   It displays the the results of the intermediate steps in addition and subtraction. They include values after (i) Alignment, (ii) Arithmetic, (iii) Normalisation, (iv) Rounding steps. \
	 `FLP.py -ds -a -ew 5 -fa 0x0000 -fb 0x0000`


### 3. PrettyPrinting :
   This switch displays rich information about the process including what the inputs-outputs are, what switches are taken into consideration and their values.\
	 `FLP.py -pp -ew 5 -n 16 -d2f 1E-7`
