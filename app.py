from flask import Flask, request, render_template
from stories import Story, story

app = Flask(__name__)

@app.route('/')
def home_page():
    """ set up prompts for story injection, use item(n)-partofspeech for names so make unique names"""
    skel = ["place", "adjective", "verb", "noun", "plural_noun"]
    acc = ''
    count = 1
    for item in skel:
        li = f"""<li>{item}:&nbsp;&nbsp;<input type="textarea" name="item{count}-{item}" /></li>"""
        acc += li
        count += 1
    ret = render_template("home.html", lis=acc)
    return(ret)

def extract_prompt(arg):
    """ labels are of form item(n)-partofspeech (ex. "item4-noun"), 
        this function removes the item(n) part to leave just the part-of-speech
        and pairs with the value again
    """
    (item, val) = arg
    prompt = "-".join(item.split("-")[1:])    # pop off item(n) from string
    return (prompt, val)

@app.route('/story')
def finished_story():
    """ remove item(n) from keys & feed GET data in dictionary form directly to generate """
    prompts = dict([ extract_prompt(arg) for arg in request.args.items() ])
    ret = story.generate(prompts)
    return(ret)
 

