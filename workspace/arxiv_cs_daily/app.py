import requests
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

ARXIV_API = "http://export.arxiv.org/api/query"


# 获取某个领域的当天论文
def fetch_daily_papers(category="cs.AI"):
    params = {
        "search_query": f"cat:{category}",
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": 30
    }
    response = requests.get(ARXIV_API, params=params)
    text = response.text

    # ArXiv 返回 Atom XML，这里简单解析（真实项目可用 feedparser）
    import xml.etree.ElementTree as ET
    root = ET.fromstring(text)

    ns = {"atom": "http://www.w3.org/2005/Atom"}

    papers = []
    for entry in root.findall("atom:entry", ns):
        paper = {
            "id": entry.find("atom:id", ns).text,
            "title": entry.find("atom:title", ns).text.strip(),
            "summary": entry.find("atom:summary", ns).text.strip(),
            "published": entry.find("atom:published", ns).text,
            "updated": entry.find("atom:updated", ns).text,
            "authors": [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)],
            "pdf_url": entry.find("atom:link[@type='application/pdf']", ns).attrib["href"],
            "category": category
        }
        papers.append(paper)

    return papers


# 获取单篇论文详情
def fetch_paper(arxiv_id):
    url = f"{ARXIV_API}?id_list={arxiv_id}"
    response = requests.get(url)
    xml = response.text

    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml)
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    entry = root.find("atom:entry", ns)

    info = {
        "id": entry.find("atom:id", ns).text.split("/")[-1],
        "title": entry.find("atom:title", ns).text.strip(),
        "summary": entry.find("atom:summary", ns).text.strip(),
        "published": entry.find("atom:published", ns).text,
        "authors": [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)],
        "pdf_url": entry.find("atom:link[@type='application/pdf']", ns).attrib["href"]
    }

    return info


@app.route("/")
def index():
    categories = ["cs.AI", "cs.CV", "cs.LG", "cs.CL", "cs.TH", "cs.SY"]
    category = request.args.get("cat", "cs.AI")
    papers = fetch_daily_papers(category)
    return render_template("index.html", papers=papers, categories=categories, cur=category)


@app.route("/paper/<arxiv_id>")
def paper_detail(arxiv_id):
    info = fetch_paper(arxiv_id)

    # BibTeX 生成
    bibtex = f"""@article{{{info['id']},
  title={{ {info['title']} }},
  author={{ {' and '.join(info['authors'])} }},
  journal={{arXiv preprint arXiv:{info['id']} }},
  year={{ {info['published'][:4]} }}
}}"""

    citation = f"{', '.join(info['authors'])}. \"{info['title']}\" arXiv:{info['id']} ({info['published'][:4]})."

    return render_template("paper.html", info=info, bibtex=bibtex, citation=citation)


if __name__ == "__main__":
    app.run(debug=True)
