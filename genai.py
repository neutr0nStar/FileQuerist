import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv() 

class GenAI:
    
    def __init__(self) -> None:
        # Initilize with API key
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

        # Load model
        self.model = genai.GenerativeModel(model_name='gemini-pro')

    def get_qna(self, doc_content: str, n_questions: int = 10) -> list[dict]:
        """
        Generate questions and answers from the doc content.

        Parameters:
        - doc_content: Contents of the document
        - n_questions: number of questions to generate

        Returns list of dictionaries with keys 'question' and 'answer'.
        """

        prompt = """
        Generate %s MCQ questions and answers with 4 options from the document contents only. Give response in JSON format.
        Response example:  [{'question': 'Sun rises in which direction', 'options': ['North', 'East', 'West', 'South'], 'answer': 'East'}, ...]
        Use only English Language. Document content: %s
        """ % (str(n_questions), doc_content)

        response = self.model.generate_content(prompt)


        try:
            if response.text.startswith('```'):
                res_text = response.text[7:-3].replace("\'", "\"")
                response = json.loads(res_text) # 7 & -3 to filter out ```json and ```
            else:
                res_text = response.text.replace("\'", "\"")
                response = json.loads(res_text) # 7 & -3 to filter out ```json and ```
        except Exception as e:
            print(e)
            pass
    
        return response

    

if __name__ == "__main__":
    gai = GenAI()
    with open('./blackholes.txt', 'r') as f:
        res = gai.get_qna(f.read())
    print(res)

