#---------------------------------------------------------------------------------------#
# Name  : FLP.py
# Author: T.K.R.Arvind
# Date  : 27th December 2020
# CLI   : FLP.py 
#
# This program is for floating point computation and related opeartions and is 
# mainly written to cross-check the result produced on hardware implementation.
# So part of this code results or operations are done as bit wise computations.
# This has four main features written with minimal library functions:
#       a) Floating Point addition
#       b) Floating point subtraction
#       c) Float to decimal conversion
#       d) Decimal to Float conversion
# It rounds FLP numbers by 'ROUND to EVEN TIE to ZERO' method
#---------------------------------------------------------------------------------------#

import sys      
import math
import argparse #for command line interface only

#========================== 1)Floating point addition subtraction ========================#
# This takes in five parameter as inputs
#                  1) floata : floating point a
#                  2) floatb : floating point b
#                  3) Ewidth : width of the exponent
#                  4) sign   : indication addition/subtraction
#                  5) display: determines whether to print intermediate step results
# It returns the resultant of two numbers    
#
#=======================================================================================#
#
def FLPADD(floata,floatb,Ewidth,sign,display):
    floata = floata.lower()
    floatb = floatb.lower()
   
    if(floata == "nan" or floata == "inf" or floata == "minf" or floatb == "nan" or floatb == "inf" or floatb == "minf"):
        print("\npass special values in Hex")
        sys.exit(1)
        
    flpa = floata.replace("0x",'')
    flpb = floatb.replace("0x",'')
    
    N = len(flpa) # taking the value of (N-bit)/4 number and should be integer
    if(N != len(flpb)): 
        print("Length of the N-bit numbers dont match")
        sys.exit(1)
        
    if((math.log(N,2)).is_integer()): #checking whether input is incomplete 
        N = N*4 # number of bits in N-bit binary floating point representation
        if(N <= Ewidth+1):
            print("Exponent width is more than number of bits")
            sys.exit(1)
    else:
        print("\nInput Numbers are incomplete or not a floating value.")
        sys.exit(1)
    
    ina = ''
    inb = ''
    try:
        ina = (bin(int(flpa,16))).lstrip('0b').zfill(N) #converting Hexa inputs to binary numbers
        inb = (bin(int(flpb,16))).lstrip('0b').zfill(N)
    except ValueError:
        print("\nInput Numbers are not a floating value.")
        sys.exit(1)
    
    if(display): 
        print('\n#--------- Inputs ------------#')    
        print('Floating point A :',ina[0]+'_'+ina[1:Ewidth+1]+'_'+ina[Ewidth+1:])
        print('Floating point B :',inb[0]+'_'+inb[1:Ewidth+1]+'_'+inb[Ewidth+1:])
        print('Is sutraction    :',str(sign))
    
    #--------------------------- alignment starts here --------------------------------#
    #   In alignment the code checks for special values and returns special values. It finds the
    #   maximum and minimum and aligns the minimum value with respect to the difference in 
    #   the exponenet value or depending on other factor. 
    #----------------------------------------------------------------------------------#
    
    opn = int(ina[0],2)^int(inb[0],2)^sign # 1 means subtraction
    expa = int(ina[1:Ewidth+1],2) # storing biased exponent A
    expb = int(inb[1:Ewidth+1],2) # storing biased exponent B
    
    mana = ('0' if expa==0 else '1') +ina[Ewidth+1:] # storing mantissa A without hidden bit
    manb = ('0' if expb==0 else '1') +inb[Ewidth+1:] # storing mantissa B without hidden bit
    bias = 2**(Ewidth-1)-1
    EInf = 2**(Ewidth)-1
    HBManWidth = len(mana) #includes hidden bit in length
    
    InfWoSign = '1'*Ewidth + '0'* (HBManWidth-1)
    NaN = '1'*N
    #processing the special values like Nan and Inf here
    if(ina == NaN or inb == NaN): #If any are NaN just return N
        return NaN
    elif(ina[1:] == InfWoSign and inb[1:] != InfWoSign): #if any one is infinity return infinity with sign
        return ina
    elif(inb[1:] == InfWoSign and ina[1:] != InfWoSign):
        return inb
    elif(ina[1:] == InfWoSign):
        if(inb == ina[0]+InfWoSign): #both are same signed infinity
            if(sign == 0): #addition operation
                return ina
            else:
                return NaN
        else:
            if(sign == 1): #both are different signed infinity
                return ina #addition operation
            else:
                return NaN
    
     
    newsign = int(inb[0],2) ^ sign
    Newinb = str(newsign) + inb[1:] #taking subtraction into effect
    
    swap = 0 # indicator to swap the inputs to assign MaxMan etc
    if(expb > expa): 
        swap = 1
    elif(expa == expb):
        if(int(manb,2) > int(mana,2)):
            swap = 1
   
    MaxMan = mana
    MinMan = manb
    MaxExp = expa
    MinExp = expb
    sign = '1' if(ina[0]=='1') else '0'    
    
    if(swap == 1):
        MaxMan = manb
        MinMan = mana
        MaxExp = expb
        MinExp = expa
        sign = '1' if(Newinb[0]=='1') else '0' #taking subtraction into consideration
    
    #finding  the shift value with which the number id shifted
    delE = 0
    if(MinExp==0 and MaxExp>0): #right shift be E-1 when one is denormal
        delE = MaxExp-1
    else:
        delE = MaxExp-MinExp
    
    MaxMan += '000'
    MinMan += '000' #simply filling with GRS bits
    if(delE <= HBManWidth+4): #just not to run of processors bit :)
        ShiftedMan = '0'*delE + MinMan[0:]
    else:
        ShiftedMan = '0'*(HBManWidth+4) + MinMan[0:]
    
    
    AlignedMan = ''
    if(len(ShiftedMan[0:HBManWidth+2]) < (HBManWidth+2)): #if width of aligned is less than or equal to (hb+Manwidth+GR) bit
        AlignedMan = (ShiftedMan[0:HBManWidth+2]).rjust(HBManWidth+2,'0')
    else:
        AlignedMan = ShiftedMan[0:HBManWidth+2]
        
    
    if (int(ShiftedMan[HBManWidth+2:HBManWidth+4],2)>0): # calculating stickybit values
        AlignedMan += '1'
    else:
        AlignedMan += '0'
    
    if(display):   
        print('\n#------- Alignment -----------#')
        print('is subtraction?  :',opn)
        print('Rshift Mantissa  :',delE)
        print('mantissa to shift:',MinMan[0]+'_'+MinMan[1:-3]+'_'+MinMan[-3:])
        print('Aligned mantissa :',AlignedMan[0]+'_'+AlignedMan[1:-3]+'_'+AlignedMan[-3:])
        print('Maximum mantissa :',MaxMan[0]+'_'+MaxMan[1:-3]+'_'+MaxMan[-3:]) 
    
    #--------------------------- arithmetic starts here --------------------------------#
    #   The computation of numbers happens here in two's complement method
    #-----------------------------------------------------------------------------------#
    
    FA = len(AlignedMan) # number of Full adder needed
    complementedMan = '' # This is just a initialisation not to be confused
    if(opn == 1): #1's complement only if subtraction
        for i in range(0,len(AlignedMan)):
            if(AlignedMan[i] == '0'):
                complementedMan += '1'
            else:
                complementedMan += '0'
    else:
       complementedMan = AlignedMan 
    
    cin = opn
    partialsum = 0
    arithmeticResult = ''
    for i in range(FA-1,-1,-1): #moving from lsbth position to 0
        partialsum += cin
        partialsum += 1 if(complementedMan[i] =='1') else 0
        partialsum += 1 if(MaxMan[i] =='1') else 0
        arithmeticResult = str(partialsum %2) + arithmeticResult
        cin = 1 if(partialsum >1) else 0
        partialsum = 0  
        
    if (opn==1): #it cannot produce a negative result as it is swap even for delexp = 0
        arithmeticResult = '0' + arithmeticResult
    else:
        arithmeticResult = str(cin)+ arithmeticResult
    
    if(display):       
        print('\n#------- Arithmetic ----------#')
        print('lsb cin '+str(cin))
        print('Mantissa Min Val :', AlignedMan[0]+'_'+AlignedMan[1:-3]+'_'+AlignedMan[-3:])
        print('Complemented Val :', complementedMan[0]+'_'+complementedMan[1:-3]+'_'+ complementedMan[-3:])
        print('Mantissa Max Val :', MaxMan[0]+'_'+MaxMan[1:-3]+'_'+MaxMan[-3:])
        print('Arithmetic Val  :', arithmeticResult[:2]+'_'+arithmeticResult[2:-3]+'_'+arithmeticResult[-3:])
    
    #--------------------------- Normalisation starts here --------------------------------#
    #   This normalises the arithmetic results by left shifting or right shifting the mantissa
    #   and reflecting its effect on the exponent.
    #--------------------------------------------------------------------------------------#
    
    NormalisedMan = '' 
    NormalisedExp = MaxExp
    
    try:
        preshift = arithmeticResult[1:].index('1') #starting from hidden so neglected carry bit
    except ValueError:
        preshift = 2*N #some big number
        
    if(opn == 0 ): #only if addition and has produced a carry
        if(arithmeticResult[0]=='1'):
            NormalisedMan = arithmeticResult[1:]#removing carry bit as it becomes a hiddn bit
            NormalisedExp +=1
            if(NormalisedExp >= 2**(Ewidth)-1 ):#if exp goes to Infinity return inf
                Inf = sign +'1'*Ewidth
                return Inf.rjust(N,'0')
        else:
            NormalisedMan = arithmeticResult[2:]#removing hidden bit as it is the first bit
    elif(MaxExp == 0 ):
        NormalisedMan = arithmeticResult[2:]
    elif(MaxExp > preshift): 
        NormalisedExp -= preshift
        NormalisedMan = arithmeticResult[preshift+2:]#removing the hidden bit present at preshift
    else:
        NormalisedMan = arithmeticResult[MaxExp:]
        NormalisedExp = 0;
    
    
    t =(len(MaxMan))  #if Normalised man is less than Mantissa +GRS
    if(len(NormalisedMan) <= t ): #K is less than mantissa and GRS bits then pad 0
        NormalisedMan = NormalisedMan.ljust(t-1,'0')
        
          
    NormalisedExp = bin(NormalisedExp).lstrip('0b').rjust(Ewidth,'0')
    PreRound = '0' + NormalisedExp + NormalisedMan
    
    if(display): 
        print('\n#----- Normalisation ---------#')
        print('Max-Exp  Value   :', str(MaxExp))
        print('preshift value   :', str(preshift))
        print('NormalisedExp is :', NormalisedExp)
        print('NormalisedMan is :', NormalisedMan)
        print('Pre Rounding  is :',PreRound[0]+'_'+PreRound[1:Ewidth+1]+'_'+PreRound[Ewidth+1:N]+'_'+PreRound[N:])
    
    
    #--------------------------- Rounding starts here --------------------------------#
 
    Round = RND2EVNTIE20(PreRound,N,0.0,display)    
    if(Round[0] == '1'): #during rouning there is a possibility that exp becomed infinity
        Inf = sign +'1'*EWidth
        return Inf.rjust(N,'0')
    else:#fixing the sign
        Round = sign+Round[1:]
        return Round
