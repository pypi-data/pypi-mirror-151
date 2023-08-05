from TexSoup import TexSoup

with open("case8.tex") as file:
    code = file.read()

soup = TexSoup(code)

expressions = [node.expr for node in soup.all]