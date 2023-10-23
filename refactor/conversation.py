from transformers import pipeline, AutoTokenizer


class UserConversation:
    def __init__(self, model_path, character):
        self.character = character

        self.tokenizer = AutoTokenizer.from_pretrained('gpt2')

        self.generate_pipeline = pipeline( 
        task= "text-generation", 
        model= model_path,
        tokenizer = self.tokenizer, 
        max_new_tokens=100, 
        pad_token_id = 50256,
        #temperature=0.6,
    ) 
        
    def get_full_prompt(self, prompt):
        return f"""
            <Human>: {prompt}
            <{self.character}>:
            """.strip()
    
    def speak(self, prompt):
        full_prompt = self.get_full_prompt(prompt)
        response = self.generate_pipeline(full_prompt, return_full_text=True)
        response = response[0]['generated_text']
        response = response.splitlines()[1].strip()
        response = response[response.index(' '):].strip()
        return response
        response = response[response.index('\n'):].strip()
        response = response[:response.index('\n')]
        response = response[response.index(' '):].strip()
        return response


def test():
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



