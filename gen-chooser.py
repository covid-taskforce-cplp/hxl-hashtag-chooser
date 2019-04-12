import json

with open("hxl-knowledge-base.json", "r") as input:
    base = json.load(input)

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("'", "&apos;")

def make_tagspec(hashtag, attributes):
    attributes = [attribute for attribute in attributes if attribute]
    return " +".join(["#" + hashtag] + attributes)

def make_html_id(id, hashtag, attributes):
    if hashtag is None:
        return "_" + id
    elif not attributes:
        return hashtag
    else:
        return "_".join([hashtag] + attributes)

def display_question(id, hashtag=None, attributes=[], previous_id=None):
    question = base[id]
    html_id = make_html_id(id, hashtag, attributes)

    # rendering
    print("    <section class=\"question\" id=\"{}\">".format(esc(html_id)))
    print("      <div class=\"nav\">")
    if id == "top":
        print("      <a>HXL hashtag chooser</a>")
    else:
        print("      <a href=\"#_top\">Start over</a>")
    print("      </div>")
    print("      <h2>{}</h2>".format(esc(question["question"].capitalize())))
    if hashtag is not None:
        print("      <p>So far: <span class=\"tagspec\">{}</span></p>".format(esc(make_tagspec(hashtag, attributes))))
    if "pre-text" in question:
        print("        <p class=\"pre-text\">{}</p>".format(esc(question["pre-text"])))
    print("      <ul>")
    for option in question["options"]:
        display_option(option, hashtag, attributes)
    print("      </ul>")
    if "post-text" in question:
        print("        <p class=\"post-text\">{}</p>".format(esc(question["post-text"])))
    print("        <div class=\"nav\">")
    if previous_id is not None:
        print("      <a href=\"#{}\">Previous question</a>".format(esc(previous_id)))
    else:
        print("      <a>Previous question</a>")
    print("          <a href=\"http://hxlstandard.org/standard/dictionary\" target=\"_blank\">HXL dictionary</a>")
    print("        </div>")
    print("    </section>")

    # recursion
    if "options" in question:
        for option in question["options"]:
            opt_hashtag = hashtag
            opt_attributes = list(attributes)
            if "hashtag" in option:
                opt_hashtag = option["hashtag"]
            elif opt_hashtag is not None:
                opt_attributes.append(option.get("attribute", ""))

            if "dest" in option:
                display_question(option["dest"], opt_hashtag, opt_attributes, html_id)
            else:
                display_result(option, opt_hashtag, opt_attributes, html_id)

def display_option(option, hashtag, attributes):
    if "include" in option and hashtag not in option["include"]:
        return
    elif "exclude" in option and hashtag in option["exclude"]:
        return
    
    opt_hashtag = hashtag
    opt_attributes = list(attributes)
    if "hashtag" in option:
        opt_hashtag = option["hashtag"]
    elif opt_hashtag is not None:
        opt_attributes.append(option.get("attribute", ""))
        
    link = make_html_id(option.get("dest"), opt_hashtag, opt_attributes)
    if "dest" not in option:
        link = link + "_000"
    print("        <li><a href=\"#{}\">{}</a></li>".format(
        esc(link),
        esc(option["text"])
    ))

def display_result(option, hashtag, attributes, previous_id):
    print("    <section class=\"result\" id=\"{}_000\">".format(esc(make_html_id(id, hashtag, attributes))))
    print("      <div class=\"nav\"><a href=\"#_top\">Start over</a></div>")
    print("      <h2>Use this hashtag and attributes</h2>")
    print("      <p class=\"tagspec\">{}</p>".format(esc(make_tagspec(hashtag, attributes))))
    if "note" in option:
        print("      <p class=\"note\">{}</p>".format(esc(option["note"])))
    print("      <div class=\"nav\">")
    print("        <a href=\"#{}\">Previous question</a>".format(esc(previous_id)))
    print("        <a href=\"http://hxlstandard.org/standard/dictionary\" target=\"_blank\">HXL dictionary</a>")
    print("      </div>")
    print("    </section>")

print("<!DOCTYPE html>")
print("<html>")
print("  <head>")
print("    <title>HXL hashtag chooser</title>")
print("    <link rel=\"stylesheet\" href=\"style.css\"/>")
print("    <meta charset=\"utf-8\"/>")
print("    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"/>")
print("  </head>")
print("  <body>")
display_question("top")
print("  </body>")
print("  <script src=\"script.js\"></script>")
print("</html>")
