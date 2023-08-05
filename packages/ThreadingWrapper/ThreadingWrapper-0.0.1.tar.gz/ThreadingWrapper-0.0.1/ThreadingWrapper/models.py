class FunctionArgs:
    pointer: any
    arguments: tuple
    keyword_arguments: dict
    output_var: str

    def __init__(self, function: any, output_var="", *args, **kwargs):
        self.pointer = function
        self.arguments = args if args is not None else ()
        self.keyword_arguments = kwargs if kwargs is not None else {}
        self.output_var = output_var
