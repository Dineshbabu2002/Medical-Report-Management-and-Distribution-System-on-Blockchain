import hashlib
from flask import Flask,render_template,request,session,redirect,url_for
import pandas as pd
from datetime import date
import mysql.connector
import datetime
db=mysql.connector.connect(user='root',port=3306,database='healthcare',charset='utf8')
cur=db.cursor()
app=Flask(__name__)
app.secret_key='@Ha%36Dg@*cds5&^83KDkg^8783TRCkfvuhgvf783478$#&^$*#Q'
global m,n

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/admin_log',methods=['POST','GET'])
def adminlog():
    if request.method=='POST':
        username=request.form['name']
        passcode=request.form['password']
        if username=='Admin' and passcode =='admin':
            return render_template('adminhome.html')
        else:
            msg="Invalid Credentials"
            return render_template('adminlog.html',msg=msg)
    return render_template('adminlog.html')

@app.route('/adddoctor',methods=['POST','GET'])
def adddoctor():
    if request.method=='POST':
        name=request.form['name']
        dept=request.form['department']
        session['department']=dept
        number=request.form['number']
        email=request.form['email']
        address=request.form['address']
        password=request.form['password']
        sql="select * from doc_reg where DoctorName='%s' or DoctorEmail='%s'"%(name,email)
        cur.execute(sql)
        data=cur.fetchall()
        db.commit()
        print(data)
        if data == []:
            sql="insert into doc_reg (DoctorName,Department,DoctorNumber,DoctorEmail,Address,Password)values(%s,%s,%s,%s,%s,%s)"
            val=(name,dept,number,email,address,password)
            cur.execute(sql,val)
            db.commit()
            msg='Doctor Details Added Successfully '
            # sender_address = 'sender@gmail.com'
            # sender_pass = 'password'
            # content="Your requested books on are available please collect From Smart Library Management System"
            # receiver_address = m1
            # message = MIMEMultipart()
            # message['From'] = sender_address
            # message['To'] = receiver_address
            # message['Subject'] = 'Smart library management System for SOET'
            # message.attach(MIMEText(content, 'plain'))
            # ss = smtplib.SMTP('smtp.gmail.com', 587)
            # ss.starttls()
            # ss.login(sender_address, sender_pass)
            # text = message.as_string()
            # ss.sendmail(sender_address, receiver_address, text)
            # ss.quit()
            return render_template('adddoc.html',msg=msg)
        else:
            msg="Details already Exists"
            return render_template('adddoc.html',msg=msg)
    return render_template('adddoc.html')

@app.route('/receptionist',methods=['POST','GET'])
def receptionist():
    if request.method=='POST':
        name = request.form['name']
        number = request.form['number']
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']
        sql="select * from reception where ReceptionistName='%s' or Email ='%s'"%(name,email)
        cur.execute(sql)
        data=cur.fetchall()
        db.commit()
        print(data)
        if data ==[]:
            sql="insert into reception (ReceptionistName,Number,Email,Address,Password)values(%s,%s,%s,%s,%s)"
            val=(name,number,email,address,password)
            cur.execute(sql,val)
            db.commit()
            # sender_address = 'sender@gmail.com'
            # sender_pass = 'password'
            # content="Your requested books on are available please collect From Smart Library Management System"
            # receiver_address = m1
            # message = MIMEMultipart()
            # message['From'] = sender_address
            # message['To'] = receiver_address
            # message['Subject'] = 'Smart library management System for SOET'
            # message.attach(MIMEText(content, 'plain'))
            # ss = smtplib.SMTP('smtp.gmail.com', 587)
            # ss.starttls()
            # ss.login(sender_address, sender_pass)
            # text = message.as_string()
            # ss.sendmail(sender_address, receiver_address, text)
            # ss.quit()
            msg="Details Added Successfully"
            return render_template('reception.html',msg=msg)
        else:
            msg="Details Already Exists"
            return render_template('reception.html',msg=msg)
    return render_template('reception.html')

