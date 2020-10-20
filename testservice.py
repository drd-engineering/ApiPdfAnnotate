import requests

pdfStringFile=""

with open('data.txt', 'r') as file:
    pdfStringFile = file.read().replace('\n', '')

url = 'http://127.0.0.1:8000/makepdf'

myobj = {'pdffile': pdfStringFile,
         "annotations":[
             {"anType":"line","page":1,"x":324.0,"y":100.0,"width":None,"height":None,'text':None,'points':[[106.0, 324.0],[361.5, 330.0]],"identification":None},
             {"anType":"highlighter","page":1,"x":324.0,"y":122.0,"width":None,"height":None,'text':None,'points':[[106.0, 340.0],[361.5, 380.0]],"identification":None},
             {"anType":"text","page":1,"x":200.0,"y":80.0,"width":150.0,"height":100.0,'points':None,'text':'MANTAP BANGET',"identification":None},
             {"anType":"identity","page":1,"x":524.0,"y":12.0,"width":150.0,"height":100.0,'text':None,'points':None,"identification":{"encryptedUserId":"+vpshR4Sr+qGAUCQBd344WvAMppBmj0fbYTvG54VcXc=","imageFileName":"04f4b285-6175-4d29-ad8b-f251c23ace9c.png","name":"Jessica","code":"DRD-200922105910440"}},
             {"anType":"identity","page":1,"x":591.0,"y":192.0,"width":150.0,"height":100.0,'text':None,'points':None,"identification":{"encryptedUserId":"+vpshR4Sr+qGAUCQBd344WvAMppBmj0fbYTvG54VcXc=","imageFileName":"9cf0597f-030e-4e4a-8bcc-806b6a89ad51.png","name":"Jessica","code":"DRD-200922105310440"}},
             {"anType":"identity","page":1,"x":629.0,"y":368.0,"width":150.0,"height":100.0,'text':None,'points':None,"identification":{"encryptedUserId":"+vpshR4Sr+qGAUCQBd344WvAMppBmj0fbYTvG54VcXc=","imageFileName":"4a2e02a8-9daa-4d2e-859a-18925c4a4304.png","name":"Jessica","code":"DRD-200922105110440"}},
            ],
         }

x = requests.post(url, json = myobj)

with open('hasilpdftesting.txt', 'w') as file:
    file.write(x.text)
