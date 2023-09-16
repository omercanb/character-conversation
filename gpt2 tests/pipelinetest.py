from transformers import pipeline, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('gpt2')

generate = pipeline( 
    task= "text-generation", 
    model= "test_model",
    tokenizer = tokenizer, 
    max_new_tokens=100, 
    temperature=0.7,
) 

def get_full_prompt(prompt_response_pair):
    if 'response' in prompt_response_pair.keys():
        return f"""
        <Human>: {prompt_response_pair['prompt']}
        <Joker>: {prompt_response_pair['response']}
        """.strip()
    else:
        return f"""
        <Human>: {prompt_response_pair['prompt']}
        <Joker>:
        """.strip()

print(generate(get_full_prompt({'prompt': "Stop this right now!"})))



while True:
    prompt = str(input("You: "))
    prompt = get_full_prompt({"prompt": prompt})
    print(generate(prompt))