@app.route('/viewdoctors')
def viewdoctors():
    sql="select Id,DoctorName,DoctorEmail,DoctorNumber,Department,Address from doc_reg"
    data=pd.read_sql_query(sql,db)
    db.commit()
    return render_template('viewdoctors.html',cols=data.columns.values,rows=data.values.tolist())


@app.route('/recep')
def recep():
    sql="select Id,ReceptionistName,Email,Number,Address from reception"
    data=pd.read_sql_query(sql,db)
    db.commit()
    return render_template('receptionist.html',cols=data.columns.values,rows=data.values.tolist())

@app.route('/reception_log',methods=['POST','GET'])
def receptionlog():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        print(name)
        sql="select ReceptionistName,Password from reception where ReceptionistName='%s' and Password='%s'"%(name,password)
        cur.execute(sql)
        data=cur.fetchall()
        db.commit()
        print(data)
        if data==[]:
            msg="Credentials Doesn't Exist"
            return render_template('receptionlog.html',msg=msg)
        else:
            return render_template('receptionhome.html')
    return render_template('receptionlog.html')

@app.route('/addpatients',methods=['POST','GET'])
def addpatients():
    if request.method=='POST':
        x = datetime.datetime.now()
        name=request.form['Name']
        age=request.form['Age']
        contact=request.form['Contact']
        email=request.form['Email']
        address=request.form['Address']
        symptoms=request.form['Symptoms']
        Department=request.form['Department']
        password=request.form['Password']
        print("hello")
        sql="insert into patients (Name,Age,Contact,Email,Address,Symptoms,Department,Password,Date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val=(name,age,contact,email,address,symptoms,Department,password,x)
        cur.execute(sql,val)
        db.commit()
        msg="Details added succesfully"
        return render_template('addpatients.html',msg=msg)

    return render_template('addpatients.html')

@app.route('/view_patients')
def viewpatients():
    sql="select Id,Name,Age,Contact,Email,Address,Symptoms,Department,Date from patients"
    data=pd.read_sql_query(sql,db)
    db.commit()

    return render_template('viewpatients.html',cols=data.columns.values,rows=data.values.tolist())

@app.route('/doctor_login',methods=['POST','GET'])
def doctorlogin():
    if request.method=='POST':
        name=request.form['name']
        session['docname']=name
        passcode=request.form['password']
        session['pass']=passcode
        sql="select * from doc_reg where DoctorName='%s' and Password='%s'"%(name,passcode)
        cur.execute(sql)
        data=cur.fetchall()
        db.commit()
        print(data)
        if data==[]:
            msg="Details are not valid"
            return render_template('doctorlogin.html',msg=msg)
        else:
            return render_template('doctorhome.html')

    return render_template('doctorlogin.html')


@app.route('/all_patients')
def allpatients():
    sql="select * from doc_reg where DoctorName='%s' and Password='%s'"%(session['docname'],session['pass'])
    cur.execute(sql)
    da=cur.fetchall()
    db.commit()
    dept=da[0][2]
    sql="select Id,Name from patients where Department='%s'"%(dept)
    data=pd.read_sql_query(sql,db)
    db.commit()
    if data.empty:
        print('Helooooooooooooo')
        msg="You dont have any appointments"
        return render_template('allpatients.html',msg=msg)

    return render_template('allpatients.html',cols=data.columns.values,rows=data.values.tolist())

