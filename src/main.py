from dotenv import load_dotenv
from datetime import date
import os
import google.generativeai as genai
import ast

#configure key
load_dotenv()
key=os.getenv("GEMINI_API_KEY")
genai.configure(api_key=key)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

def fetch_system_prompt(user_prompt: str) -> str:
    """Returns system Prompt"""
    system_prompt= f"""
you are an agent. use available tools to either approve or reject product return. Today's date is {date.today()}
1. check if customer is fraudulant
2. check if request is within return window
if both looks good approve.

user_prompt : {user_prompt}

availble tools:
1. check_order_details (order_id: string) -> Returns [product_name, customer_id, purchase_date, product_class]
2. fetch_return_window (product_class: string) -> Returns [return_window: date]
3. customer_details (customer_id: string)-> Returns [customer_trust_score: integer 1 to 10, 10 being very trustworthy]
4. final_decision (decision: string: either 'approve' or 'reject' )

Just choose a tool name from above. you will be provided the result in next request. Reply strictly in below format. 

[{{"tool": tool_name, "params": {{param_name: value}}, "reasoning": explain thought process precisely}}]

previous tool responses:
"""
    return system_prompt

def print_section(title, descr):
    """prints output for readability"""
    print(f"\n____{title}_______________________________________")
    print(descr)

def llm_call(prompt: str)-> str:
    """Does API call to LLM model and waits for response """
    response = model.generate_content(prompt)
    message= response.text.strip().strip('```').strip('json')
    message= ast.literal_eval(message)
    return message
    
def check_order_details(order_id):
    """Tool definition to check order details- Hardcoded for simlifying the code"""
    return {'product_name': 'samsung galaxy a35' , 'customer_id': 112, 'purchase_date': '2025-09-01', 'product_class': 'mobile_phone'}

def fetch_return_window(product_class):
    """Tool definition to check return window- Hardcoded for simlifying the code"""
    return {'return_window': '1 month'}

def customer_details(customer_id):
    """Tool definition to check customer details- Hardcoded for simlifying the code"""
    return {'customer_trust_score': '10'}

def tool_call(llm_resp):
    """This function calls required tools"""
    tool_resp_li=[]
    for item in llm_resp:
        if item['tool']== 'check_order_details':
            res= check_order_details(item['params']['order_id'])
        elif item['tool']=='fetch_return_window':
            res= fetch_return_window(item['params']['product_class'])
        elif item['tool']=='customer_details':
            res= customer_details(item['params']['customer_id'])
        elif item['tool']=='final_decision':
            print_section('DECISION', item['params']['decision'])
            return None
        else: res= None
        
        tool_resp= { 'tool': item['tool'], 'tool_response': res, 'reasoning': item['reasoning']}
        tool_resp_li.append(tool_resp)
    return tool_resp_li

def main(user_prompt):
    system_prompt= fetch_system_prompt(user_prompt)
    tool_resp= None
    i=1
    while True:
        if i>6:
            print_section("FORCE STOPPED", '')
            break
        print_section(f'*EPOCH {i}*',  '')
        print_section('PROMPT', system_prompt)
        llm_resp=llm_call(system_prompt)
        print_section('LLM', llm_resp)
        tool_resp= tool_call(llm_resp)
        if tool_resp:
            print_section('TOOL', tool_resp)
        else:
            print_section("*COMPLETED*", '')
            break
        system_prompt=system_prompt+ "\n"+ str(tool_resp)
        i=i+1
if __name__=="__main__":
    user_prompt= "I want to return this product. order ID 11221"
    main(user_prompt)