#
#=======================================================================================#            
 
 
 
 
 
 
 


#================================= 2)LeadZerofinder ===================================#
# This function takes two parameters as inputs
#                  1) fraction : fraction for which l index to be found
#                  2) MaxIter  : Maxiteration to be performed in fraction
# It returns two values as outputs
#                  1) fraction : resultant fraction after Lead One is found
#                  2) Npos     : Position at which Lead one is present
#
#=====================================================================================#    
#
def LEAD0FINDER(fraction,MaxIter =10):
    iter = 1
    while(iter <= MaxIter):
        fraction *= 2
        if(fraction < 1):
            iter +=1
        else:
            fraction -= 1
            return fraction,iter
    return fraction,iter
    
#=======================================================================================#     
    
         
         
         
         
         
         
 
#================================= 3)Rounding Logic ======================================#
#This function takes the N+(k>2) binary numbers and does round to even with tie to zero rule
#                  1) fa      : Flp number to be rounded
#                  2) Nwidth  : width of floating point number
#                  3) fraction: optional parameter used as sticky bit
#                  4) display : determines whether to print intermediate step results
# It returns one outputs
#                  1) rounded : the rounded binary value of fa
#
#=======================================================================================#
#
def RND2EVNTIE20(fa,Nwidth,fraction = 0.0,display = 0):
    try:
        stickybit = int(fa[Nwidth+2:],2) #sticky bit is 1 is any bit after sticky is one which in integer is >0
    except ValueError:
        stickybit = 0
    
    
    if(stickybit >0 or fraction > 0): #fraction is fraction value of sticky
        grsbits = (fa[Nwidth:Nwidth+2]+'1') #converting to integer value for {LSB,Ground,Round,Sticky}
    else:
        grsbits = (fa[Nwidth:Nwidth+2]+'0')
    
    ulp = 0
    if(int(grsbits,2) > int('100',2)): #add ulp if  of G,R,S > 100
        ulp = 1
    elif(int(grsbits,2) == int('100',2) and int(fa[Nwidth-1],2)): #roundup to zero in half case
        ulp = 1
    else:
        ulp = 0
        
    cin = ulp
    rounded = ''
    sum = 0
    for i in range(Nwidth-1,-1,-1): #moving from lsbth position to 0
        sum += cin
        sum += 1 if(fa[i] =='1') else 0
        rounded = ('1' if sum==1 else '0')+rounded
        cin = 1 if(sum ==2) else 0
        sum = 0
    
    if(display):   
        print('\n#-------- Round --------------#')
        print('PreRounding  is  :',fa[:Nwidth]+'_'+fa[Nwidth:])
        print('Round decision   :',grsbits)
        print('is ulp added     :',str(ulp))
        print('rounded value is :',str(cin)+rounded[:Nwidth+1])
        print('rounded Hex is   :',hex(int(rounded,2)))
        print('')
    
    return rounded
