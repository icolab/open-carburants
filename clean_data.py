# XML processing
# http://boscoh.com/programming/reading-xml-serially.html
import xml.etree.ElementTree as etree
for xmlFile in glob.glob("tmp/*.xml"):
    print(xmlFile)
    for event, elem in etree.iterparse(xmlFile, events=('start', 'end', 'start-ns', 'end-ns')):
        if event == 'end' and elem.tag == 'pdv':
            
            # Get the station ID
            id_station = elem.attrib.get('id')
            
            # Get the station postal code qnd update it to cassandra
            cp = elem.attrib.get('cp')
            session.execute("UPDATE carburant_stations SET cp = '"+cp+"' WHERE id_station = "+id_station)
            
            # Get the station pop and update it to cassandra
            pop = elem.attrib.get('pop')
            session.execute("UPDATE carburant_stations SET pop = '"+pop+"' WHERE id_station = "+id_station)
            
            # Get the station adresse and update it to cassandra
            #adresse = elem.attrib.get('adresse')
            #print(str(type(adresse)))
            #session.execute("UPDATE carburant_stations SET adresse = '"+adresse+"' WHERE id_station = "+id_station) 
            # Get the station ville and update it to cassandra
            #ville = elem.attrib.get('ville')
            #session.execute("UPDATE carburant_stations SET ville = '"+ville+"' WHERE id_station = "+id_station) 
            # Get the station ouverture and update it to cassandra
            # Get the station fermeture and update it to cassandra
            # Get the station saufjour and update it to cassandra
            # Get the station services and update it to cassandra
            #prix: nom,id,maj(->timestamp),valeur,
            for child in elem:
                if child.tag == 'prix' and len(child.attrib) > 0:
                    
                    # prix
                    prix = int(child.attrib.get('valeur'))
                    # carburant_id
                    id_carburant = int(child.attrib.get('id'))
                    # timestamp
                    timestamp =  int(time.mktime(time.strptime(child.attrib.get('maj')[0:19], "%Y-%m-%d %H:%M:%S")))
                    
                    #id_station::timestamp::carburant_id, id_station,carburant_id
                    session.execute("INSERT INTO carburant_maj (id,id_station,id_carburant,timestamp,prix) VALUES (%s,%s,%s,%s,%s)",
                        (id_station+"::"+str(timestamp)+"::"+str(id_carburant),int(id_station),id_carburant,timestamp,prix))