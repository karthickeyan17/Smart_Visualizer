from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import io
import base64
import matplotlib.pyplot as plt
import google.generativeai as genai

app = FastAPI()

# Configure the Google Generative AI
genai.configure(api_key="AIzaSyDANMtt9fXmVf3Q85eQk0fxsDsbFhZk5TU")

# Set up templates and static files directory
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Store the uploaded data globally (not recommended for production)
df = None

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/uploadcsv/")
async def upload_csv(file: UploadFile = File(...)):
    global df
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    if df is None:
        return RedirectResponse(url="/", status_code=303)
    return RedirectResponse(url="/summary", status_code=303)

@app.get("/summary", response_class=HTMLResponse)
async def display_summary(request: Request):
    global df
    if df is None:
        return RedirectResponse(url="/", status_code=303)
    summary = df.describe(include='all').to_html(classes="table table-striped")
    return templates.TemplateResponse("summary.html", {"request": request, "summary": summary})


@app.post("/generate_code/", response_class=HTMLResponse)
async def generate_code(request: Request, prompt: str = Form(...)):
    global df
    if df is None:
        return RedirectResponse(url="/", status_code=303)
    csv_text = df.to_csv(index=False)
    model = genai.GenerativeModel('gemini-1.5-flash')
    imp = "important only code for the plot with comments no explanation because the response of this prompt is given to exec()"
    query = f"Here is some data from a CSV file:\n\n{csv_text}\n\n{prompt} in plot . {imp} .The  CSV file is in dataframe with variable df, don't read csv just use it."
    response = model.generate_content(query)
    code = response.text.strip().replace("plt.show()","")
    # Execute the generated code
    local_vars = {'df': df}
    try:
        exec(code[code.index('\n')+1:-3], {}, local_vars)
    except Exception as e:
        return templates.TemplateResponse("summary.html", {"request": request, "summary": df.describe(include='all').to_html(classes="table table-striped"), "error": str(e), "code": code})
    
    # Generate the plot image in-memory
    plot_data = None
    if 'plt' in local_vars:
        buf = io.BytesIO()
        local_vars['plt'].savefig(buf, format='png')
        buf.seek(0)
        plot_data = base64.b64encode(buf.read()).decode('utf-8')
        local_vars['plt'].close()
    
    return templates.TemplateResponse(
        "summary.html", 
        {
            "request": request, 
            "summary": df.describe(include='all').to_html(classes="table table-striped"), 
            "plot_data": plot_data,
            "prompt": prompt, 
            "code": code
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
