import os
from PIL import Image
import get_color
import detect_str
import predict_radius
import predict_font
from yolo import YOLO
import xml.etree.ElementTree as ET

def ysort(elements):
    new_elements = []
    while len(elements) > 0:
        i = 0
        k = 0
        while i < len(elements):
            if elements[i][2] < elements[k][2]:
                k = i
            i += 1
        new_elements.append(elements.pop(k))
    return new_elements


def ydiv(elements, yd, xd):
    len_elements = len(elements)
    layout = []
    div = []
    start = 0
    up= 0
    down = elements[0][4]
    end = 0
    i = 0
    img = Image.open('image/real.jpg')
    w = img.size[0]
    h = img.size[1]
    while i < len_elements - 1:
        if elements[i + 1][2] > down+yd:
            end = i
            if start ==0:
                div.append([0, 0, 0, w, (down+elements[end + 1][2])/2])
                up = down
                down = elements[i+1][4]
            else:
                div.append([0, 0, (elements[start][2]+up)/2, w, (down+elements[end + 1][2])/2])
                up = down
                down = elements[i + 1][4]
            while start <= end:
                div.append(elements[start])
                start += 1
            div = xsort(div)
            div = xdiv(div, xd)
            layout.append(div)
            div = []
        else:
            if elements[i+1][4] > down:
                down = elements[i+1][4]
        i += 1
    div.append([0, 0, (elements[start][2]+up)/2, w, h])
    while start < len_elements:
        div.append(elements[start])
        start += 1
    div = xsort(div)
    div = xdiv(div,xd)
    layout.append(div)
    return layout


def merge(classes, boxes):
    len_classes = len(classes)
    i = 0
    while i < len_classes:
        boxes[i].insert(0, classes[i])
        i = i + 1
    return boxes


def xsort(elements):
    new_elements = []
    new_elements.append(elements.pop(0))
    while len(elements) > 0:
        i = 0
        k = 0
        while i < len(elements):
            if elements[i][1] < elements[k][1]:
                k = i
            i += 1
        new_elements.append(elements.pop(k))
    return new_elements


def xdiv(elements, xd):
    layout = []
    layout.append(elements.pop(0))
    len_elements = len(elements)
    div = []
    start = 0
    end = 0
    i = 0
    while i < len_elements - 1:
        if elements[i + 1][1] > elements[i][3] + xd:
            end = i
            s = start
            left = elements[s][1]
            top = elements[s][2]
            right = elements[s][3]
            down = elements[s][4]
            while s<=end:
                if elements[s][1]<left:
                    left = elements[s][1]
                if elements[s][2] < top:
                    top = elements[s][2]
                if elements[s][3]>right:
                    right = elements[s][3]
                if elements[s][4]>down:
                    down = elements[s][4]
                s+=1
            div.append([0, left, top, right, down])
            while start <= end:
                div.append(elements[start])
                start += 1
            layout.append(div)
            div = []
        i += 1
    s = start
    left = elements[s][1]
    top = elements[s][2]
    right = elements[s][3]
    down = elements[s][4]
    while s < len_elements:
        if elements[s][1] < left:
            left = elements[s][1]
        if elements[s][2] < top:
            top = elements[s][2]
        if elements[s][3] > right:
            right = elements[s][3]
        if elements[s][4] > down:
            down = elements[s][4]
        s+=1
    div.append([0, left, top, right, down])
    while start < len_elements:
        div.append(elements[start])
        start += 1
    layout.append(div)
    return layout


def html(elements):
    fp = open('myhtml.html', 'w')
    fp.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link rel="stylesheet" type="text/css" href="mystyle.css">
</head>
    
<body>
''')
    fp.close()
    fc = open('mystyle.css', 'w')
    fc.write('')
    fc.close()
    len_elements = len(elements)
    x = 1
    i = 0
    while i < len_elements:
        fp = open('myhtml.html', 'a')
        fp.write(f'''    <div id = "div{x}">
''')
        fp.close()
        img = Image.open('image/real.jpg')
        img = img.crop((elements[i][0][1],elements[i][0][2],elements[i][0][3],elements[i][0][4]))
        color = get_color.get_color(img,1)
        fc = open('mystyle.css','a')
        fc.write(f'''#div{x} {{
  position:absolute;
  left:{elements[i][0][1]}px;
  top:{elements[i][0][2]}px;
  width:{elements[i][0][3]-elements[i][0][1]}px;
  height:{elements[i][0][4]-elements[i][0][2]}px;
  background-color:rgb{color};
  }}''')
        fc.close()
        x+=1
        x = html_y(elements[i], x)
        fp = open('myhtml.html', 'a')
        fp.write(f'''    </div>
