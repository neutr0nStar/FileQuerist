import time
from flask import Flask, render_template, request, flash, redirect
from genai import GenAI

app = Flask(__name__)

# To store questions and answers
qna = []

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/QnA", methods=['POST'])
def quesAns():
    global qna

    # Check if any file is uploaded
    if len(request.files) == 0:
        return redirect('/')
    
    # Get file contents
    doc_content = str(request.files['document'].read())
    
    # Get QnA
    qna = GenAI().get_qna(doc_content, int(request.form['numQues']))

    while str(qna).startswith("Generate"):
        time.sleep(1)
        # If it didn't work properly
        qna = GenAI().get_qna(doc_content, int(request.form['numQues']))

    return render_template('qna.html', qna=qna)

@app.route("/result", methods=['POST'])
def result():
    global qna

    if qna == []:
        return "Error"
    
    result_response = []

    score = 0
    for i, (q,r) in enumerate(request.form.items()):
        # Score
        if r == qna[i]['answer']:
            score += 1


        # Update result_response
        result_response.append({
            'question': q,
            'response': r,
            'answer': qna[i]['answer']
        })
        
    score /= len(result_response)
    score *= 100

    return render_template('result.html', res=result_response, score=score)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9009, debug=True)