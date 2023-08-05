from TexSoup import TexSoup

with open("input0.tex") as file:
    code = file.read()

soup = TexSoup(code)

expressions = [node.expr for node in soup.all]