@app.route('/add_report/<m>/<n>/',methods=['POST','GET'])
def addreport(m=0,n=''):
    if request.method=='POST':
        filedata=request.files['filedata']
        print(filedata.filename)
        x=filedata.read()
        sql="select * from patients where Id='%s' and Name='%s'"%(m,n)
        cur.execute(sql)
        data=cur.fetchall()
        db.commit()
        symp=data[0][6]
        datalen = int(len(x) / 2)
        print(datalen, len(x))
        g = 0
        a = ''
        b = ''
        c = ''
        for i in range(0, 2):
            if i == 0:
                a = x[g: datalen:1]
                a=a.decode('utf-8')
                print(a)
                result = hashlib.sha1(a.encode())
                hash1 = result.hexdigest()
                print(hash1)
                print("===================================")
                # result = hashlib.sha1(a.encode())
                # hash1 = result.hexdigest()
                # print(hash1)
                print("++++++++++++++++++++++++++")
                # print(g)
                # print(len(data))
                # b = data[g: len(data):1]
                # print(c)

                print(g)
                print(len(x))
                c = x[datalen: len(x):1]
                c = c.decode('utf-8')
                print(c)
                print("===================================")
                print("*****************************")
                result = hashlib.sha1(c.encode())
                hash2 = result.hexdigest()
                print(hash2)
                print(m,n)
                dat=data[0][-1]
                from datetime import date
                today = date.today()
                try:
                    sql = "INSERT INTO reports (slno,Name,Symptoms,FileData,HashA,HashB,StartDate,EndDate) VALUES (%s,%s,%s,AES_ENCRYPT(%s,'keys'),%s,%s,%s,%s)"
                    val=(m,n,symp,x,hash1,hash2,dat,today)
                    cur.execute(sql,val)
                    db.commit()
                    msg="File Uploaded successfully"
                    return render_template('addreport.html',m=m,n=n,msg=msg)
                except:
                    msg="Each File Added only Once for a patient"
                    return render_template('addreport.html',m=m,n=n, msg=msg)

    return render_template('addreport.html',m=m,n=n)


@app.route('/all_reports/<m>/<n>')
def allreports(m=0,n=''):
    print(m,n)
    sql="select Slno,Name,Symptoms from reports where slno='%s' and Name='%s' "%(m,n)
    data=pd.read_sql_query(sql,db)
    db.commit()

    return render_template("allreports.html",m=m,n=n,cols=data.columns.values,rows=data.values.tolist())

@app.route('/allpatientsdetails')
def allpatientsdetails():
    sql="select Id,Name,Age,Contact,Email,Address,Symptoms,Department from patients"
    data=pd.read_sql_query(sql,db)
    db.commit()
    return render_template("allpatientsdetails.html",cols=data.columns.values,rows=data.values.tolist())

@app.route('/view_finalreports/<r>/<r1>/<r2>')
def viewfinalreports(r=0,r1='',r2=''):
    print(r,r1,r2)
    sql="select Id,Name,Symptoms,StartDate,Filedata,EndDate from reports where Slno='%s' or Name='%s' and Symptoms='%s'"%(r,r1,r2)
    cur.execute(sql)
    data=cur.fetchall()
    db.commit()
    print(data)
    id=data[0][0]
    Name=data[0][1]
    sympt=data[0][2]
    sd=data[0][3]
    ed=data[0][-1]
    sql = "select count(*), aes_decrypt(Filedata, 'keys') from reports where Slno='%s' or Name='%s' and Symptoms='%s'"%(r,r1,r2)
    cur.execute(sql)
    data=cur.fetchall()
    db.commit()
    y=data[0][1]
    c=y.decode()
    sql="select Email from patients where (Id='%s' and Symptoms='%s') or Name='%s'"%(r,r2,r1)
    cur.execute(sql)
    email=cur.fetchall()
    db.commit()
    Email=email[0][0]
    print(Email)
    # sender_address = 'sender@gmail.com'
    # sender_pass = 'password'
    # content="Your requested books on are available please collect From Smart Library Management System"
    # receiver_address = Email
    # message = MIMEMultipart()
    # message['From'] = sender_address
    # message['To'] = receiver_address
    # message['Subject'] = 'Smart library management System for SOET'
    # message.attach(MIMEText(content, 'plain'))
    # ss = smtplib.SMTP('smtp.gmail.com', 587)
    # ss.starttls()
    # ss.login(sender_address, sender_pass)
    # text = message.as_string()
    # ss.sendmail(sender_address, receiver_address, text)
    # ss.quit()
    print('123456789')

    return render_template('viewfinalreports.html',message=c,id=id,Name=Name,Symptoms=sympt,sd=sd,ed=ed)


