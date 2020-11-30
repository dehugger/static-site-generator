import re, sys, os, uuid

input_folder = sys.argv[1]
output_folder = sys.argv[2]

class RegularExpressions:
    flags = re.I|re.M|re.U
    components = r'(\{[^}]*\})'
    block = r'(\[[^\]]*\])'
    html = r'(\<[^>]*\>)'
    lists = r'(\_[^_]*\_)'

def ss_parser(raw):
    formatted = raw
    lists = re.findall(RegularExpressions.lists, raw, flags=RegularExpressions.flags)
    blocks = re.findall(RegularExpressions.block, raw, flags=RegularExpressions.flags)
    components = re.findall(RegularExpressions.components, raw, flags=RegularExpressions.flags)
    # print(lists)
    # print(blocks)
    # print(components)
    for i in lists:
        formatted = formatted.replace(i, list_parser(i))
    for i in blocks:
        formatted = formatted.replace(i, block_parser(i))
    for i in components:
        formatted = formatted.replace(i, component_parser(i))
    return formatted

def block_parser(block):
    uid = str(uuid.uuid4())
    output = ''
    block = block.replace('[','')
    block = block.replace(']','')
    text, control = block.split('|',1)
    if '^' in control:
        control, class_name = control.split('^')
    else:
        class_name = ''
    
    if '!' in control:
        control, path = control.split('!')

    if control == 'link':
        if '"' in path:
            link = path.replace('"','')
        else:
            link = '/' + path.replace('.ss', '.html')
        output = '<a id="{uid}" href="{link}" class="{class_name}">{text}</a>'.format(uid=uid, link=link, class_name=class_name, text=text)

    elif control == 'img':
        if '"' in path:
            link = path.replace('"','')
        else:
            link = '/images/' + path
        output = '<img id="{uid}" src="{link}" class="{class_name}">{text}</a>'.format(uid=uid, link=link, class_name=class_name, text=text)

    elif control == 'span':
        output = '<span id="{uid}" class="{class_name}">{text}</span>'.format(uid=uid, class_name=class_name, text=text)

    elif control in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        output = '<{control} id="{uid}" class="{class_name}">{text}</{control}>'.format(control=control, uid=uid, class_name=class_name, text=text)

    else:
        output == '<{control} id="{uid}" class="{class_name}">{text}</{control}>'.format(control=control, uid=uid, class_name=class_name, text=text)        

    return output

def component_parser(component):
    component = component.replace('{','')
    component = component.replace('}','')
    with open('components/' + component, 'r') as f:
        return ss_parser(f.read())

def list_parser(l):
    l = l.replace('_','')
    l = l.replace('_','')
    items = l.split(',')
    output = '<ul id="{uid}">\n'.format(uid = str(uuid.uuid4()))
    for i in items:
        output += '<li id="{uid}">{text}</li>\n'.format(uid = str(uuid.uuid4()), text=i)
    output += '</ul>\n'
    return output

def file_parser(filename):
    with open(filename, 'r') as f:
        if '/' in filename:
            title = filename.split('/')[-1]
        if '.' in title:
            title = title.split('.')[0]
        raw = f.read()
    formatted = ss_parser(raw)
    html = '''<html>
<head>
<title>{title}</title>
<link rel="stylesheet" href="css/style.css">
<meta charset="UTF-8">
</head>
<body>
{content}
<body>
</html>
'''.format(title=title, content=formatted)
    return html

def print_dir_tree(path):
    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            print(os.path.join(root, name))
        for name in dirs:
            print(os.path.join(root, name))

print('Input\n')
print_dir_tree(input_folder)
print('\n-----\n')

for root, dirs, files in os.walk(input_folder, topdown=True):
    for name in dirs:
        new_dir = str(os.path.join(root,name)).replace(input_folder, output_folder)
        os.mkdir(new_dir)
    for name in files:
        if name.split('.')[-1] in ['jpg', 'jpeg', 'png', 'gif']: #add image extensions as needed
            new_file = output_folder + '/images/' + name
            with open(os.path.join(root,name), 'rb') as fr:
                with open(new_file, 'wb') as fw:
                    fw.write(fr.read())
        else:
            new_file = str(os.path.join(root,name)).replace(input_folder, output_folder)
            new_file = new_file.replace('.ss', '.html')
            with open(new_file, 'w') as f:
                html = file_parser(os.path.join(root,name))
                f.write(html)

print('Output\n')
print_dir_tree(output_folder)