#=======================================================================================#
#    



#================================= 4)Decimal to Float Convertion =========================#
# This takes in the three parameters as inputs
#                  1) deca : decimal number to be converted to float 
#                  2) Ewidth : width of the exponent in Float
#                  3) Nwidth : width of the binary number to generate
# It converts the decimal point to floating point of Nwidth bit representation
#
#=======================================================================================#
# 
def DEC2FLP(dec,Ewidth,Nwidth):
    if(Nwidth <= Ewidth+1): #checking for valid bit widths
        print("Exponent width is more than number of bits");
        sys.exit(1)
    Mwidth = Nwidth - Ewidth -1 # Mantissa width will remove sign and exponenet bits
    
    sign = '0'
    if(dec.lower() =="nan"):   #checking for exception values and returning approproate strings  
        return '1'+'1'*Ewidth+'1'*Mwidth
    elif(dec.lower() =="inf"):
        return '0'+'1'*Ewidth+'0'*Mwidth
    elif(dec.lower() =="minf"):
        return '1'+'1'*Ewidth+'0'*Mwidth
    
    try:
        dec = float(dec)
        integer = abs(int(dec))
        fraction = abs(dec) - integer
        if(dec < 0): #assigning the sign based on decimal
            sign = '1'
    except ValueError:
        print("\n"+dec,"is not integer to convert")
        return '1'*Nwidth #returning NaN value
   
    bias = 2**(Ewidth-1)-1 #Exponent is initialised to bias
    intBinary = bin(integer).lstrip('0b') #Converting integer to binary
    fracBinary = ''
    
    posPow = len(intBinary) #Positve power to be added to the exponent
    MaxPosPow = 2**Ewidth-1
    iter = 0
    
    if(posPow > MaxPosPow):# If exp goes to all ones or above then return Inf 
        return sign+'1'*Ewidth+'0'*Mwidth
    elif(posPow > 0):
        exp = bias + posPow-1 #because lsb is 2^0 not 2^1 hence subtractby 1
        intBinary = intBinary[1:] #removing Hiddenbit 
        ManWFrac = Mwidth + 4 - posPow # the number of mantissa bits required from frac(includes Hiddenbit,GRS bits)
        fracBinary,fraction = FRAC2BIN(fraction,ManWFrac)
    else:
        fraction,iter = LEAD0FINDER(fraction,bias-1) #Max iter as bias-1 within which it should find one
        exp = bias - iter #adding negative power
        ManWFrac = Mwidth + 3 #includes GRS bits
        fracBinary,fraction = FRAC2BIN(fraction,ManWFrac)
        
    ManBinary = intBinary + fracBinary #combining the bits which doesnt include hidden bit
    ExpBinary = bin(exp).lstrip('0b').rjust(Ewidth,'0')
    PreRound = sign + ExpBinary + ManBinary
    return RND2EVNTIE20(PreRound,Nwidth,fraction,0)
