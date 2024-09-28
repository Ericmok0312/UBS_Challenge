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
            if (arg[i].replace('.', '', 1).isdigit() or arg[i].replace('e', '', 1).replace('+', '').replace('-', '').replace('.', '', 1).isdigit() or (arg[i][0] == '-' and arg[i][1:].replace('e', '', 1).replace('+', '').replace('-', '').replace('.', '', 1).isdigit())):
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
            if (arg[i].replace('.', '', 1).isdigit() or arg[i].replace('e', '', 1).replace('+', '').replace('-', '').replace('.', '', 1).isdigit() or (arg[i][0] == '-' and arg[i][1:].replace('e', '', 1).replace('+', '').replace('-', '').replace('.', '', 1).isdigit())):
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
            if (arg[i].replace('.', '', 1).isdigit() or arg[i].replace('e', '', 1).replace('+', '').replace('-', '').replace('.', '', 1).isdigit() or (arg[i][0] == '-' and arg[i][1:].replace('e', '', 1).replace('+', '').replace('-', '').replace('.', '', 1).isdigit())):
                ls.append(arg[i])
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
            if (arg[i].replace('.', '', 1).isdigit() or arg[i].replace('e', '', 1).replace('+', '').replace('-', '').replace('.', '', 1).isdigit() or (arg[i][0] == '-' and arg[i][1:].replace('e', '', 1).replace('+', '').replace('-', '').replace('.', '', 1).isdigit())):
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
            if (arg[i].replace('.', '', 1).isdigit() or arg[i].replace('e', '', 1).replace('+', '').replace('-', '').replace('.', '', 1).isdigit() or (arg[i][0] == '-' and arg[i][1:].replace('e', '', 1).replace('+', '').replace('-', '').replace('.', '', 1).isdigit())):
                ls.append(arg[i])
                ls.append(arg[i])
            else:
                return False

        return str(abs(float(ls[0])))


    def getMax(self, *arg):
        ls = []

        if(len(arg)<2):
            return False

        for i in range(len(arg)):
            if (arg[i].replace('.', '', 1).isdigit() or arg[i].replace('e', '', 1).replace('+', '').replace('-', '').replace('.', '', 1).isdigit() or (arg[i][0] == '-' and arg[i][1:].replace('e', '', 1).replace('+', '').replace('-', '').replace('.', '', 1).isdigit())):
                ls.append(float(arg[i]))
            else:
                return False

        
        return str(max(ls))

    def getMin(self, *arg):
        ls = []

        if(len(arg)<2):
            return False

        for i in range(len(arg)):
            if (arg[i].replace('.', '', 1).isdigit() or arg[i].replace('e', '', 1).replace('+', '').replace('-', '').replace('.', '', 1).isdigit() or (arg[i][0] == '-' and arg[i][1:].replace('e', '', 1).replace('+', '').replace('-', '').replace('.', '', 1).isdigit())):
                ls.append(float(arg[i]))
            else:
                return False

        
        return str(min(ls))

    def greaterthan(self, *arg):
        if not(len(arg)==2):
            return False

        ls = []
        for i in range(len(arg)):
            if (arg[i].replace('.', '', 1).isdigit() or arg[i].replace('e', '', 1).replace('+', '').replace('-', '').replace('.', '', 1).isdigit() or (arg[i][0] == '-' and arg[i][1:].replace('e', '', 1).replace('+', '').replace('-', '').replace('.', '', 1).isdigit())):
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
            if (arg[i].replace('.', '', 1).isdigit() or arg[i].replace('e', '', 1).replace('+', '').replace('-', '').replace('.', '', 1).isdigit() or (arg[i][0] == '-' and arg[i][1:].replace('e', '', 1).replace('+', '').replace('-', '').replace('.', '', 1).isdigit())):
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
                result = self.interpreter_func(input[index + 1:])
                if not result:
                    return False
                else:
                    statement.append(result)
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
    # "expressions": ['(set integer 3571)', '(puts (str (min -6793.2542 -881.804 -5855.1282 9553.2677 -2827.2686 8653.1933 -4285.4174 8800.5244 -7400.1013 -9392.4838 -6999.3198 -9544.3795 2423.9715 2516.5775 5732.3224 9826.9646 9588.1015 -2658.8987 4991.013 3849.2933 9631.4483 -6177.8205 -9345.3672 -5853.149 8422.9775 5726.7487 7087.3448 -9922.5071 5946.7117 -7178.3715 -3991.7834 -377.8366 -3657.896 1687.6651 2540.4958 5082.1077 7712.6126 839.6264 -5175.3332 28.355 703.3311 9970.0534 4115.1373 -7307.3346 1860.0029 -8981.8619 -5818.5971 -4160.741 3799.067 -179.9052 -2020.4614 9208.5699 -5362.8407 -3517.038 -3330.5141 -7216.0994 5658.4787 -610.7228 6890.4184 4915.1224 -5567.1607 -7560.9721 5666.0896 1328.897 5377.4427 -4239.3325 9079.8601 -4242.0258 -7707.4722 -2412.2851 4842.0612 2362.5943 -4714.221 -5241.6083 -7537.6642 -5949.5655 7431.1831 1725.74 -3231.4161 8287.038 -5839.338 -4792.9912 -7278.1072 -2541.3327 4158.4178 5717.7764 9564.5959 8241.5069 -8558.0647 6844.6027 7016.0994 6822.7021 -52.4738 -5364.1955 -3219.896 -1917.4206 -3575.5406 9734.1196 5692.9863 3614.0299)))', '(puts (str (subtract 7040 -3797.2093)))', '(puts (str (divide 1559 4833.5726)))', '(puts (str (abs -7311)))', '(puts (str (max -7436.2597 6037.3712 -3848.9988 8774.8181 -5017.3059 -6947.0579 -2234.1073 -6076.1926 -997.5785 8322.4692 6681.2841 -2019.0622 8900.104 -1906.7632 -2583.0857 7309.0147 1700.8448 1586.8974 -5766.9873 -9022.2763 2990.1068 -670.649 -8031.1853 907.7643 8841.9054 -1497.6666 -6591.3394 -1403.0013 -7842.2969 1262.163 -3474.0647 -266.4496 965.9343 5731.0467 -9670.7417 8873.937 6058.5841 -4148.7329 -369.8817 -3116.6758 -7830.9433 8218.1773 -2113.576 3985.5103 -2041.4208 -827.8817 -9896.9745 5085.2356 1727.2364 -5427.9439 7741.0274 -6564.1266 -8188.5671 -1740.338 2961.8037 -9123.2804 -6122.8657 3142.0566 6124.6983 -7629.8154 -3796.3223 3282.4463 8460.2303 2086.798 -6447.8386 5625.6896 -5146.3386 5255.6235 623.9874 -2217.2798 -7016.7395 -4992.7102 -8503.4095 9446.9379 1373.3452 547.9139 -5721.6245 -4234.2244 5921.305 -9701.5791 -922.0591 -9421.8989 -1812.9044 2042.4364 2412.4411 -6340.1892 2582.9846 7618.4032 -5284.9361 -3807.3723 -4568.9811 -9059.5125 -3445.8022 3793.5939 -4058.8346 4718.2422 -7242.7992 9663.8152 -4267.0352 -3320.6401)))', '(puts (str (multiply 932 -410 230)))', '(puts (str (add -6061 4064 -65 6577 -6834 -8393 -6822 1709 -6795 -9538 2468 -570 1548 9590 8125 -5547 -7026 -9948 6561 -2853 -442 500 -8683 -6233 1544 -930 1534 7257 9315 -8481 3463 3659 8231 -2713 9936 -4883 -8557 -9565 -8169 3211 -6537 -9313 -9325 -2972 -9260 9636 -7140 1364 6015 2807 7020.8096)))', '(puts (str (equal (puts (lowercase "94rlH_r[Xo7Y`QaJe^FXxy8huP=I[qJ[NAkc;tQjd^i0iSFe>lGSXIHx7cAhqZ8onMVaY?Q1mZThjk]3v>fChQ5coA^qU]W0Z[L;Ns2>7v^0vQn]tVXW]<@Twst?V2j4;=_<rszm=kpNJaAL?fvx?gq`i]@gWe?UVJ1u6A?lAU9:2pMM6oxy<vY?QB@Ey6<eVg")) (puts (uppercase "U6Yj:`S>a0p4qwZf5H8x18=SiPOvMr34jO`cEY9b:=KPLBkmcVu`uuzaUPWE:0_KMRwCKNcdpqGk2flp]Hi@ZmAru_iaz:AEcsLym4j3SAPX39fVemBqsFoQw?YhK1Vv=Y:>sPlMQ`0mAk_FkY2knecHME>D7_u1?8Tr@gzWo1[Rx;>R^Vsm^OCo")))))', '(puts (str (divide -7510 206)))', '(puts (concat (str integer) (uppercase "o00000oo00000o")))', '(puts (subtract integer 2357.6438))'],
    # "expressions":["(set x 15)","(puts (str (subtract x 5)))"]
    
    
    
    
    
