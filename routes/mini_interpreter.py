import json
import logging


from flask import jsonify
from flask import request

from routes import app

logger = logging.getLogger(__name__)


class interpreter:

    def __init__(self):
        self.arguments = {}

    def puts(self, *message):
        if not (len(message) == 1):
            return False
        # print(message[0])
        return message[0]

    def assignment(self, *argname):
        if(not (len(argname)==2)):
            return False
        if argname[0] in self.arguments:
            return False
        self.arguments[argname[0]] = argname[1] #may need change here
        return 'null'
    
    def st_concat(self, *arg):
        if(not(len(arg) == 2)):
            return False
        a = arg[0]
        b = arg[1]
        if not (a[0]==a[-1] and a[0]=='"'):
            return False
        if not(b[0]==b[-1] and b[0] == '"'):
            return False
        
        return '"'+ a[1:-1] + b[1:-1] + '"'

    def stlower(self, *arg):
        if(not(len(arg)==1)):
            return False

        a = arg[0]

        if not (a[0]==a[-1] and a[0]=='"'):
            return False


        return '"' + (a[1:-1]).lower() + '"'

    
    def stupper(self, *arg):
        if(not(len(arg)==1)):
            return False

        a = arg[0]

        if not (a[0]==a[-1] and a[0]=='"'):
            return False


        return '"' + (a[1:-1]).upper() + '"'      


    def substringReplace(self, *arg):
        if(not len(arg==3)):
            return False
        
        a = arg[0]
        b = arg[1]
        c = arg[2]

        if not (a[0]==a[-1] and a[0]=='"'):
            return False
        if not (b[0]==b[-1] and b[0]=='"'):
            return False
        if not (c[0]==c[-1] and c[0]=='"'):
            return False


        a= a[1:-1]
        b= b[1:-1]
        c= c[1:-1]

        loc= a.find(b)
        if(loc == -1):
            return arg[0]

        return '"' + a[:loc] + c + a[loc+len(c):] + '"'

        


    def substring(self, *arg):
        if (not(len(arg==3))):
            return False

        a = arg[0]
        b = arg[1]
        c = arg[2]

        if not (a[0]==a[-1] and a[0]=='"'):
            return False

        try:
            b = int(b)
            c = int(c)

        except:
            return False

        
        return '"'+ a[b:c] +'"'

    def add(self, *arg):
        ls = []

        if(len(arg)<2):
            return False

        for i in range(len(arg)):
            if (arg[i].replace('.', '', 1).isdigit() or arg[i].isdigit() or (arg[i][0] == '-' and arg[i][1:].replace('.', '', 1).isdigit())):
                ls.append(arg[i])
            else:
                return False
        
        ans = 0
        for i in ls:
            ans += float(i)

        return str(ans)
    
    def sub(self, *arg):
        if(not(len(arg)==2)):
            return False
        
        ls = []

        for i in range(len(arg)):
            if (arg[i].replace('.', '', 1).isdigit() or arg[i].isdigit() or (arg[i][0] == '-' and arg[i][1:].replace('.', '', 1).isdigit())):
                ls.append(arg[i])
            else:
                return False

        if (ls[0].isdigit() and ls[1].isdigit()):
            return str(int(ls[0])-int(ls[1]))
        return f"{float(ls[0])-float(ls[1]):.4g}"

    def multiply(self, *arg):
        ls = []

        if(len(arg)<2):
            return False

        for i in range(len(arg)):
            if (arg[i].replace('.', '', 1).isdigit() or arg[i].isdigit() or (arg[i][0] == '-' and arg[i][1:].replace('.', '', 1).isdigit())):
                ls.append(arg[i])
            else:
                return False
        
        ans = 1
        flag = True
        for i in ls:
            if '.' in i:
                ans *= float(i)
                # flag = False
            else:
                ans *= int(i)
        # if flag:
        #     str(int(ans))
        # else:
        str(ans)
        return f"{ans:.4g}" 

    def division(self, *arg):
        if(not(len(arg)==2)):
            return False
        
        ls = []

        for i in range(len(arg)):
            if (arg[i].replace('.', '', 1).isdigit() or arg[i].isdigit() or (arg[i][0] == '-' and arg[i][1:].replace('.', '', 1).isdigit())):
                ls.append(arg[i])
            else:
                return False
        if (ls[1] == "0"):
            return False
        if ('.' in ls[0] and '.' in ls[1]):
            return str(int(ls[0])/int(ls[1]))
        return f"{float(ls[0])/float(ls[1]):.4g}"


    def abosulte(self, *arg):
        if(not len(arg)==1):
            return False

        ls = []

        for i in range(len(arg)):
            if (arg[i].replace('.', '', 1).isdigit() or arg[i].isdigit() or (arg[i][0] == '-' and arg[i][1:].replace('.', '', 1).isdigit())):
                ls.append(arg[i])
            else:
                return False

        return str(abs(float(ls[0])))


    def getMax(self, *arg):
        ls = []

        if(len(arg)<2):
            return False

        for i in range(len(arg)):
            if (arg[i].replace('.', '', 1).isdigit() or arg[i].isdigit() or (arg[i][0] == '-' and arg[i][1:].replace('.', '', 1).isdigit())):
                ls.append(float(arg[i]))
            else:
                return False

        
        return str(max(ls))

    def getMin(self, *arg):
        ls = []

        if(len(arg)<2):
            return False

        for i in range(len(arg)):
            if (arg[i].replace('.', '', 1).isdigit() or arg[i].isdigit() or (arg[i][0] == '-' and arg[i][1:].replace('.', '', 1).isdigit())):
                ls.append(float(arg[i]))
            else:
                return False

        
        return str(min(ls))

    def greaterthan(self, *arg):
        if not(len(arg)==2):
            return False

        ls = []
        for i in range(len(arg)):
            if (arg[i].replace('.', '', 1).isdigit() or arg[i].isdigit() or (arg[i][0] == '-' and arg[i][1:].replace('.', '', 1).isdigit())):
                ls.append(float(arg[i]))
            else:
                return False

        if ls[0]>ls[1]:
            return 'true'
        else:
            return 'false'

    def lessthan(self, *arg):
        if not(len(arg)==2):
            return False

        ls = []
        for i in range(len(arg)):
            if (arg[i].replace('.', '', 1).isdigit() or arg[i].isdigit() or (arg[i][0] == '-' and arg[i][1:].replace('.', '', 1).isdigit())):
                ls.append(float(arg[i]))
            else:
                return False

        if ls[0]<ls[1]:
            return 'true'
        else:
            return 'false'
    
    def equal(self, *arg):
        if (not(len(arg)==2)):
            return False

        a = arg[0]
        if arg[0][0]=='"' and arg[0][-1] == '"':
            a = a[0][1:-1]
         
        b = arg[1]
        if arg[1][0] == '"' and arg[1][-1] == '"':
            b = b[0][1:-1]

        if (arg[0]==arg[1]):
            return 'true'
        else:
            return 'false'

    def neq(self, *arg):
        if (not(len(arg)==2)):
            return False

        a = arg[0]
        if arg[0][0]=='"' and arg[0][-1] == '"':
            a = a[0][1:-1]

        if arg[1][0] == '"' and arg[1][-1] == '"':
            b = b[0][1:-1]

        if not (arg[0]==arg[1]):
            return 'true'
        else:
            return 'false'

    def tostr(self, *arg):
        if not len(arg) == 1:
            return False
        
        return '"' + str(arg[0]) + '"'

    
    # def interpreter_func(self, *arg):
    #     statements = []
    #     stack = []
    #     current_statement = []

    #     for char in arg[0]:
    #         if char == '(':
    #             if current_statement:
    #                 # If we have a current statement, save it when a new '(' is found
    #                 statements.append(''.join(current_statement).strip())
    #                 current_statement = []
    #             stack.append(char)
    #             current_statement.append(char)
    #         elif char == ')':
    #             current_statement.append(char)
    #             stack.pop()
    #             if not stack:  # If the stack is empty, we finished a full statement
    #                 statements.append(''.join(current_statement).strip())
    #                 current_statement = []
    #         else:
    #             current_statement.append(char)
    #     if current_statement:
    #         statements.append(''.join(current_statement).strip())


    #     for i in range(len(statements)):
    #         count = 0
    #         if statements[i][-1]!=')': # incomplete statement
    #             count +=1
    #             continue
    #         elif statements[i][-1] == ')':
    #             func = statements[i].replace("(", "").replace(")", "")
    #             statements[i] = self.translate(func.split(" "))
    #             while(count!=0):
    #                 statements[i-1] = self.translate((statements[i-1].replace("(", "").replace(")", ""), statements[i]))
    #                 statements.pop(i)
    #                 i-=1
    #                 count-=1

    #     print (statements)
    
    def interpreter_func(self, input):
        index = 0
        statement = []
        current_statement = ""
        while index < len(input):
            if input[index] == '(':
                statement.append(self.interpreter_func(input[index + 1:]))
                index += 1
                para_num = 0
                while (input[index] != ')' and para_num == 0) or para_num > 0:
                    if input[index] == '(':
                        para_num += 1
                    if input[index] == ')':
                        para_num -= 1
                    index += 1
                index += 1
            elif input[index] == ')':
                if current_statement != "":
                    statement.append(current_statement)
                    current_statement = ""
                return self.translate(statement)
            elif input[index] != ' ':
                current_statement += input[index]
                index += 1
            else:
                if current_statement != "":
                    statement.append(current_statement)
                    current_statement = ""
                index += 1
        return statement
                
                # "(puts (str (equal \"10.5\" \"10\")))"
                
                
    def translate(self, list):
        # print(list)
        fun = list[0]
        if fun == "puts":
            return self.puts(*list[1:])
        elif fun == "set":
            return self.assignment(*list[1:])
        elif fun == "concat":
            return self.st_concat(*list[1:])
        elif fun == "lowercase":
            return self.stlower(*list[1:])
        elif fun == "uppercase":
            return self.stupper(*list[1:])
        elif fun == "replace":
            return self.substringReplace(*list[1:])
        elif fun == "substring":
            return self.substring(*list[1:])
        elif fun == "add":
            return self.add(*list[1:])
        elif fun == "subtract":
            return self.sub(*list[1:])
        elif fun == "multiply":
            return self.multiply(*list[1:])
        elif fun == "divide":
            return self.division(*list[1:])
        elif fun == "abs":
            return self.abosulte(*list[1:])
        elif fun == "max":
            return self.getMax(*list[1:])
        elif fun == "min":
            return self.getMin(*list[1:])
        elif fun == "gt":
            return self.greaterthan(*list[1:])
        elif fun == "lt":
            return self.lessthan(*list[1:])
        elif fun == "equal":
            return self.equal(*list[1:])
        elif fun == "not_equal":
            return self.neq(*list[1:])
        elif fun == "str":
            return self.tostr(*list[1:])

                



        

