import re
import os


def _element(name: str, content: str, indentation: int, inline: bool, **element_attributes) -> str:
    indent_str = ' ' * 4

    attributes = element_attributes.items()
    attributes = [f' {k}="{v}"' if isinstance(v, str)
                  else (f' {k}' if v else '')
                  for k, v in attributes]
    attributes = ''.join(attributes)

    if not inline:
        newline = '\n' + (indent_str * indentation)
        indented_newline = newline + indent_str
        trailing_newline = '\n'
    else:
        newline, indented_newline, trailing_newline = '', '', ''

    if content is not None:
        content = content.splitlines()
        content = indented_newline.join(content)
        return (f'{newline}<{name}{attributes}>{indented_newline}{content}{newline}</{name}>'
                f'{trailing_newline}')
    else:
        return f'{newline}<{name}{attributes}>{trailing_newline}'


class Placeholder:
    _HTML_PATTERN = (r'^<!DOCTYPE html>\s*<html.*>[\s\S]*<head>[\s\S]*<\/head>[\s\S]*'
                     r'<body>\n?(?P<indent>\s*)(?P<body>\S[\s\S]*>)?\s*<\/body>[\s\S]*<\/html>$')
    html_file_pattern = re.compile(_HTML_PATTERN, re.MULTILINE)
    place_holder_pattern = re.compile(r'[A-Z0-9_]+')

    @staticmethod
    def create(placeholder_name: str) -> re.Pattern:
        if not re.match(Placeholder.place_holder_pattern, placeholder_name):
            raise ValueError

        pattern_str = r'( *)(<!-- ' + placeholder_name + r' -->)'

        return re.compile(pattern_str)


class Page:
    def __init__(self, path: str, name: str = None):
        self.name = path.split('/')[-1].split('.')[0] if not name else name

        with open(path, 'r') as index_html_file:
            self._text = index_html_file.read()

        self._write_files = []

    def include_file(self, path: str):
        self._write_files.append(path)
        return self

    def inject_text(self, text: str, pattern: re.Pattern, element=None, **element_attributes):
        if Placeholder.html_file_pattern.match(text):
            html_match = Placeholder.html_file_pattern.search(text)
            indent_length = len(html_match.group('indent'))
            body_text = html_match.group('body')

            if body_text is None:
                text = ''
            else:
                split_body = body_text.split('\n')

                scrubbed_indentation = [line[indent_length:]
                                        for line in split_body[1:]]
                scrubbed_indentation = '\n'.join(scrubbed_indentation)

                text = split_body[0] + '\n' + scrubbed_indentation

        attributes = ''.join([f' {k}={v}'
                              for k, v in element_attributes.items()])

        pattern_match = pattern.search(self._text)

        try:
            indentation = pattern_match.group(1)
        except AttributeError:
            raise ValueError(f'pattern not found: {pattern_match}')

        if element is not None:
            subindentation = indentation + ' ' * 4
            text = text.replace('\n', '\n' + subindentation)
            text = f'{subindentation}{text}\n{indentation}'
            text = f'{indentation}<{element}{attributes}>\n{text}</{element}>'
        else:
            text = text.replace('\n', '\n' + indentation)
            text = f'{indentation}{text}'

        new_html = pattern.sub(text, self._text)
        self._text = new_html

        return self

    def inject(self, path: str, pattern: re.Pattern, element=None, **element_attributes):
        with open(path, 'r') as file:
            file_text = file.read()

        self.inject_text(file_text, pattern, element, **element_attributes)

        return self

    def write(self, output_folder: str):
        try:
            os.makedirs(output_folder)
        except FileExistsError:
            pass

        for in_file in self._write_files:
            file_name = in_file.split('/')[-1]
            out_file = os.path.join(output_folder, file_name)
            with open(in_file, 'rb') as file_in, open(out_file, 'wb') as file_out:
                file_out.write(file_in.read())

        index_path = os.path.join(output_folder, self.name + '.html')
        with open(index_path, 'w') as output:
            output.write(self._text)

    @property
    def text(self):
        return self._text