# "expressions": ['(puts (concat "MyParser" "IsBest"))']
# 2024-09-28 15:37:10,211 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:10] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (str (multiply 3 -2.5)))']
# 2024-09-28 15:37:10,716 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:10] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(set x (add (multiply -7972 7616) (subtract 6927 (divide 5483 -7929))))', '(set y (divide (add x -6173) 7769))', '(puts (str (multiply y (subtract 4147 (divide x -4796)))))']
# 2024-09-28 15:37:11,219 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:11] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (str (equal "True" "true")))']
# 2024-09-28 15:37:11,591 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:11] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (str (divide 10 4)))']
# 2024-09-28 15:37:11,973 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:11] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (str (multiply -100.567)))']
# 2024-09-28 15:37:12,354 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:12] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (replace "yzyzyzyzABCDEFGHIJKLMNOPQRSTyzyzyzyzy" "zy" "mn"))']
# 2024-09-28 15:37:12,765 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:12] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (uppercase (str (gt (multiply -578 544 209) (add 8883.3355 -1055.6057 -2013.9854 -3500.5961 -2818.647 3475.1026 7282.5782 1011.2722 1154.0986 -7270.035 5340.9768 9219.8377 -5900.1119 -8446.8187 1965.8317 4939.2569 1610.6371 -4947.0035 -6159.9525 -8791.7588 5378.896 -1918.6328 7549.1682 -1383.7614 7281.5292 -9024.2844 -4513.8298 5915.9689 7163.1792 86.7 -7113.9794 7965.0663 693.3711 208.7207 5942.9972 -8411.0302 -8516.1473 -7906.7576 -2138.0202 -372.0534 -5133.6325 2363.501 -1071.8923 -5928.7298 -1408.9193 -1516.2362 -6208.411 7022.9579 1915.4829 7581.4686 5894.702 8617.0989 7133.6878 4116.429 -2795.9691 -8267.3822 1528.9056 -1731.9748 -1947.4514 5614.9546 2060.4503 -7663.8961 3777.4302 2001.0713 -9914.1587 -2685.8406 -6892.5645 -9039.2103 -4910.3338 435.223 -5397.809 -6625.1084 8476.1897 -2269.2649 -180.7177 -794.1946 -6769.5433 9161.3531 -5963.5231 6389.2478 809.8332 -8180.4435 -7320.3537 5225.223 5622.2469 -8166.3803 -4978.9797 853.0849 -4980.7628 1530.6481 -729.9095 2114.0335 -4895.2116 8429.7454 3317.6713 -1579.1104 -6736.2755 6057.468 215.1525 4457.9315)))))', '(puts (str (divide -6612 -8592)))', '(puts (str (add -2618 4389 6884 1632 7800 -5191 -551 4144 1466 4541 -399 7501 -6494 -3669 593 -7953 2018 9785 5053 8993 48 8101 8138 7111 -5348 6900 -2452 778 190 -486 7540 -5554 8167 6282 3188 201 -6866 5379 -6938 5353 6687 4620 -708 -8399 7448 -1920 1023 3030 -3685 3583 -9660 -8965 -4620 -9528 4253 9762 5559 9770 6487 8577 -7762 3804 -7079 479 -3210 7818 -5820 -7947 2600 9158 -9326 8051 -4508 8025 365 1373 618 -37 -7011 4048 321 -9430 -7903 -4466 -9997 -9761 6268 3034 8182 2558 -2500 7881 -6545 2249 1393 7866 -14 5929 9438 -8735)))', '(puts (uppercase (str (lt (max 779 8788 -5760 4128 3345 9652 4166 -7224 -6107 7622) (abs (min -9158.6475 -7835.6892 3215.8805 7658.2497 -249.6911 -5662.9573 5823.3121 -6299.7194 -520.4722 -4479.5417))))))', '(puts (str (multiply -56 -22 89 -8.8652)))', '(puts (str (max -376.5056 -1041.3433 -3865.1089 9638.2996 9380.8156 -9367.5786 -555.3423 -6482.5439 -476.4382 -9073.7998 -7551.1046 -6487.3867 -5827.5238 767.2629 -2426.3769 -6095.7349 469.6533 5902.8193 1422.4501 -6626.0089 -5324.073 -714.5879 -9025.7093 -1225.1097 -2477.8409 1538.9522 -5293.6995 8468.3599 5512.272 9791.7318 8924.1706 9081.9038 -533.007 2524.869 -9272.9593 2785.6661 -8872.3477 3214.8005 220.687 -6688.015 851.7484 7443.2725 -522.569 2573.2348 3224.3057 -8285.7376 -2711.757 -9957.4903 4411.4498 1221.3951 -423.1265 486.361 -1346.1204 -3887.3662 -6075.7215 6080.7663 613.5938 -7709.1422 -436.9397 -2097.7046 -243.9954 -778.8601 -6029.6353 -7764.5164 -459.2073 -2855.4967 -5302.012 -8595.6474 -219.0925 -4006.6959 -337.6088 -7044.164 6060.0657 4874.7501 -7180.6499 -4206.7502 -1016.201 3831.5093 2210.5248 -3201.1312 5631.012 3672.1779 -1998.0471 -3512.028 722.639 2868.7363 1516.8874 8066.1976 1403.2303 -3597.1766 -2731.3275 -1883.3469 4689.4524 -444.4872 475.5998 3580.2596 9549.5661 -5682.7079 -7106.1276 -8906.7722)))', '(puts (str (min -839 -2590 3371 -5852 -5497 5461 -790 -3307 -8422 2787 4937 3218 -2538 -2284 7404 -9903 2392 -3029 5987 7669 -5087 1682 -5294 231 -8121 -3340 -9761 3302 8423 8460 -1151 -3083 -5061 -7890 4914 -4926 1330 7193 3653 4168 -6234 -1013 5516 7050 7546 3202 8519 -3260 6789 -3929 8630 8256 2528 4290 -4969 -2450 -3439 -4286 4609 4172 1385 7672 -6107 5655 -2423 -6575 -7362 4858 4961 -846 -2520 3752 -2023 9128 -4372 -3764 4052 -2572 3558 3254 6910 1635 3919 4781 8158 -920 -749 1494 7855 4166 -4724 -9216 4771 8366 8128 -5573 6790 46 -2345 1338 2196.4802)))', '(puts (str (concat (concat "G3t:xxItx1y3k3hNWvj_uT>StiZjTO_7X4VNo>3zK@MCUSN>MPUZl35tTOo_>BGwYbdEihTTLBvR^GJyBjaFSX1N2we[^d4DlE<Jv`TRtBE1N]5ZeNwoCJyxZ@1[>GSjP3>EN`b8cc_j?W:fN_v_cU8nl1g8JEm4w81qWRz^qI5se:Cwq>rCx<OPQ:e[W0;4BZL>?" "3WQ>wWCcqAXPIzD]b?c;ln?m=aMdq@5y3F>?Qt]JLP=gAfUQ114oKwg`YavYUKI?]^8N6J]@G5N_QGq4rwZ0idUt6Am3lqL<i]TD_pgxEjKM_a<QG]kPk=M@EaFOQuLGl[h:=nB=3yyP9>uoOy>[9N4hQ") (str (divide -6709 0)))))']
# 2024-09-28 15:37:13,145 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:13] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(set x (divide (add 8994 (subtract (multiply -2058 -387) -8390)) (multiply 4629 -5120)))', '(puts (concat (str (equal x -9817)) "B;3VtDXm;5IZtWT^E0zni9lWG>hIB@PqaS@SF2L>[eQx8Kg5q;om"))', '(puts (str (add x (replace (str 3452) "1s9DJGEoxXPPHN^y]0RFY]TCYNbx>ojp>Dq=qXTrkUKMTucK>2KgRchowka72JxjT;JOemSB>>s4TmIvqksUfUIG`2g=^5gg7Gae0>1W`x3XZNH;zazQ>dhCmw1wc_qe8wOi>1UvmnxJ_S8vz@l2e]Zj^UfJuJlJ" "qD@]wsSMm1fN;7KG33ojjcs@rn_o<t^J7:1njFGT<k"))))']
# 2024-09-28 15:37:13,520 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:13] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(set integer 3571)', '(puts (str (min -6793.2542 -881.804 -5855.1282 9553.2677 -2827.2686 8653.1933 -4285.4174 8800.5244 -7400.1013 -9392.4838 -6999.3198 -9544.3795 2423.9715 2516.5775 5732.3224 9826.9646 9588.1015 -2658.8987 4991.013 3849.2933 9631.4483 -6177.8205 -9345.3672 -5853.149 8422.9775 5726.7487 7087.3448 -9922.5071 5946.7117 -7178.3715 -3991.7834 -377.8366 -3657.896 1687.6651 2540.4958 5082.1077 7712.6126 839.6264 -5175.3332 28.355 703.3311 9970.0534 4115.1373 -7307.3346 1860.0029 -8981.8619 -5818.5971 -4160.741 3799.067 -179.9052 -2020.4614 9208.5699 -5362.8407 -3517.038 -3330.5141 -7216.0994 5658.4787 -610.7228 6890.4184 4915.1224 -5567.1607 -7560.9721 5666.0896 1328.897 5377.4427 -4239.3325 9079.8601 -4242.0258 -7707.4722 -2412.2851 4842.0612 2362.5943 -4714.221 -5241.6083 -7537.6642 -5949.5655 7431.1831 1725.74 -3231.4161 8287.038 -5839.338 -4792.9912 -7278.1072 -2541.3327 4158.4178 5717.7764 9564.5959 8241.5069 -8558.0647 6844.6027 7016.0994 6822.7021 -52.4738 -5364.1955 -3219.896 -1917.4206 -3575.5406 9734.1196 5692.9863 3614.0299)))', '(puts (str (subtract 7040 -3797.2093)))', '(puts (str (divide 1559 4833.5726)))', '(puts (str (abs -7311)))', '(puts (str (max -7436.2597 6037.3712 -3848.9988 8774.8181 -5017.3059 -6947.0579 -2234.1073 -6076.1926 -997.5785 8322.4692 6681.2841 -2019.0622 8900.104 -1906.7632 -2583.0857 7309.0147 1700.8448 1586.8974 -5766.9873 -9022.2763 2990.1068 -670.649 -8031.1853 907.7643 8841.9054 -1497.6666 -6591.3394 -1403.0013 -7842.2969 1262.163 -3474.0647 -266.4496 965.9343 5731.0467 -9670.7417 8873.937 6058.5841 -4148.7329 -369.8817 -3116.6758 -7830.9433 8218.1773 -2113.576 3985.5103 -2041.4208 -827.8817 -9896.9745 5085.2356 1727.2364 -5427.9439 7741.0274 -6564.1266 -8188.5671 -1740.338 2961.8037 -9123.2804 -6122.8657 3142.0566 6124.6983 -7629.8154 -3796.3223 3282.4463 8460.2303 2086.798 -6447.8386 5625.6896 -5146.3386 5255.6235 623.9874 -2217.2798 -7016.7395 -4992.7102 -8503.4095 9446.9379 1373.3452 547.9139 -5721.6245 -4234.2244 5921.305 -9701.5791 -922.0591 -9421.8989 -1812.9044 2042.4364 2412.4411 -6340.1892 2582.9846 7618.4032 -5284.9361 -3807.3723 -4568.9811 -9059.5125 -3445.8022 3793.5939 -4058.8346 4718.2422 -7242.7992 9663.8152 -4267.0352 -3320.6401)))', '(puts (str (multiply 932 -410 230)))', '(puts (str (add -6061 4064 -65 6577 -6834 -8393 -6822 1709 -6795 -9538 2468 -570 1548 9590 8125 -5547 -7026 -9948 6561 -2853 -442 500 -8683 -6233 1544 -930 1534 7257 9315 -8481 3463 3659 8231 -2713 9936 -4883 -8557 -9565 -8169 3211 -6537 -9313 -9325 -2972 -9260 9636 -7140 1364 6015 2807 7020.8096)))', '(puts (str (equal (puts (lowercase "94rlH_r[Xo7Y`QaJe^FXxy8huP=I[qJ[NAkc;tQjd^i0iSFe>lGSXIHx7cAhqZ8onMVaY?Q1mZThjk]3v>fChQ5coA^qU]W0Z[L;Ns2>7v^0vQn]tVXW]<@Twst?V2j4;=_<rszm=kpNJaAL?fvx?gq`i]@gWe?UVJ1u6A?lAU9:2pMM6oxy<vY?QB@Ey6<eVg")) (puts (uppercase "U6Yj:`S>a0p4qwZf5H8x18=SiPOvMr34jO`cEY9b:=KPLBkmcVu`uuzaUPWE:0_KMRwCKNcdpqGk2flp]Hi@ZmAru_iaz:AEcsLym4j3SAPX39fVemBqsFoQw?YhK1Vv=Y:>sPlMQ`0mAk_FkY2knecHME>D7_u1?8Tr@gzWo1[Rx;>R^Vsm^OCo")))))', '(puts (str (divide -7510 206)))', '(puts (concat (str integer) (uppercase "o00000oo00000o")))', '(puts (subtract integer 2357.6438))']
# 2024-09-28 15:37:13,902 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:13] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(set x (add 3371 (multiply 5235 6669)))', '(set y (subtract x (divide (multiply -1695 298) (add -1019 -273))))', '(puts (str (add (multiply x y) (divide 2869 -175))))', '(puts (concat (uppercase (str y)) "vqS5joiwX^oH5efguQqe8IVdbatE2kW2<qHt42Ig^nwBkd<83:UT;hgeCnM8r87hCBqB5v^DqxQP=>bU1d=1vtnTf6u69j;6Cf2>;^vsfx`0MPgou1f@JK0sYs`_Ckia39mRJ`=JDUygpA"))']
# 2024-09-28 15:37:14,404 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:14] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (str (add 1 2)))']
# 2024-09-28 15:37:14,781 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:14] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(set x (str (multiply 5101 -9424)))', '(set y (str (divide 4749 -2770)))', '(set z (concat x y))', '(puts (str (equal z "0IpU1sf_MA7<0D6rc6xX=T@F]144mnUU<5R3]pxBYixhakiXM[r?Pzwu`OvkRv7L4ht<fwXGE^usPaYZ:ko>]yXJH>kI3RhB6ch;_I`1IRZkug")))', '(puts (str (equal z (concat x "UkePz:Nq`tGhe31ezn840vr6MOG_Lq2tFX0Bfb^u73J[Mi0pa3cT:2:e9e>Iqw7ppjwsWi<btI29zWPou23PBwJiKY"))))', '(puts (str (equal z "cTLO8Zs0_k;3e`OcZU_SNiGGIk9v5l8g9tfcuR6]LL4LyaMaqbBQwS")))']
# 2024-09-28 15:37:15,167 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:15] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(set x 5316)', '(puts (str (subtract x 5865)))']
# 2024-09-28 15:37:15,548 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:15] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (concat (concat "@<Y:OzYS;cAzR0;1`1?OQsKeVCK?7ot4lS][3GZ6MzrKT3@cPgsVn2OOEHq`rqm0UbePe@RpgKJs`ieeC[O1JlD2[e[JKN:Mqt89`<MoUjUOa3OeJD>Qp^fKUCQPfBKvwjBBOwpI5eyniM9E0_aESAQGUrqV@Le`S" "kZHIkSpjB=rxF]`AX[Qdjex`uDHTX<eJR=daRwMrjARaH;nT4z?nK[Ov^otylehk^88ir7_PCRuSD4Rox^6zN1^rRr6HBP2nss[ef") (lowercase "4_0h8MsDP")))', '(puts (str (substring (concat (concat "`40;c7gH[" "vN?cJ_") (lowercase "sXtGZo1")) (min (abs (multiply 5 4 -10 1 -6 4 4 0 -8)) 0) (min (abs (add -1125 7355 3966 1622 4056 5471 7843 656 8386 -8626 -1353 -977 6405 -6313 -6680 -8484 3657 6973 -3597 -2551 -1352 9375 -5527 -3692 9538 9694 4731 -6845 -4587 -2292 4495 -4704 1848 3153 7715 -6927 9765 6993 2639 6334 -5777 -18 1958 -4155 -8271 -7448 4177 -9188 -7739 -441 6485 -1209 -271 -2063 -3612 8854 1318 6791 8662 -3439 7287 -8798 2830 3203 5847 8972 3804 -7566 4075 -173 8507 3809 2450 591 -6992 4613 -4395 -2503 -5182 2816 2036 8543 4293 -211 -1507 5340 7621 3355 5408 9917 2016 -3044 -5316 -4857 1205 3618 4321 4402 -826 1075)) 5))))', '(set bb (lowercase (concat "CbwxTre5NE;3AHr]y;3Sc9[E2ljQ?Uc8NAK22sbvRKmw;BPPM39`cUl7_6jL^n[wRw0md_6DS5HKNi6gi^kR@UqZv<" "rKesW`N5Z]Cn3DsSc>rOUWgQAoo>]bWclH?_u1ndDWPWLJE>KwZP7S@DH:8bz]pa88cqAbESJC6^?D>84`6@f3kOwn0S4;HusjfVtSJt0`HJlA3xC1k>Qj<fGn=L8^gj23IShcJrXf")))', '(set aa (concat "30xGmRH0iYGoxIH[9U7^_HWK_83w^QTdD?B=ZK<A=8P6OBFQSCEFpm2m@f@qFBwAf5SF2F;kU[n3GWokHS:magj=Bbz2qXsb51AxxW:>oc<orz9B<URFCaTOL2B68" "JP1BfZ`Tf=4tROGO>s?O6[koqv_gI@6]_wpMM`OYtvbxzpKpCIC^S1FSjB8`jbK^aW556[Z280auL76XM9mrnceLWC]Y8pumNj<q?^xnuPjUN:MGno="))', '(puts (replace aa "a" "varA"))', '(puts (replace bb "b" "varB"))', '(puts (replace (lowercase aaa) "a" "varA"))']
# 2024-09-28 15:37:15,941 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:15] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts "ERROR at line 3")', '(set a (add 1552 5068 -6484 249 2067 -6677 2973 2884 -6799 4885 -8911 1031 -9081 5428 9040 -7951 -1350 -2720 -7411 -285 -2930 7629 -7423 7339 -8181 8302 -7720 7563 -9541 -4953 -6564 -1333 2390 -477 -4731 7553 1203 7498 -8182 -4188 3271 5562 -7634 -6743 -7886 -4642 283 -886 -6869 3747 -3083 7356 -5818 -337 1114 492 5451 5963 -1609 3109 -4437 -1120 -6182 8740 790 3566 -1642 -6916 9418 4115 5797 3435 -3397 5562 8149 9785 -2102 -9779 -7264 -1029 -649 -3935 -5285 9382 -2049 -9892 -1271 -1647 -7307 3647 4002 -3767 -1031 -9265 -952 -9312 -6410 1795 7335 -2052 -2991.7736))', '(puts (str a))']
# 2024-09-28 15:37:16,454 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:16] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (replace "hello world" "world" ""))']
# 2024-09-28 15:37:16,828 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:16] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (replace (replace (concat (uppercase "WibFzOkX^yTJsydNtgn>J3N") (lowercase "u@sej[xPo;wQ^MagCy1]][<q0m70cilCmmhydepb<y0bf=?O0XIbhH01y`S_Nbs15b]K7XP^EK>Zgo?WOi84paPrurnwD9nm^nYq_2OOS=qS=B4FJPg1400ryg")) "l" "x") "o" "y"))']
# 2024-09-28 15:37:17,198 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:17] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (str (not_equal (abs (subtract 5169 -2382)) -8376)))', '(puts (str (gt (multiply 111 -801 -760) 4060)))', '(puts (str (lt (divide 2982 -6617) (multiply -3433 5345))))']
# 2024-09-28 15:37:17,575 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:17] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(set a (add -9003 (multiply (subtract -1160 (divide 1387 -709)) (add 4157 (max 9410 5502)))))', '(set b (concat (lowercase (str a)) "5FoueO<<7ZyzOQgQe2R`y0L1uNUzCqwO4uwAIe3qPWx`af[lb<6=72GIe3fUV:nXCXrK<<Zi]E8PqWZ><<`wY<S0PuNF:9Yb^rBj`tHa6z<GGPJrxsbp=`G>3Oy9RpYARtx<a`j[z0C:n[>ABFiDOaE]Ii4[KD=7sX^w7^2riQaA0gO4xJ^ZbJPsoW1rNNcX@BBIuEa"))', '(puts (replace b "[kII>E2J3c0Ql4S^9Z<X^s=WN:zx5F<=ZFOz2XtWmRNWT" (str (add 4777 (subtract 9458 -3731)))))', '(puts (str (equal a -2320)))', '(puts (concat b "0p7d2FKLVd;:cTZBHn[B5yJ`xts@b]E0Ois5e]9>PH5S=X=Ye90y9zlFmJY;[vPbOPmHlgW4]41W@:=RzS[S4rEz6SNJ8=OWR0uRfL@>iI^FCnKz_Wac<u9dt6I2o@WOFiS7QbxDUF9mmMsEn@KdoqmLdPJ>oFZsW`gbp>c=L]pSKwYF8?"))']
# 2024-09-28 15:37:17,962 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:17] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(set a null)', '(set b (concat "E>Zfbjcoj^<" "^[EEPrRK6z`Bxj`Iec3F];7dLX:`3XtOZVXpv7V9r][4isW3OMEr:<mX@<VnYg<W=Io"))', '(puts (str (equal a b)))', '(set c (equal null a))', '(puts (str (equal (str c) "I8X=z@Zm_8ToJw>rkPk6aw<Z;L=1WRIbo>g6fzwzJ>e2dFOnF<G?e0YL0s:2FDj`l@4GAG[9GV=v1?9_ILcdAdS>QT12Y5BhhFdX[?nj>MmH9WBD6SNjTR4TU6s^NB:957c0mPkiEKPDBTa]S6")))', '(puts (str (equal a "fTgaSs2nYM1luzkk5AbUm8GB:bXuNzaBPg6gF=4O_ASSH[k<hWxXHqOPLRE=iTtXDCJd0cy6Dftb6<[Iz^0;<vNpJ3@3y87P;ercE6gD?[=`^i;z^^KElg`CTq<9K_1Hp0@9p47t3q[SVQ_15xth")))']
# 2024-09-28 15:37:18,339 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:18] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(set a (add 6252 (multiply (subtract -5547 (divide 5201 -4785)) (add 1466 (max -6727 5553 -3340)))))', '(set b (concat (uppercase (str (subtract a (divide -2449 -1786)))) "hR@`t<Dav[Gdk:02YzO[<5?PZj0tcpU>DnmO:@j4gGprB;7:;fz8m6Mb9Z:zb0Xccv0XPlMt]Fd`WY_t]S1TVWsxWvNGaL>S:bBTZQwn1q9KR9wBRT>kL:`Vj4[kigA^T_nKBPsK:5R3:=LS_eK3`u8?@"))', '(set c (subtract (multiply (add -8715 1423) (max (subtract 2612 -5893) 2897)) (min -3984 -342)))', '(set d (replace b "ms?fE`BxJYhO]I7bB9_rL5Kj5D2g]b[7x=fenRcv8nyS75wF`2Q`v57`p?d7aVE;?S?tMSLECOkb^>" (str c)))', '(puts (str c))', '(puts (lowercase (concat d "xzWILeb4rJMzWZcnqrZQiyk?N2dK@OWrK_M7e61l1e>tzNC52DuUrpCNYRYTM=u5TvqPtT0;^lVdZS^I<mzKdMxUGzub;lXMMb8sdkmgpB[KpIAM>OsXt<kdAy1iJ^Qt>MNwn`")))', '(set e (divide c (multiply (subtract c (divide -8625 9276)) 5190)))', '(puts (str e))']
# 2024-09-28 15:37:18,712 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:18] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (str (not_equal null (abs -1003.7925))))', '(puts (uppercase (concat "HyR2YdYxB[LQJG0]u" (lowercase "AkLEMcW9Vd>"))))']
# 2024-09-28 15:37:19,088 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:19] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (str (equal (puts "Dao]N398>aalYxp<JPPjbUjr4g8u5;^;[6oB`j]8_Fa6UAuajn^x_no8dgFEKzjaO5=5lLr>;=]dsL=rYOfiVZUF[C=QMpqaqWPGaYX^lVq[VrwbhXSq4x2bwykk=gGIvmr>5YgCDgH[go") (puts "so4lOqG7p@hBgt1Ug1KaLk^lYPgrM]0qz8zzX7b:IXie5GKO^f6kPgnGmA8NEqXCMZMnbkdkLj5oCAnSO`ss>e>VKDfBzpJsLfVo`9W<MEdOD:egegiJ03JGAhGR;pIqaCIe9F"))))']      
# 2024-09-28 15:37:19,528 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:19] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(set x (concat (uppercase "harder") (lowercase "TEST")))', '(set y (replace x "ER" "XY"))', '(set z (substring y 0 8))', '(puts (str z))', '(puts (concat z "Wx9ZFt=PeBsur7_Gb:bF9WNqfh4Fz;:p6RpGi^ENnZuemW?P8qMmhiL;qbG6YCd^W29?hen=zgcFz@J9ABhh]zJEu<eB8>:?TXDOiXAfHWFJru[O>i3T]3EaCO0>NVdC8yC0I48b^<TJavk<Ujnl_JpUVOMMS7AF2GFB<uVXUvy782Yt>77:S_]5]unXD]59k6@f"))', '(set errorTest (concat x 6810))']
# 2024-09-28 15:37:19,898 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:19] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (str (divide 1 2)))']
# 2024-09-28 15:37:20,273 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:20] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (concat (str (add (subtract -7377 (abs -9593.1064)) (multiply 5 7 5 -2 0 -5 -10 -9.6066))) (concat " is the result AND :D " ">@ncHBK56`i[CJ5>fpA_m>etB0pN8J2fkMdh_;ydaGVwj81YDGPEo3euSVzu6TBNn3QjMkangzVXFpr[JQaPi]n=8eq=rFJM5peH7ixP=k^4`RhutuG;bn<=3YjQDz5AxCZ2bn?c2lzOaOzp>PBwrVlQ?AX3_KI_EDmM2:Jyk>w^w2RyCusEs0<pChxw7oy<4uZo5NZ?")))', '(puts (str (multiply -9210.6524)))']
# 2024-09-28 15:37:20,658 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:20] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(set a (add -3946 (subtract -7828 (divide 4847 -1752))))', '(set b (concat (uppercase (str a)) "UmD3[W7d]zdrQJtXj9eyXWLleKL>wR2j:^fiZa>>jJXl]2x<0LWAVYjkNH5>cUUTEyg0zySBv12S90GLq9jdhlQy7GHtj>8Lyldiu73KJdClCC0U=cNR9p;H;@o@NT6nov62v1Mf7h0C7R4mWoGJwkaT:l;NS>"))', '(set c (replace b "la4tvd=RsBA2CY62:vJ7y2sIHa8" (str (divide (add (multiply 8973 -8078) (subtract -4269 -2286)) 146))))', '(set d (multiply (subtract (max 1734 -5084) (min 4509 7309)) (abs (subtract -5846 (divide 1044 442)))))', '(puts (str (equal (subtract d (multiply a -709)) -5107)))', '(set e (concat (lowercase (str d)) "C7<hP2zHI]LExIJVzAus;fpaYqC7PMuRtX7pL58LELGtjQYTgp3D<B]OiiJgOk_s:1l9JapiPPPD^YO;wxZ4Nd@SC9gpQD:K50f68LSyTT<fN8xl2XOwbldU;xG6iyg=VhI^CtJc`lK39oiBm1p1aA3^MI3?jF8VEKHEv;Du^AE_`d@[5WCQvq?cOzBJNZr"))', '(puts e)', '(set f (add (str d) (uppercase e)))', '(puts (str f))', '(set g (divide (subtract f a) (add (multiply (subtract -4991 3330) (divide -1586 8022)) 9452)))', '(puts (str g))']
# 2024-09-28 15:37:21,061 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:21] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (substring "abcdef" 0 6))', '(puts (substring "abcdef" 2 10))']
# 2024-09-28 15:37:21,440 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:21] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(set x -1618)', '(set x -6782)']
# 2024-09-28 15:37:21,877 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:21] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (str (add (multiply -6696 (subtract -973 (divide 2053 6098))) (subtract 1467 -3924))))', '(puts (str (subtract (add (multiply -2877 9310) (divide 360 226)) (divide 7589 -1616))))']
# 2024-09-28 15:37:22,304 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:22] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (abs (max -9065 6997.1718)))']
# 2024-09-28 15:37:22,674 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:22] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (str (equal (add -1412 -1412) -2824.0)))', '(puts (str (gt (add -1412 "-1412") -2824.0)))']
# 2024-09-28 15:37:23,043 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:23] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (replace "Hello World" "World" "There"))']
# 2024-09-28 15:37:23,428 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:23] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (str (divide 4070 -8147)))', '(puts (str (divide 2360 -2760.7321)))', '(puts (add 5350 "5350"))', '(puts (subtract -2409 2889))']
# 2024-09-28 15:37:23,825 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:23] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(set a -2914)', '(set b (divide a 3299))', '(set c (subtract b (multiply 7909 2989)))', '(puts (str c))', '(set d (add c (divide 8103 2548)))', '(puts (str d))', '(set e (add d -2552))', '(puts (str e))']
# 2024-09-28 15:37:24,237 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:24] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (substring "43`vHzFuXn0]a`eZEYanU82BWAfAuN[1BiKXbYLUO1KWcEHHXy70EDNQlZ69dsVmP8PtBbd5Z[XApL]mPNH`1XrL69^cv" 30 97))']
# 2024-09-28 15:37:24,652 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:24] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (str (add (subtract 6610 -5535) -733)))', '(puts (str (add -986.5279)))']
# 2024-09-28 15:37:25,259 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:25] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (substring "abcdef" 78 119))']
# 2024-09-28 15:37:25,659 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:25] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (str (divide 650.25 5.0)))']
# 2024-09-28 15:37:26,079 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:26] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(set str1 "k]11K25OStl<zyf=G2jbzAZsElM]u>2z>RzP<erWAfQpal=r9:PKT[nEu3iQ]xFscU]]Q3S>pkMgL`Qh^t`l2AuDsk1rOk7_npeYT0DRah03G;bB<<M^44v=K5Im=kjV80CNT")', '(set part (substring str1 4597 -633))', '(puts (str (equal part "J`]UXsh5l1e;O0cPixlqQ]VQm]n?lE<=zexXFpeK[54hViO0qR?U9hUubaaS3HwP1z_yK3x@h7kutpIM3pRQ1PPR")))', '(set invalidPart (substring str1 3869 -1738))', '(puts (str (equal invalidPart "pX7D<49o52y[KjW_GiUrw;qRp]`TlHlPO_7wxO>2j:2E^VQ[HtCprMo<<VKR@O9A4f>_GGa5h6A7=c^z6s=w]i>J5Rxan4u2Se")))']
# 2024-09-28 15:37:26,488 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:26] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(set x (str (add -2855 -6405)))', '(set y (str (divide -3871 -7136)))', '(set z (str (multiply 1706 -2547)))', '(puts (str (equal x y)))', '(puts (str (equal y z)))', '(puts (str (equal z "dvo1QOa^lf[iqg6:qW6y2>hY>K7jiZ6^BFIeURaxk0@3o@C8oOkUXp0YV[GMHGAPGHqFD=nv?eAWCCDVMJphIRCC6Pvq[tmyLzY9K=N^M3yHAtOsguijR^IC9L]5TRAzVC:0BjSo]m8cex5TwpKVSg@pNYIWLpV")))', '(puts (str (equal z (concat "r@nf<>Fbw;v?tb:Stozn@wlXT8G8^mC1iiQF>KsL5w4=CB`RF?Mb]fr8SO3^IVm9cUlxjOUJPj:BqoLGag0CkvTuUdwi]7W?Fzo=Qz>_2DONJGb7" "EB4o6p0rvj8Ev_t71bHu>AJGWmB7`pOrHEBmvi4J2nr^t^eyLgT`4;GV[u4"))))']
# 2024-09-28 15:37:26,862 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:26] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(set x -9437)', '(puts (str (add x -2710)))', '(puts (str (divide x 0.0)))', '(puts "This line should not be printed")']
# 2024-09-28 15:37:27,238 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:27] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(puts (str (divide 5 0)))', '(puts (str (divide 10 2.0)))', '(puts (str (divide 10 2)))', '(puts (str (divide 5.5 2.0)))']
# 2024-09-28 15:37:27,614 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:27] "POST /lisp-parser HTTP/1.1" 200 -
# "expressions": ['(set x (str (multiply (add -527 (subtract 7572 -1936)) (divide 2861 2877))))', '(puts (replace x (str (divide 7528 -7877)) (str (multiply -3786 -8877))))', '(puts (concat (uppercase x) "r9VeWsIqPk2R?QwpXqwDSffX5m?;ae6`3PW_8^UARD???:vyW1S0NB8zELnI:TL2KAAr=mHkv0Vken0kKp>zTiwrHhKpO31R2_r6;AVcGFoPMZiZMWn090K<Z1F=wUtG<=lTEQ9FqUh4EEo_="))']
# 2024-09-28 15:37:27,987 werkzeug     INFO     127.0.0.1 - - [28/Sep/2024 15:37:27] "POST /lisp-parser HTTP/1.1" 200 -
    
    
    
    
}
ans = []
for index, input in enumerate(data["expressions"]):
    result = inter.interpreter_func(input)
    print(result)
    if result:
        ans.append(result[0].strip("\""))
    else:
        ans.append("ERROR at line " + str(index + 1))
        break
print({"output": ans})
        

@app.route('/lisp-parser', methods=['POST'])
def square():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    ans = []
    for index, input in enumerate(data["expressions"]):
        result = inter.interpreter_func(input)
        print(result)
        if result:
            ans.append(result[0].strip("\""))
        else:
            ans.append("ERROR at line " + str(index + 1))
            break
    # print({"output": ans})
    return jsonify({"output": ans})