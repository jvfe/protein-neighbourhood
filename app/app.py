from flask import Flask, redirect, request, render_template, url_for
import ids_functions

app = Flask(__name__)

@app.route('/', methods = ['POST',  'GET'])
def index():
   return render_template("index.html")

genes = []
@app.route('/query', methods=['GET','POST'])
def getgenes():
    if request.method=='GET':
        gene = request.args.get("gene", None).upper()
        try:
            genes.clear()
            results = ids_functions.sortbyscore(gene)
            genes.extend(list(ids_functions.getgenes(results)))
            #return str(genes)
            return render_template("genes.html", querygene=gene, genes=genes)
        except:
            warning = "Hey! You have to insert a valid protein!"
            return render_template("index.html", warning=warning)


    else:
        g = request.form.get('g')
        query = str(request.url).upper()
        query = query.replace("HTTP://LOCALHOST:5000/QUERY?GENE=", "")
        try:
            pdb = ids_functions.get_pdb(str(g))
            return render_template("genes.html", querygene = query, genes=genes,pdb=pdb)
        except:
            failure = g
            return render_template("genes.html", querygene= query, genes=genes,failure=failure)

if __name__ == '__main__':
    app.run()