''')
        fp.close()
        i+=1
    fp = open('myhtml.html', 'a')
    fp.write('''</body>''')
    fp.close()
    return


def html_y(elements, x):
    len_elements = len(elements)
    i = 1
    fp = open('myhtml.html', 'a')
    fp.write(f'''        <div id = "div{x}">
    ''')
    fp.close()
    img = Image.open('image/real.jpg')
    img = img.crop((elements[i][0][1],elements[i][0][2],elements[i][0][3],elements[i][0][4]))
    color = get_color.get_color(img,1)
    fc = open('mystyle.css', 'a')
    fc.write(f'''#div{x}{{
              position:absolute;
              left:{elements[i][0][1]-elements[0][1]}px;
              top:{elements[i][0][2]-elements[0][2]}px;
              width:{elements[i][0][3] - elements[i][0][1]}px;
              height:{elements[i][0][4] - elements[i][0][2]}px;
              background-color:rgb{color};
              }}''')
    fc.close()
    x += 1
    x = html_x(elements[i], x)
    fp = open('myhtml.html', 'a')
    fp.write('''        </div>
    ''')
    fp.close()
    i+=1
    while i < len_elements:
        fp = open('myhtml.html', 'a')
        fp.write(f'''        <div id = "div{x}">
''')
        fp.close()
        img = Image.open('image/real.jpg')
        img = img.crop((elements[i][0][1], elements[i][0][2], elements[i][0][3], elements[i][0][4]))
        color = get_color.get_color(img, 1)
        fc = open('mystyle.css', 'a')
        fc.write(f'''#div{x}{{
          position:absolute;
          left:{elements[i][0][1]-elements[0][1]}px;
          top:{elements[i][0][2]-elements[0][2]}px;
          width:{elements[i][0][3] - elements[i][0][1]}px;
          height:{elements[i][0][4] - elements[i][0][2]}px;
          background-color:rgb{color};
          }}''')
        fc.close()
        x+=1
        x = html_x(elements[i],x)
        fp = open('myhtml.html', 'a')
        fp.write('''        </div>
''')
        fp.close()
        i+=1
    return x


def html_x(elements,x):
    len_elements = len(elements)
    i=1
    while i<len_elements:
        if elements[i][0] == 1:
            img = Image.open('image/real.jpg')
            img = img.crop((elements[i][1], elements[i][2], elements[i][3], elements[i][4]))
            img.save(f'../img/img{x}.png')
            string = detect_str.get_str(f'../img/img{x}')
            font_size = predict_font.predict(f'../img/img{x}.png')
            fp = open('myhtml.html', 'a')
            fp.write(f'''            <a id="a{x}">{string}</a>
''')
            fp.close()
            fc = open('mystyle.css', 'a')
            fc.write(f'''#a{x}{{
                      position:absolute;
                      left:{elements[i][1] - elements[0][1]}px;
                      top:{elements[i][2] - elements[0][2]}px;
                      width:{elements[i][3] - elements[i][1]}px;
                      height:{elements[i][4] - elements[i][2]}px;
                      box-sizing: border-box;
                      font-size:{font_size}px
                      }}''')
            fc.close()
        elif elements[i][0] == 2:
            img = Image.open('image/real.jpg')
            img = img.crop((elements[i][1], elements[i][2], elements[i][3], elements[i][4]))
            color = get_color.get_color(img,2)
            img.save(f'../img/img{x}.png')
            string = detect_str.get_str(f'../img/img{x}')
            radius = predict_radius.predict(f'../img/img{x}.png')
            fp = open('myhtml.html', 'a')
            fp.write(f'''            <select id="select{x}">
                  <option>{string}</option>
            </select>
''')
            fp.close()
            fc = open('mystyle.css', 'a')
            fc.write(f'''#select{x}{{
            position:absolute;
            left:{elements[i][1] - elements[0][1]}px;
            top:{elements[i][2] - elements[0][2]}px;
            width:{elements[i][3] - elements[i][1]}px;
            height:{elements[i][4] - elements[i][2]}px;
            background-color:rgb{color};
            box-sizing: border-box;
            border-radius:{radius}px;
            }}''')
            fc.close()
        elif elements[i][0]==3:
            img = Image.open('image/real.jpg')
            img = img.crop((elements[i][1], elements[i][2], elements[i][3], elements[i][4]))
            color = get_color.get_color(img,2)
            img.save(f'../img/img{x}.png')
            string = detect_str.get_str(f'../img/img{x}')
            radius = predict_radius.predict(f'../img/img{x}.png')
            fp = open('myhtml.html', 'a')
            fp.write(f'''            <input id="input{x}" placeholder="{string}">
''')
            fp.close()
            fc = open('mystyle.css', 'a')
            fc.write(f'''#input{x}{{
