import pyodbc as po
import json
class SQL_Connection:
    "Interfaces with SSMS"
#dbo.addCharacter (charactername,description,userid)
#dbo.addUser (userid,username)
#dbo.defragmentIndexes
#dbo.deleteCharacter (charactername,ownerid)
#dbo.getCharacter (ownerid,charactername)
#dbo.getOwnerID (userid)
#dbo.Load_Data
#dbo.updateCharacter (charactername,description,ownerid)
  
    def __init__(self) -> None:
      """sets up the  connection string"""
      with open('SQLInfo.Json','r') as JsonHold:
        __JS = json.load(JsonHold)
      server = __JS['server']
      database = __JS['database']
      username = __JS['username']
      password = __JS['password']
      driver = __JS['driver']
      self.__connectionString = po.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
      self.__connectionString.setdecoding(po.SQL_CHAR, encoding='latin1')
      pass

  
    def getCharacter(self,user_id,character_name):
      """Retrieves a character's page provided their owner's Discord ID and character name\n
      user_iD : (int)\n
      character_name: (string)\n
      out : (string)
      """
      cursor = self.__getCursor()
      cursor.execute(f"execute getOwnerID @UserID = ?", user_id)
      pkIDForUser = cursor.fetchone()[0]
      cursor.execute(f"execute getCharacter @ownerid = ?, @charactername = ?", pkIDForUser,character_name)
      return cursor.fetchone()[0]

  
    def deleteCharacter(self,user_id,character_name):
      """Used To Delete Characters\n
        user_id : (int)\n
        character_name : (string)\n
          out : void"""
      cursor = self.__getCursor()
      cursor.execute(f"execute deleteCharacter @ownerid =?, @charactername =?", user_id,character_name)
      pass

  
    def updateCharacter(self,user_id,character_name,description):
      """Used to update a character\nuser_id : (int)\n
      character_name : (string)\n
      description : (string)\n
      out : void"""
      cursor = self.__getCursor()
      cursor.execute(f"execute updateCharacter @ownerid =?, @charactername =?, @description =?", user_id,character_name,description)
      pass

  
    def createCharacter(self,user_id,character_name,description):
      """Used to create a character\n
      user_id : (int)\n
      character_name : (string)\n
      description : (string) \n
      out : void"""
      cursor = self.__getCursor()
      cursor.execute(f"execute addCharacter @ownerid =?, @charactername =?, @description =?", user_id,character_name,description)
      pass

  
    def checkIfOne(self,character_name):
      """Used to check if it's the only character in the database\n
      character_name : (string) \n
      out : boolean"""
      cursor = self.__getCursor()
      cursor.execute(f"select count(*) from character where charactername = ?", character_name)
      return cursor.fetchone()[0] == 1
      pass

  
    def getUserName(self,userID):
      """Used to get a username with a userID\n
      userID: (int)\n
      out : string"""
      cursor = self.__getCursor()
      cursor.execute(f"select username from [user] where userID = ?", userID)
      return cursor.fetchone()[0]
      pass
    
    def getID(self,userID):
      """Used to get a username with a userID\n
      userID: (int)\n
      out : int"""
      cursor = self.__getCursor()
      cursor.execute(f"select id from [user] where userID = ?", userID)
      return cursor.fetchone()[0]
      pass

    def getMultiList(self,charaName):
      """Used To Deal with multiple characters with the same name, returns i[listname{number}][characterid]"""
      cursor = self.__getCursor()
      cursor.execute(f"execute getMultiList @name =?", charaName)
      return cursor.fetchall()

    def getIDChar(self,charaID):
      """Used To Deal with multiple characters with the same ID, returns character Information matching the id"""
      cursor = self.__getCursor()
      cursor.execute(f"select description from character where id = ?",charaID)
      return cursor.fetchone()[0]

    def getList(self,wildCard):
      """Gets Simular Names"""
      cursor = self.__getCursor()
      cursor.execute("Execute getSimularList @wc=?",wildCard)
      holdAllName = ''
      cnt = 0
      for i in cursor.fetchall():
        holdAllName = holdAllName + i[0] + '\n'
        cnt+=1
      if cnt > 50:
        return 'Be more specific'
      return holdAllName
    def __getCursor(self):
       """Returns a cursor to the SQL Server"""
       return self.__connectionString.cursor()
    def CheckIfPersonExists(self,id):
      """Returns True if person exists"""
      cursor = self.__getCursor()
      cursor.execute("Select userid from [user] where userid = ?",id)
      return cursor.fetchone()!= None
    def UpdateUsername(self,id,userName):
      """checks if userName is up to date, Updates the username if it isn't"""
      cursor = self.__getCursor()
      cursor.execute("Select username from [user] where userid =?",id)
      if cursor.fetchone()[0]!= userName:
        cursor.execute("Update [user] set username =? where userid =?",userName,id)
        return 
      return 
    def CreatePerson(self,id,userName):
      """Creates a new person in the database"""
      cursor = self.__getCursor()
      cursor.execute("Insert into [user] (userid,username) values (?,?)",id,userName)
i = SQL_Connection()
