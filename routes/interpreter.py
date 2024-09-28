import json
import logging


from collections import deque

from flask import request, jsonify

from routes import app

logger = logging.getLogger(__name__)


class interpreter:

    def __inti__(self):
        self.arguments = {}

    def puts(self, *message):
        if not (len(message) == 1):
            return False
        print(message[0])
        return message[0]

    def assignment(self, *argname):
        if(not (len(argname)==2)):
            return False
        if argname[0] in self.arguments:
            return False
        self.arguments[argname[0]] = argname[1] #may need change here
        return True
    
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
            if (arg[i].isnumeric() or arg[i].isdigit() or (arg[i][0]=='-' and (arg[i][1:].isdigit() or arg[i][1:].isnumeric()))):
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
            if (arg[i].isnumeric() or arg[i].isdigit() or (arg[i][0]=='-' and (arg[i][1:].isdigit() or arg[i][1:].isnumeric()))):
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
            if (arg[i].isnumeric() or arg[i].isdigit() or (arg[i][0]=='-' and (arg[i][1:].isdigit() or arg[i][1:].isnumeric()))):
                ls.append(arg[i])
            else:
                return False
        
        ans = 1
        flag = True
        for i in ls:
            if (i.isdigit()):
                ans *= float(i)
                flag = False
            else:
                ans *= int(i)
        if flag:
            str(int(ans))
        return f"{ans:.4g}" 

    def division(self, *arg):
        if(not(len(arg)==2)):
            return False
        
        ls = []

        for i in range(len(arg)):
            if (arg[i].isnumeric() or arg[i].isdigit() or (arg[i][0]=='-' and (arg[i][1:].isdigit() or arg[i][1:].isnumeric()))):
                ls.append(arg[i])
            else:
                return False
        if (ls[0].isdigit() and ls[1].isdigit()):
            return str(int(ls[0])/int(ls[1]))
        return f"{float(ls[0])/float(ls[1]):.4g}"


    def abosulte(self, *arg):
        if(not len(arg)==1):
            return False

        ls = []

        for i in range(len(arg)):
            if (arg[i].isnumeric() or arg[i].isdigit() or (arg[i][0]=='-' and (arg[i][1:].isdigit() or arg[i][1:].isnumeric()))):
                ls.append(arg[i])
            else:
                return False

        return str(abs(float(ls[0])))


    def getMax(self, *arg):
        ls = []

        if(len(arg)<2):
            return False

        for i in range(len(arg)):
            if (arg[i].isnumeric() or arg[i].isdigit() or (arg[i][0]=='-' and (arg[i][1:].isdigit() or arg[i][1:].isnumeric()))):
                ls.append(float(arg[i]))
            else:
                return False

        
        return str(max(ls))

    def getMin(self, *arg):
        ls = []

        if(len(arg)<2):
            return False

        for i in range(len(arg)):
            if (arg[i].isnumeric() or arg[i].isdigit() or (arg[i][0]=='-' and (arg[i][1:].isdigit() or arg[i][1:].isnumeric()))):
                ls.append(float(arg[i]))
            else:
                return False

        
        return str(min(ls))

    def greaterthan(self, *arg):
        if not(len(arg)==2):
            return False

        ls = []
        for i in range(len(arg)):
            if (arg[i].isnumeric() or arg[i].isdigit() or (arg[i][0]=='-' and (arg[i][1:].isdigit() or arg[i][1:].isnumeric()))):
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
            if (arg[i].isnumeric() or arg[i].isdigit() or (arg[i][0]=='-' and (arg[i][1:].isdigit() or arg[i][1:].isnumeric()))):
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
        
        return '"' + arg[0] + '"'

    
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
        print(list)
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
        elif fun == "str":
            return self.tostr(*list[1:])
        elif fun == "equal":
            print(len(list[1:]))
            return self.equal(*list[1:])

                



        

inter = interpreter()

data = {
  "expressions": [
    "(puts \"Hello\")",
    "(puts \"World!\")"
  ]
}
ans = []
for input in data["expressions"]:
    ans.append(inter.interpreter_func(input)[0].strip("\""))
print({"output": ans})
        

@app.route('/lisp-parser', methods=['POST'])
def interpreter():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    ans = []
    for input in data["expressions"]:
        ans.append(inter.interpreter_func(input)[0].strip("\""))
    print("trash")
    json_response = json.dumps({"output": ans})
    return json_response, 200, {'Content-Type': 'application/json; charset=utf-8'}
