Example Use:
python ss_gen.py input_folder output_folder
python ss_gen.py /home/lauren/Desktop/Projects/static_site_gen/test_input /home/lauren/Desktop/Projects/static_site_gen/output

Input Folder Structure:

root
├── components
│   ├── footer.ss
│   └── header.ss
├── content_1
│   ├── content_1.ss
│   └── sub_content_1
│       └── content_1.ss
├── content_2
│   └── content_2.ss
├── images
│   └── img_1.jpg
└── index.ss

Output Folder Structure:

html
├── css
│   └── style.css
├── components
│   ├── footer.html
│   └── header.html
├── content_1
│   ├── content_1.html
│   └── sub_content_1
│       └── content_1.html
├── content_2
│   └── content_2.html
├── images
│   └── img_1.jpg
└── index.html

SS File Syntax:

Link - [Link Text|link!path/to/file/file.ss]
Link External - [Link Text|link!"www.example.com"]
Component - {component_name.ss} #sourced from 'components' folder
Image - [Mouseover text|img!img_file.jpg] #jpg, png, whatever
Header - [Text|h1] #h1,2,3,4,5,6
Span - [Text|span]
Direct HTML Element <br> <hr>
Class Name - [Example|h1^menu] #class name should always come last
List - _Item1, Item2, Item3_

Example SS File:

---
{header.ss}
[Test Page|h1^page-title]
<hr>
[Google|link!"www.google.com"]
Look at this picture of cute cats!
They are so cute!
[Cute Kittens|img!kittens.jpg]
[Kitten Names:|span^list-title]
_Tiger,Spot,Rex - [Pictures of Rex|link!"www.rexsblog.com"]_
{footer.ss}
---

Output:
---
<html>
<head>
<title>index</title>
<link rel="stylesheet" href="css/style.css">
<meta charset="UTF-8">
</head>
<body>
<h1 id="7ce3c30f-5566-45af-b502-e9d6d1169dce" class="page-title">Test Page</h1>
<hr>
<a id="d1b6ca1d-249e-4e6b-ba6d-6b620bc0cd06" href="www.google.com" class="">Google</a>
Look at this picture of cute cats!
They are so cute!
<img id="26f6ead3-442a-4f5b-b19a-def7180ff7c6" src="/images/kittens.jpg" class="">Cute Kittens</a>
<span id="6ea707f3-a2ff-48b1-8df4-59f848c70680" class="list-title">Kitten Names:</span>
<ul>
    <li>Tiger</li>
    <li>Spot</li>
    <li>Rex - <a id="f5649b30-e13e-4994-9c91-d30c3908ea6c" href="www.rexsblog.com" class="">Pictures of Rex</a></li>
</ul>
<body>
</html>
---

Notes:
For generated elements a uuid id is added to allow that specific element to be targetted by CSS