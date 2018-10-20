import json
import requests
import Tkinter
import tkMessageBox
def write_to_html(selected):
    for select in selected:
        for key, value in select.iteritems():
            if not isinstance(value, (int, long)):
                value = value.encode('utf-8')
                value = value.replace("'", "")
    
    html_str = list_to_html_table(selected)
    with open("./a.html", "w") as f:
       f.write(html_str.encode("UTF-8"))
   
def html_table(result):
  yield '<style>'
  yield '    table {' 
  yield '    border-collapse: collapse;' 
  yield '    text-align: left;' 
  yield '    width: 100%;'
  yield '    font: normal 12px/150% Arial, Helvetica, sans-serif;' 
  yield '    width: 700px;'
  yield '    background: #fff;'
  yield '    overflow: hidden;	'
  yield '    border: 1px solid #006699;'
  yield '    -webkit-border-radius: 3px;'
  yield '    -moz-border-radius: 3px;'
  yield '    border-radius: 3px;'
  yield '    }'
  yield '    table td, table th {'	
  yield '    padding: 3px 10px;'
  yield '    }'
  yield '    table thead th {'
  yield '    background:-webkit-gradient( linear, left top, left bottom, color-stop(0.05, #006699), color-stop(1, #00557F) );'	
  yield '    background:-moz-linear-gradient( center top, #006699 5%, #00557F 100% );'
  yield '    filter:progid:DXImageTransform.Microsoft.gradient(startColorstr="#006699", endColorstr="#00557F");'
  yield '    background-color:#006699;'
  yield '    color:#FFFFFF; '
  yield '    font-size: 15px; '
  yield '    font-weight: bold; '
  yield '    border-left: 1px solid #0070A8; '
  yield '    } '
  yield '    table tbody td {' 	
  yield '    color: #00496B; 	'
  yield '    border-left: 1px solid #E1EEF4;'	
  yield '    font-size: 12px;	'
  yield '    font-weight: normal;' 
  yield '    }'
  yield '    table tbody td:first-child {'	
  yield '    border-left: none;' 
  yield '    }'
  yield '    table tbody tr:last-child td {' 	
  yield '    border-bottom: none;' 
  yield '    }'
  yield '    </style>'
  yield '<table>'
  yield '''<thead>
					<tr>
                    <th>id</th>
                    <th>adId</th>
                    <th>userId</th>
                    <th>eventType</th>
                    <th>Category</th>
                    <th>eventType</th>

                    
					</tr>
				</thead>'''
  for sublist in result:
    yield '  <tr>'
    yield '    <td>'
    yield str(sublist["id"])
    yield '  </td>'
    yield '    <td>'
    yield str(sublist["adId"])
    yield '  </td>'
    yield '    <td>'
    yield str(sublist["userId"])
    yield '  </td>'
    yield '    <td>'
    yield sublist["eventType"]
    yield '  </td>'
    yield '    <td>'
    yield str(sublist["category"])
    yield '  </td>'
    yield '    <td>'
    yield str(sublist["eventDate"])
    yield '  </td></tr>'
  yield '</table>'
  
def list_to_html_table(result):
    return ''.join(html_table(result))

def request_data():
    response = requests.get("https://devakademi.sahibinden.com/api/stats/findAllWithPagination?pageSize=5000&currentPage=0")
    
    response = json.loads(response.text)
    
    
    selected = []
    adId = []
         
    for res in response:
        for key, value in res.iteritems():
            if key == "eventType" and value == "CLICK":
                selected.append(res)
                adId.append(res['adId'])
        
    selected.sort()
    selected_table(selected)
    write_to_html(selected)

def selected_table(selected):
    r=0
    c=0
    top =Tkinter.Tk()
    top.geometry("600x300")
    for select in selected:
        for key, value in select.iteritems():
            if r == 0:
                Tkinter.Label(top, text=key, borderwidth=3 ).grid(row=r,column=c)
            else:
                Tkinter.Label(top, text=value, borderwidth=1 ).grid(row=r,column=c)
            c+=1
            if not isinstance(value, (int, long)):
                value = value.encode('utf-8')
                value = value.replace("'", "")
        r+=1
        c=0
    Tkinter.Button(top, text="Print to HTML", borderwidth=1, command=write_to_html(selected)).grid(row=r,column=c+1)
    top.mainloop()
    
def find_user():
    a=gender.get("1.0","end-1c")
    age=bdate.get("1.0","end-1c")
    found = []
    if a == "e" or a == "E":
        response = requests.get("https://devakademi.sahibinden.com/api/users/findAllByGender?gender=E")
        response = json.loads(response.text)
        for res in response:
            for key, value in res.iteritems():
                if key == "age" and (value <=int(age)+5 or value > int(age)-5):
                    found.append(res)
        selected_table(found)
    elif a == "k" or a == "K":
        response = requests.get("https://devakademi.sahibinden.com/api/users/findAllByGender?gender=K")
        response = json.loads(response.text)
        for res in response:
            for key, value in res.iteritems():
                if key == "age" and (value <=int(age)+5 or value > int(age)-5):
                    found.append(res)
        selected_table(found)            
    else:
        tkMessageBox.showinfo("Uyarı", "E veya K yazın!")
        

if __name__ == '__main__':
    main_window = Tkinter.Tk()
    main_window.geometry("800x600")
    table = Tkinter.Button(main_window, text="Get Table", command=request_data).pack()
    gender = Tkinter.Text(main_window, width=1, height=1)
    gender.pack()
    bdate = Tkinter.Text(main_window, width=4, height=1)
    bdate.pack()
    similar = Tkinter.Button(main_window, text="Show Similar Users", command=find_user).pack()
    

    
    main_window.mainloop()