
from formattex.intermediate_repr import create_internal_repr_texfile

path_in = "input0.tex"

repr = create_internal_repr_texfile(path_in)
code_out = repr.dump()

if code_out != repr.full_code:
    with open("tmp_input.tex", "w") as file:
        file.write(repr.full_code)

    with open("tmp_dumped.tex", "w") as file:
        file.write(code_out)

    raise RuntimeError