#    
#======================================================================================#
 
 
            
#========================== 5)Fraction to Binary Converter =============================#
# This function takes in two parameters as input
#                  1) fraction : fraction for which biary to be computed
#                  2) Nwidth   : Number of bits to represent the fraction
# It returns two values as outputs
#                  1) fracBinary : Nwidth binary reperesentation of fraction
#                  2) fraction : conuation value with with more bits can be generated
#
#======================================================================================#
#
def FRAC2BIN(fraction,Nwidth):
    fracBinary = ''
    while(Nwidth > 0):
        fraction *= 2
        if(fraction >= 1):
            fracBinary += '1'
            fraction -= 1
        else:
            fracBinary += '0'
        Nwidth -=1
    return fracBinary,fraction
#======================================================================================#



 





#================================= 6)Float to Decimal Convertion =========================#
# This takes in the two parameters as inputs
#                  1) fa : Flp number (as HEX) to convert to decimal 
#                  2) Ewidth : width of the exponent in Flp
# It converts the floating point hex value to decimal with base 10 representation
#
#=======================================================================================#
#
def FLP2DEC(flpO,Ewidth):
   flpO = flpO.lower()
   
   if(flpO == "nan"):
    return float("nan");
   elif(flpO =="minf"):
    return float("-Inf")
   elif(flpO =="inf"):
    return float("Inf")
    
   
   flp = flpO.replace("0x",'').replace("0X",'')
   N = len(flp) # taking the value of (N-bit)/4 number and should be integer
   
   if((math.log(N,2)).is_integer()): #checking whether input is incomplete 
    N = N*4 # number of bits in N-bit binary floating point representation
    if(N <= Ewidth+1):
        print("\nExponent width is more than number of bits")
        sys.exit(1)
   else:
    print("\nEither Input Number -",flpO,"- in FLP2DEC is incomplete or not a valid floating point number in Hexadecimal")
    sys.exit(1)
    
   decimalRoundby = int((N/2)-1) # this is the value to round depending on N-bit for decimal output
   input = ''
   try:
    input = (bin(int(flp,16))).lstrip('0b').zfill(N) #converting Hexa inputs to binary number
   except ValueError:
    print("\n"+flpO+' is not a valid floating point number in Hexadecimal')
    sys.exit(1)
   
   #--------------------- Conversion process starting here --------------------------------#
   
   Bias = 2**(Ewidth-1)-1 #calculating Bias term
   ExpWBias = int(input[1:1+Ewidth],2) #stores the value of exponent with bias 
   
   
   if(ExpWBias == 0): #case for denormal number
    exp = 1-Bias 
    Mantissa = '0'+str(input[1+Ewidth:]) #adding hidden bit as zero
   else:
    if(ExpWBias == 2**(Ewidth)-1): #case for infinity or Nan
        exp = ExpWBias
    else:
        exp = ExpWBias-Bias #removing bias from exponent
    Mantissa = '1'+str(input[1+Ewidth:]) #adding 1 as hidden bit
   
   
   sum = 0; #calculating mantissa value  
   for i in range(0,len(Mantissa)):
    if(Mantissa[i] == '1'):
        sum = sum+2**(-i)
    
   if(ExpWBias == 2**(Ewidth)-1): #exponents are all ones
    if(sum == 1): #Mantissa is 1
        if(str(input[0])=='0'):
            return float("Inf")
        else:
            return float("-Inf");
    else: #if Mantissa >1
        return float("NaN");
   else:
    FLPValue = sum * 2**(exp) #mantissa times two raised to the power of exponent without bias.
    FLPValue = round(FLPValue,decimalRoundby)
    if(str(input[0]) == '1'):
        return -1*FLPValue
    else:
        return FLPValue
