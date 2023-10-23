from transformers import pipeline, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('gpt2')

generate = pipeline( 
    task= "text-generation", 
    model= "test_model",
    tokenizer = tokenizer, 
    max_new_tokens=100, 
    #temperature=0.6,
) 

def get_full_prompt(prompt_response_pair):
    if 'response' in prompt_response_pair.keys():
        return f"""
        <Human>: {prompt_response_pair['prompt']}
        <Shrek>: {prompt_response_pair['response']}
        """.strip()
    else:
        return f"""
        <Human>: {prompt_response_pair['prompt']}
        <Shrek>:
        """.strip()


def print_response(response):
    text = response[0]["generated_text"]
    print(text)

print_response(generate(get_full_prompt({'prompt': "Stop this right now!"})))


while True:
    prompt = str(input("You: "))
    prompt = get_full_prompt({"prompt": prompt})
    print_response(generate(prompt))