position:absolute;
left:{elements[i][1] - elements[0][1]}px;
top:{elements[i][2] - elements[0][2]}px;
width:{elements[i][3] - elements[i][1]}px;
height:{elements[i][4] - elements[i][2]}px;
background-color:rgb{color};
box-sizing: border-box;
border-radius:{radius}px;
}}''')
            fc.close()
        elif elements[i][0] == 4:
            img = Image.open('image/69.png')
            img = img.crop((elements[i][1], elements[i][2], elements[i][3], elements[i][4]))
            color = get_color.get_color(img,2)
            img.save(f'../img/img{x}.png')
            string = detect_str.get_str(f'../img/img{x}')
            font_size = predict_font.predict(f'../img/img{x}.png')
            fp = open('myhtml.html', 'a')
            fp.write(f'''            <textarea id="textarea{x}">{string}</textarea>
''')
            fp.close()

            fc = open('mystyle.css', 'a')
            fc.write(f'''#textarea{x}{{
            position:absolute;
            left:{elements[i][1] - elements[0][1]}px;
            top:{elements[i][2] - elements[0][2]}px;
            width:{elements[i][3] - elements[i][1]}px;
            height:{elements[i][4] - elements[i][2]}px;
            background-color:rgb{color};
            box-sizing: border-box;
            font-size:{font_size}px;
            }}''')
            fc.close()
        elif elements[i][0] == 5:
            img = Image.open('image/real.jpg')
            img = img.crop((elements[i][1],elements[i][2],elements[i][3],elements[i][4]))
            img.save(f'../img/img{x}.png')
            fp = open('myhtml.html', 'a')
            fp.write(f'''            <img id="img{x}" src="../img/img{x}.png">
''')
            fp.close()
            fc = open('mystyle.css', 'a')
            fc.write(f'''#img{x}{{
            position:absolute;
            left:{elements[i][1] - elements[0][1]}px;
            top:{elements[i][2] - elements[0][2]}px;
            width:{elements[i][3] - elements[i][1]}px;
            height:{elements[i][4] - elements[i][2]}px;
            box-sizing: border-box;
            }}''')
            fc.close()
        elif elements[i][0] == 6:
            img = Image.open('image/real.jpg')
            img = img.crop((elements[i][1], elements[i][2], elements[i][3], elements[i][4]))
            img.save(f'../img/img{x}.png')
            string = detect_str.get_str(f'../img/img{x}')
            font_size = predict_font.predict(f'../img/img{x}.png')
            fp = open('myhtml.html', 'a')
            fp.write(f'''            <span id="span{x}">{string}</span>
''')
            fp.close()
            fc = open('mystyle.css', 'a')
            fc.write(f'''#span{x}{{
            position:absolute;
            left:{elements[i][1] - elements[0][1]}px;
            top:{elements[i][2] - elements[0][2]}px;
            width:{elements[i][3] - elements[i][1]}px;
            height:{elements[i][4] - elements[i][2]}px;
            box-sizing: border-box;
            font-size:{font_size}px;
            }}''')
            fc.close()
        elif elements[i][0] == 7:
            img = Image.open('image/real.jpg')
            img = img.crop((elements[i][1], elements[i][2], elements[i][3], elements[i][4]))
            img.save(f'../img/img{x}.png')
            string = detect_str.get_str(f'../img/img{x}')
            font_size = predict_font.predict(f'../img/img{x}.png')
            fp = open('myhtml.html', 'a')
            fp.write(f'''            <p id="p{x}">{string}</p>
''')
            fp.close()
            fc = open('mystyle.css', 'a')
            fc.write(f'''#p{x}{{
            position:absolute;
            left:{elements[i][1] - elements[0][1]}px;
            top:{elements[i][2] - elements[0][2]}px;
            width:{elements[i][3] - elements[i][1]}px;
            height:{elements[i][4] - elements[i][2]}px;
            box-sizing: border-box;
            font-size:{font_size}px;
            }}''')
            fc.close()
        elif elements[i][0] == 8:
            img = Image.open('image/real.jpg')
            img = img.crop((elements[i][1], elements[i][2], elements[i][3], elements[i][4]))
            color = get_color.get_color(img,2)
            img.save(f'../img/img{x}.png')
            string = detect_str.get_str(f'../img/img{x}')
            radius = predict_radius.predict(f'../img/img{x}.png')
            font_size = predict_font.predict(f'../img/img{x}.png')
            fp = open('myhtml.html', 'a')
            fp.write(f'''            <button id="button{x}">{string}</button>
''')
            fp.close()
            fc = open('mystyle.css', 'a')
            fc.write(f'''#button{x}{{
            position:absolute;
            left:{elements[i][1] - elements[0][1]}px;
            top:{elements[i][2] - elements[0][2]}px;
            width:{elements[i][3] - elements[i][1]}px;
            height:{elements[i][4] - elements[i][2]}px;
            box-sizing: border-box;
            background-color:rgb{color};
            border-radius:{radius}px;
            font-size:{font_size}px;
            }}''')
            fc.close()
        elif elements[i][0] == 9:
            fp = open('myhtml.html', 'a')
            fp.write(f'''            <input id="radio{x}" type="radio">
