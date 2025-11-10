#!/usr/bin/env python3
"""
Script to convert markdown module content to HTML and update nivel1.html
"""

import re

def markdown_to_html(md_content):
    """Convert markdown to HTML with Tailwind styling matching existing modules"""

    html = '<div class="prose max-w-none">\n'

    lines = md_content.split('\n')
    i = 0
    in_code_block = False
    code_lang = ''
    in_list = False
    in_ordered_list = False
    in_table = False

    while i < len(lines):
        line = lines[i]

        # Skip the main title (# Módulo X.X)
        if i == 0 and line.startswith('# Módulo'):
            i += 1
            continue

        # Code blocks
        if line.strip().startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_lang = line.strip()[3:] or 'cpp'
                html += f'<pre class="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto mb-4"><code class="language-{code_lang}">'
            else:
                html += '</code></pre>\n\n'
                in_code_block = False
            i += 1
            continue

        if in_code_block:
            # Escape HTML in code
            escaped = line.replace('<', '&lt;').replace('>', '&gt;')
            html += escaped + '\n'
            i += 1
            continue

        # H2 headers
        if line.startswith('## '):
            if in_list:
                html += '</ul>\n'
                in_list = False
            if in_ordered_list:
                html += '</ol>\n'
                in_ordered_list = False
            title = line[3:].strip()
            html += f'<h4 class="text-xl font-bold mb-3 mt-5 text-gray-800">{title}</h4>\n\n'
            i += 1
            continue

        # H3 headers
        if line.startswith('### '):
            if in_list:
                html += '</ul>\n'
                in_list = False
            if in_ordered_list:
                html += '</ol>\n'
                in_ordered_list = False
            title = line[4:].strip()
            html += f'<h5 class="text-lg font-bold mb-2 mt-4 text-gray-700">{title}</h5>\n\n'
            i += 1
            continue

        # Horizontal rules
        if line.strip() == '---':
            html += '<p class="mb-4 text-gray-700 leading-relaxed">---</p>\n\n'
            i += 1
            continue

        # Tables (already in HTML format from markdown)
        if '<table' in line:
            in_table = True
            html += '<div class="overflow-x-auto mb-6">'
            html += line + '\n'
            i += 1
            continue

        if in_table:
            html += line + '\n'
            if '</table>' in line:
                html += '</div>'
                in_table = False
            i += 1
            continue

        # Unordered lists
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            if not in_list:
                html += '<ul class="list-disc list-inside space-y-2 mb-4 ml-4">\n'
                in_list = True
            content = line.strip()[2:]
            content = format_inline(content)
            html += f'<li class="mb-2">{content}</li>\n'
            i += 1
            continue
        elif in_list and not line.strip().startswith('-') and line.strip():
            # List continuation
            content = format_inline(line.strip())
            html += f'{content}\n'
            i += 1
            continue
        elif in_list and not line.strip():
            html += '</ul>\n'
            in_list = False
            i += 1
            continue

        # Ordered lists
        if re.match(r'^\d+\.\s', line.strip()):
            if not in_ordered_list:
                html += '<ol class="list-decimal list-inside space-y-2 mb-4 ml-4">\n'
                in_ordered_list = True
            content = re.sub(r'^\d+\.\s', '', line.strip())
            content = format_inline(content)
            html += f'<li class="mb-2">{content}</li>\n'
            i += 1
            continue
        elif in_ordered_list and not re.match(r'^\d+\.', line.strip()) and line.strip():
            # List continuation
            content = format_inline(line.strip())
            html += f'{content}\n'
            i += 1
            continue
        elif in_ordered_list and not line.strip():
            html += '</ol>\n'
            in_ordered_list = False
            i += 1
            continue

        # Regular paragraphs
        if line.strip() and not line.startswith('#'):
            if in_list:
                html += '</ul>\n'
                in_list = False
            if in_ordered_list:
                html += '</ol>\n'
                in_ordered_list = False

            content = format_inline(line.strip())

            # Check if it's a standalone bold line (like section labels)
            if line.strip().startswith('**') and line.strip().endswith('**'):
                html += f'<strong>{content}</strong>\n'
            else:
                html += f'<p class="mb-4 text-gray-700 leading-relaxed">{content}</p>\n\n'

        i += 1

    # Close any open lists
    if in_list:
        html += '</ul>\n'
    if in_ordered_list:
        html += '</ol>\n'

    html += '\n                    </div>'
    return html

def format_inline(text):
    """Format inline markdown elements"""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`(.+?)`', r'<code class="bg-gray-100 px-2 py-1 rounded text-sm">\1</code>', text)
    return text

def process_file(module_num, md_file, html_file):
    """Process a module markdown file and update the HTML"""

    print(f"Processing Module {module_num}...")

    # Read markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert to HTML
    html_content = markdown_to_html(md_content)

    # Read existing HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_full = f.read()

    # Find and replace the module content
    # Pattern: <div class="p-6 hidden" id="module-X"> ... </div>
    pattern = rf'(<div class="p-6 hidden" id="module-{module_num}">)(.*?)(</div>\s*</div>\s*<!--\s*Módulo\s*{module_num + 1}|</div>\s*</div>\s*</div>\s*</div>\s*</section>)'

    def replacer(match):
        return match.group(1) + '\n' + html_content + '\n                    ' + match.group(3)

    html_full = re.sub(pattern, replacer, html_full, flags=re.DOTALL)

    # Write back
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_full)

    print(f"Module {module_num} updated successfully!")

if __name__ == '__main__':
    base_path = r'C:\Users\neima\projetosCC\robo'
    html_file = f'{base_path}\\docs\\nivel1.html'

    modules = [
        (6, f'{base_path}\\curso_robotica_completo\\nivel1\\modulo6_comunicacao_serial.md'),
        (7, f'{base_path}\\curso_robotica_completo\\nivel1\\modulo7_robo_seguidor_linha.md'),
        (8, f'{base_path}\\curso_robotica_completo\\nivel1\\modulo8_robo_desviador_obstaculos.md'),
    ]

    for module_num, md_file in modules:
        try:
            process_file(module_num, md_file, html_file)
        except Exception as e:
            print(f"Error processing module {module_num}: {e}")
            import traceback
            traceback.print_exc()

    print("\nAll modules processed successfully!")