#    
#================================== FLP2DEC Complete ======================================#  
   
    



#======================================== CLI =============================================#
if __name__=='__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-i","--info",action='store_true',help ="Shows more information about the program")
    parser.add_argument("-a","--add",action='store_true',help ="Add floatA and floatB inputs ")
    parser.add_argument("-s","--sub",action='store_true',help ="Subtract floatB from floatA ")
    parser.add_argument("-ds","--displayStep",action='store_true',help ="Shows Intermediate steps in addition and subtraction ")
    parser.add_argument("-pp","--prettyPrint",action='store_true',help ="Formats output in more detail for better understanding ")
    parser.add_argument("-f2d","--flp2Dec",type = str,help ="Converts float to decimal representation i.e 0x2e66 -> 0.1")
    parser.add_argument("-d2f","--dec2Flp",type =str ,help="Decimal number to be converted to floating point i.e 0.1/1E-7/Nan/Inf")
    parser.add_argument("-ew","--exponentWidth",type=int, required = (len(sys.argv) >3),
    help="Width of the exponent in N-bit floating point number i.e 5")
    parser.add_argument("-fa","--floata",type =str ,required = ('--add' in sys.argv) or ('--sub' in sys.argv) or ('-a' in sys.argv) or ('-s' in sys.argv) ,
    help="input float number in hexadecimal i.e 0xFA34")
    parser.add_argument("-fb","--floatb",type =str ,required = ('--add' in sys.argv) or ('--sub' in sys.argv) or ('-a' in sys.argv) or ('-s' in sys.argv),
    help="input float number in hexadecimal i.e 0x0000")
    parser.add_argument("-n","--Nbit",type =int ,required = ('-d2f' in sys.argv) or ("--DEC2FLP" in sys.argv),
    help="Total number of Floating point bits i.e 8/16/32..etc")
    
    FLAGS = parser.parse_args()
    
    if(FLAGS.info):
        clearScreen()
        print("\n------------ About Floating Point function --------\n\n")
        showInfo()
    elif(FLAGS.add):
        ans = FLPADD(FLAGS.floata,FLAGS.floatb,FLAGS.exponentWidth,0,FLAGS.displayStep)
        if(FLAGS.prettyPrint):
            print("")
            print("#-- Floating point Addition --#")
            print("ExpWidth :", str(FLAGS.exponentWidth))
            print("Input A    :", str(FLAGS.floata))
            print("Input B    :", str(FLAGS.floatb))
            print("Hex Output :", hex(int(ans,2)))
            print("Bin Output :", bin(int(ans,2)))
            print("")
        else:
            print(hex(int(ans,2)))
    elif(FLAGS.sub):
        ans = FLPADD(FLAGS.floata,FLAGS.floatb,FLAGS.exponentWidth,1,FLAGS.displayStep)
        if(FLAGS.prettyPrint):
            print("")
            print("#-- Floating point Subtraction --#")
            print("ExpWidth   :", str(FLAGS.exponentWidth))
            print("Input A    :", str(FLAGS.floata))
            print("Input B    :", str(FLAGS.floatb))
            print("Hex Output :", hex(int(ans,2)))
            print("Bin Output :", bin(int(ans,2)))
            print("")
        else:
            print(hex(int(ans,2)))
    elif(('-d2f' in sys.argv) or ("--DEC2FLP" in sys.argv)):
        ans = DEC2FLP(FLAGS.dec2Flp,FLAGS.exponentWidth,FLAGS.Nbit)
        if(FLAGS.prettyPrint):
            print("")
            print("#-- Converting Decimal to Float --#")
            print("ExpWidth     :", str(FLAGS.exponentWidth))
            print("Input number :", str(FLAGS.dec2Flp))
            print("Value in bin :", str(ans))
            print("Value in Hex :",hex(int(ans,2)))
            print("")
        else:
            print(hex(int(ans,2)))
    elif(('-f2d' in sys.argv) or ("--FLP2DEC" in sys.argv)):
        ans = FLP2DEC(FLAGS.flp2Dec,FLAGS.exponentWidth)
        if(FLAGS.prettyPrint):
            print("")
            print("#-- Converting Float to Decimal --#")
            print("ExpWidth :", str(FLAGS.exponentWidth))
            print("Input    :", str(FLAGS.flp2Dec))
            print("Value    :", str(ans))
            print("")
        else:
            print(ans)
    else:
        parser.print_help()
        print("")
#=================================== THE END ================================================#