''')
            fp.close()
            fc = open('mystyle.css', 'a')
            fc.write(f'''#radio{x}{{
            position:absolute;
            left:{elements[i][1] - elements[0][1]}px;
            top:{elements[i][2] - elements[0][2]}px;
            width:{elements[i][3] - elements[i][1]}px;
            height:{elements[i][4] - elements[i][2]}px;
            box-sizing: border-box;
            }}''')
            fc.close()
        elif elements[i][0] == 10:
            fp = open('myhtml.html', 'a')
            fp.write(f'''            <input id="checkbox{x}" type="checkbox">
''')
            fp.close()
            fc = open('mystyle.css', 'a')
            fc.write(f'''#checkbox{x}{{
            position:absolute;
            left:{elements[i][1] - elements[0][1]}px;
            top:{elements[i][2] - elements[0][2]}px;
            width:{elements[i][3] - elements[i][1]}px;
            height:{elements[i][4] - elements[i][2]}px;
            box-sizing: border-box;
            }}''')
            fc.close()
        x+=1
        i+=1
    return x


def to_xml(a, b):
    image = Image.open('image/real.jpg')
    fp = open('annotations/real.xml', 'w')
    fp.write(f'''<annotation>
<folder>image</folder>
<filename>real.jpg</filename>
<path>C:\\Users\\chenchen\\Desktop\\generation\\code_generation\\real.jpg</path>
<source>
<database>Unknown</database>
</source>
<size>
<width>{image.size[0]}</width>
<height>{image.size[0]}</height>
<depth>3</depth>
</size>
<segmented>0</segmented>''')
    fp.close()
    len_a = len(a)
    i = 0
    while i < len_a:
        if a[i] == 1:
            name = 'a'
        elif a[i] == 2:
            name = 'select'
        elif a[i] == 3:
            name = 'input'
        elif a[i] == 4:
            name = 'textarea'
        elif a[i] == 5:
            name = 'img'
        elif a[i] == 6:
            name = 'span'
        elif a[i] == 7:
            name = 'p'
        elif a[i] == 8:
            name = 'button'
        elif a[i] == 9:
            name = 'radio'
        elif a[i] == 10:
            name = 'check box'
        b[i][0]=int(b[i][0])
        b[i][1] = int(b[i][1])
        b[i][2] = int(b[i][2])
        b[i][3] = int(b[i][3])
        fp=open('annotations/real.xml', 'a')
        fp.write(f'''
        <object>
<name>{name}</name>
<pose>Unspecified</pose>
<truncated>0</truncated>
<difficult>0</difficult>
<bndbox>
<xmin>{b[i][0]}</xmin>
<ymin>{b[i][1]}</ymin>
<xmax>{b[i][2]}</xmax>
<ymax>{b[i][3]}</ymax>
</bndbox>
</object>''')
        fp.close()
        i+=1
    fp = open('annotations/real.xml', 'a')
    fp.write('''
    </annotation>''')
    fp.close()
    return

def code_generation(yd,xd):
    yolo = YOLO()
    image = Image.open('image/real.jpg')
    a, b = yolo.detect_image(image)
    a = a.tolist()
    b = b.tolist()
    len_b = len(b)
    i = 0
    c = []
    while i < len_b:
        d = []
        d.append(b[i][1])
        d.append(b[i][0])
        d.append(b[i][3])
        d.append(b[i][2])
        c.append(d)
        i += 1
    to_xml(a, c)
    os.system("labelImg ./image ./classes.txt")
    tree = ET.parse('./annotations/real.xml')
    root = tree.getroot()

    labels = []
    boxes = []

    for obj in root.iter('object'):
        label = obj.find('name').text
        if label == 'a':
            label = 1
        elif label == 'select':
            label = 2
        elif label == 'input':
            label = 3
        elif label == 'textarea':
            label = 4
        elif label == 'img':
            label = 5
        elif label == 'span':
            label = 6
        elif label == 'p':
            label = 7
        elif label == 'button':
            label = 8
        elif label == 'radio':
            label = 9
        elif label == 'check box':
            label = 10
        labels.append(label)
        box = []
        xml_box = obj.find('bndbox')
        xmin = (int(xml_box.find('xmin').text))
        ymin = (int(xml_box.find('ymin').text))
        xmax = (int(xml_box.find('xmax').text))
        ymax = (int(xml_box.find('ymax').text))
        box.append(xmin)
        box.append(ymin)
        box.append(xmax)
        box.append(ymax)
        boxes.append(box)

    elements = merge(labels, boxes)
    elements = ysort(elements)
    elements = ydiv(elements, yd, xd)
    html(elements)

code_generation(0, 30)