@app.route('/view_all/<int:a>')
def viewall(a=0):
    print('============',a)
    sql="select * from patients where Id=%s"%(a)
    cur.execute(sql)
    data=cur.fetchall()
    db.commit()
    print(data)
    id=data[0][0]
    Name=data[0][1]
    Age=data[0][2]
    contact=data[0][3]
    Email=data[0][4]
    Address=data[0][5]
    Symptoms=data[0][6]
    Dept=data[0][7]
    da=data[0][9]
    return render_template('viewall.html',id=id,name=Name,age=Age,contact=contact,email=Email,address=Address,symptom=Symptoms,Dept=Dept,date=da)


@app.route('/view_patients')
def viewallpatients():
    return render_template('viewallpatients.html')

@app.route('/patient_login',methods=['POST','GET'])
def patientlogin():
    if request.method=='POST':
        name = request.form['username']
        session['patient']=name
        passcode = request.form['password']
        try:
            sql="select * from patients where Name='%s' and Password='%s'"%(name,passcode)
            cur.execute(sql)
            data=cur.fetchall()
            db.commit()
            if data==[]:
                msg="Details Not Valid"
                return render_template('patientlogin.html',msg=msg)
            # sender_address = 'sender@gmail.com'
            # sender_pass = 'password'
            # content="Your requested books on are available please collect From Smart Library Management System"
            # receiver_address = m1
            # message = MIMEMultipart()
            # message['From'] = sender_address
            # message['To'] = receiver_address
            # message['Subject'] = 'Smart library management System for SOET'
            # message.attach(MIMEText(content, 'plain'))
            # ss = smtplib.SMTP('smtp.gmail.com', 587)
            # ss.starttls()
            # ss.login(sender_address, sender_pass)
            # text = message.as_string()
            # ss.sendmail(sender_address, receiver_address, text)
            # ss.quit()
            return render_template('patienthome.html')
        except:
            pass
    return render_template('patientlogin.html')

@app.route('/reports')
def reports():
    print(session['patient'])
    sql="select * from Reports where Name='%s' "%(session['patient'])
    cur.execute(sql)
    data=cur.fetchall()
    db.commit()
    print(data)
    if data == []:
        msg="your reports are not available"
        return render_template('reports.html')


    return render_template('reports.html')

@app.route('/getdata',methods=['POST','GET'])
def getdata():
    if request.method=='POST':
        hasha=request.form['hash1']
        hashb=request.form['hash2']
        print(hasha,hashb)
        sql="select * from reports where HashA='%s' and HashB='%s' and Name='%s'"%(hasha,hashb,session['patient'])
        cur.execute(sql)
        data = cur.fetchall()
        db.commit()
        print(data)
        id = data[0][1]
        Name = data[0][2]
        sympt = data[0][3]
        sd = data[0][7]
        ed = data[0][-1]
        print('-----',data)
        if data==[]:
            msg='invalid Hash Keys'
            return render_template('reports.html',msg=msg)
        sql = "select count(*), aes_decrypt(Filedata, 'keys') from reports where HashA='%s' and HashB='%s' and Name='%s'"%(hasha,hashb,session['patient'])
        cur.execute(sql)
        data = cur.fetchall()
        db.commit()
        message=data[0][1]
        messg=message.decode()
        return render_template('getdata.html',id=id,Name=Name,Symptoms=sympt,sd=sd,ed=ed,messg=messg)
    return render_template('getdata.html')


@app.route('/profile')
def profile():
    sql="select * from patients where Name='%s'"%(session['patient'])
    data=pd.read_sql_query(sql,db)
    db.commit()
    print(data)
    return render_template('profile.html',cols=data.columns.values,rows=data.values.tolist())

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.route('/log_out')
def Logout():
    session.pop('patient',None)
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True)