inter = interpreter()

data = {
#   "expressions": ['(puts (uppercase (str (gt (multiply -578 544 209) (add 8883.3355 -1055.6057 -2013.9854 -3500.5961 -2818.647 3475.1026 7282.5782 1011.2722 1154.0986 -7270.035 5340.9768 9219.8377 -5900.1119 -8446.8187 1965.8317 4939.2569 1610.6371 -4947.0035 -6159.9525 -8791.7588 5378.896 -1918.6328 7549.1682 -1383.7614 7281.5292 -9024.2844 -4513.8298 5915.9689 7163.1792 86.7 -7113.9794 7965.0663 693.3711 208.7207 5942.9972 -8411.0302 -8516.1473 -7906.7576 -2138.0202 -372.0534 -5133.6325 2363.501 -1071.8923 -5928.7298 -1408.9193 -1516.2362 -6208.411 7022.9579 1915.4829 7581.4686 5894.702 8617.0989 7133.6878 4116.429 -2795.9691 -8267.3822 1528.9056 -1731.9748 -1947.4514 5614.9546 2060.4503 -7663.8961 3777.4302 2001.0713 -9914.1587 -2685.8406 -6892.5645 -9039.2103 -4910.3338 435.223 -5397.809 -6625.1084 8476.1897 -2269.2649 -180.7177 -794.1946 -6769.5433 9161.3531 -5963.5231 6389.2478 809.8332 -8180.4435 -7320.3537 5225.223 5622.2469 -8166.3803 -4978.9797 853.0849 -4980.7628 1530.6481 -729.9095 2114.0335 -4895.2116 8429.7454 3317.6713 -1579.1104 -6736.2755 6057.468 215.1525 4457.9315)))))', 
#                   '(puts (str (divide -6612 -8592)))', 
#                   '(puts (str (add -2618 4389 6884 1632 7800 -5191 -551 4144 1466 4541 -399 7501 -6494 -3669 593 -7953 2018 9785 5053 8993 48 8101 8138 7111 -5348 6900 -2452 778 190 -486 7540 -5554 8167 6282 3188 201 -6866 5379 -6938 5353 6687 4620 -708 -8399 7448 -1920 1023 3030 -3685 3583 -9660 -8965 -4620 -9528 4253 9762 5559 9770 6487 8577 -7762 3804 -7079 479 -3210 7818 -5820 -7947 2600 9158 -9326 8051 -4508 8025 365 1373 618 -37 -7011 4048 321 -9430 -7903 -4466 -9997 -9761 6268 3034 8182 2558 -2500 7881 -6545 2249 1393 7866 -14 5929 9438 -8735)))', 
#                   '(puts (uppercase (str (lt (max 779 8788 -5760 4128 3345 9652 4166 -7224 -6107 7622) (abs (min -9158.6475 -7835.6892 3215.8805 7658.2497 -249.6911 -5662.9573 5823.3121 -6299.7194 -520.4722 -4479.5417))))))', 
#                   '(puts (str (multiply -56 -22 89 -8.8652)))', 
#                   '(puts (str (max -376.5056 -1041.3433 -3865.1089 9638.2996 9380.8156 -9367.5786 -555.3423 -6482.5439 -476.4382 -9073.7998 -7551.1046 -6487.3867 -5827.5238 767.2629 -2426.3769 -6095.7349 469.6533 5902.8193 1422.4501 -6626.0089 -5324.073 -714.5879 -9025.7093 -1225.1097 -2477.8409 1538.9522 -5293.6995 8468.3599 5512.272 9791.7318 8924.1706 9081.9038 -533.007 2524.869 -9272.9593 2785.6661 -8872.3477 3214.8005 220.687 -6688.015 851.7484 7443.2725 -522.569 2573.2348 3224.3057 -8285.7376 -2711.757 -9957.4903 4411.4498 1221.3951 -423.1265 486.361 -1346.1204 -3887.3662 -6075.7215 6080.7663 613.5938 -7709.1422 -436.9397 -2097.7046 -243.9954 -778.8601 -6029.6353 -7764.5164 -459.2073 -2855.4967 -5302.012 -8595.6474 -219.0925 -4006.6959 -337.6088 -7044.164 6060.0657 4874.7501 -7180.6499 -4206.7502 -1016.201 3831.5093 2210.5248 -3201.1312 5631.012 3672.1779 -1998.0471 -3512.028 722.639 2868.7363 1516.8874 8066.1976 1403.2303 -3597.1766 -2731.3275 -1883.3469 4689.4524 -444.4872 475.5998 3580.2596 9549.5661 -5682.7079 -7106.1276 -8906.7722)))', 
#                   '(puts (str (min -839 -2590 3371 -5852 -5497 5461 -790 -3307 -8422 2787 4937 3218 -2538 -2284 7404 -9903 2392 -3029 5987 7669 -5087 1682 -5294 231 -8121 -3340 -9761 3302 8423 8460 -1151 -3083 -5061 -7890 4914 -4926 1330 7193 3653 4168 -6234 -1013 5516 7050 7546 3202 8519 -3260 6789 -3929 8630 8256 2528 4290 -4969 -2450 -3439 -4286 4609 4172 1385 7672 -6107 5655 -2423 -6575 -7362 4858 4961 -846 -2520 3752 -2023 9128 -4372 -3764 4052 -2572 3558 3254 6910 1635 3919 4781 8158 -920 -749 1494 7855 4166 -4724 -9216 4771 8366 8128 -5573 6790 46 -2345 1338 2196.4802)))', 
#                   '(puts (str (concat (concat "G3t:xxItx1y3k3hNWvj_uT>StiZjTO_7X4VNo>3zK@MCUSN>MPUZl35tTOo_>BGwYbdEihTTLBvR^GJyBjaFSX1N2we[^d4DlE<Jv`TRtBE1N]5ZeNwoCJyxZ@1[>GSjP3>EN`b8cc_j?W:fN_v_cU8nl1g8JEm4w81qWRz^qI5se:Cwq>rCx<OPQ:e[W0;4BZL>?" "3WQ>wWCcqAXPIzD]b?c;ln?m=aMdq@5y3F>?Qt]JLP=gAfUQ114oKwg`YavYUKI?]^8N6J]@G5N_QGq4rwZ0idUt6Am3lqL<i]TD_pgxEjKM_a<QG]kPk=M@EaFOQuLGl[h:=nB=3yyP9>uoOy>[9N4hQ") (str (divide -6709 0)))))'
#                   ]
    "expressions": ['(set integer 3571)', '(puts (str (min -6793.2542 -881.804 -5855.1282 9553.2677 -2827.2686 8653.1933 -4285.4174 8800.5244 -7400.1013 -9392.4838 -6999.3198 -9544.3795 2423.9715 2516.5775 5732.3224 9826.9646 9588.1015 -2658.8987 4991.013 3849.2933 9631.4483 -6177.8205 -9345.3672 -5853.149 8422.9775 5726.7487 7087.3448 -9922.5071 5946.7117 -7178.3715 -3991.7834 -377.8366 -3657.896 1687.6651 2540.4958 5082.1077 7712.6126 839.6264 -5175.3332 28.355 703.3311 9970.0534 4115.1373 -7307.3346 1860.0029 -8981.8619 -5818.5971 -4160.741 3799.067 -179.9052 -2020.4614 9208.5699 -5362.8407 -3517.038 -3330.5141 -7216.0994 5658.4787 -610.7228 6890.4184 4915.1224 -5567.1607 -7560.9721 5666.0896 1328.897 5377.4427 -4239.3325 9079.8601 -4242.0258 -7707.4722 -2412.2851 4842.0612 2362.5943 -4714.221 -5241.6083 -7537.6642 -5949.5655 7431.1831 1725.74 -3231.4161 8287.038 -5839.338 -4792.9912 -7278.1072 -2541.3327 4158.4178 5717.7764 9564.5959 8241.5069 -8558.0647 6844.6027 7016.0994 6822.7021 -52.4738 -5364.1955 -3219.896 -1917.4206 -3575.5406 9734.1196 5692.9863 3614.0299)))', '(puts (str (subtract 7040 -3797.2093)))', '(puts (str (divide 1559 4833.5726)))', '(puts (str (abs -7311)))', '(puts (str (max -7436.2597 6037.3712 -3848.9988 8774.8181 -5017.3059 -6947.0579 -2234.1073 -6076.1926 -997.5785 8322.4692 6681.2841 -2019.0622 8900.104 -1906.7632 -2583.0857 7309.0147 1700.8448 1586.8974 -5766.9873 -9022.2763 2990.1068 -670.649 -8031.1853 907.7643 8841.9054 -1497.6666 -6591.3394 -1403.0013 -7842.2969 1262.163 -3474.0647 -266.4496 965.9343 5731.0467 -9670.7417 8873.937 6058.5841 -4148.7329 -369.8817 -3116.6758 -7830.9433 8218.1773 -2113.576 3985.5103 -2041.4208 -827.8817 -9896.9745 5085.2356 1727.2364 -5427.9439 7741.0274 -6564.1266 -8188.5671 -1740.338 2961.8037 -9123.2804 -6122.8657 3142.0566 6124.6983 -7629.8154 -3796.3223 3282.4463 8460.2303 2086.798 -6447.8386 5625.6896 -5146.3386 5255.6235 623.9874 -2217.2798 -7016.7395 -4992.7102 -8503.4095 9446.9379 1373.3452 547.9139 -5721.6245 -4234.2244 5921.305 -9701.5791 -922.0591 -9421.8989 -1812.9044 2042.4364 2412.4411 -6340.1892 2582.9846 7618.4032 -5284.9361 -3807.3723 -4568.9811 -9059.5125 -3445.8022 3793.5939 -4058.8346 4718.2422 -7242.7992 9663.8152 -4267.0352 -3320.6401)))', '(puts (str (multiply 932 -410 230)))', '(puts (str (add -6061 4064 -65 6577 -6834 -8393 -6822 1709 -6795 -9538 2468 -570 1548 9590 8125 -5547 -7026 -9948 6561 -2853 -442 500 -8683 -6233 1544 -930 1534 7257 9315 -8481 3463 3659 8231 -2713 9936 -4883 -8557 -9565 -8169 3211 -6537 -9313 -9325 -2972 -9260 9636 -7140 1364 6015 2807 7020.8096)))', '(puts (str (equal (puts (lowercase "94rlH_r[Xo7Y`QaJe^FXxy8huP=I[qJ[NAkc;tQjd^i0iSFe>lGSXIHx7cAhqZ8onMVaY?Q1mZThjk]3v>fChQ5coA^qU]W0Z[L;Ns2>7v^0vQn]tVXW]<@Twst?V2j4;=_<rszm=kpNJaAL?fvx?gq`i]@gWe?UVJ1u6A?lAU9:2pMM6oxy<vY?QB@Ey6<eVg")) (puts (uppercase "U6Yj:`S>a0p4qwZf5H8x18=SiPOvMr34jO`cEY9b:=KPLBkmcVu`uuzaUPWE:0_KMRwCKNcdpqGk2flp]Hi@ZmAru_iaz:AEcsLym4j3SAPX39fVemBqsFoQw?YhK1Vv=Y:>sPlMQ`0mAk_FkY2knecHME>D7_u1?8Tr@gzWo1[Rx;>R^Vsm^OCo")))))', '(puts (str (divide -7510 206)))', '(puts (concat (str integer) (uppercase "o00000oo00000o")))', '(puts (subtract integer 2357.6438))'],
}
ans = []
for index, input in enumerate(data["expressions"]):
    result = inter.interpreter_func(input)[0]
    print(result)
    if result:
        ans.append(result.strip("\""))
    else:
        ans.append("ERROR at line " + str(index + 1))
print({"output": ans})
        

@app.route('/lisp-parser', methods=['POST'])
def square():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    ans = []
    for index, input in enumerate(data["expressions"]):
        result = inter.interpreter_func(input)[0].strip("\"")
        if result != "False":
            ans.append(result)
        else:
            ans.append("ERROR at line " + str(index + 1))
    # print({"output": ans})
    return jsonify({"output": ans})