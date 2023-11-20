import SQLInterface
class ServerWork:
  """All The work that is happening between the two shell classes"""
  def __init__(self):
    self.__output = ['']
    self.SI = SQLInterface.SQL_Connection()

# IO
  def getOutput(self):
    """
    Return The text Limit of queued output for the server.
    """
    if len(self.__output) > 0:
        TEXTLIMIT:int = 2000
        outText = self.__output.pop(0)
        if outText is None: 
            outText = ''
        return outText
    return ''

  def addChar(self, message, parameters):
    """
    Adds a character to the database if it doesn't already exist attached to the user, also {},@ not aloud
    """
    name = parameters[0]
    description = parameters[1]
    userID = self.__getCLID(message)
    if name == '' or description == '':
      self.__AddToOutput('You must include a name and a description for your character.')
      return
    if '{' in name or '@' in name or '}' in name:
      self.__AddToOutput('You cannot use {} or @ in your character name.')
      return
    if self.SI.getChar(name)!= None:
      self.SI.updChar(userID,name, description)
      return
    self.SI.addChar(userID,name, description)
    self.__AddToOutput('You have added a character named'+ name + '.'+ description)
    return

  def delChar(self, message, parameters):
    """
    Deletes a character from the database if it exists attached to the user
    """
    name = parameters[0] #Maybe the source of a bug if delete is only looking for the first letter of the name
    userID = self.__getCLID(message)
    self.SI.delChar(userID,name)
    return

  def getChar(self, message, parameters):
    """
    ssw.getchar(message, parameters) Retrieves character information, unless it doesn't exist or there are multiple characters named || 
    IF there are multiple characters with the same name print out the characters with a number behind them in {}
    IF there is {} in the name print out the description of the character with the appropriate brackets
    """
    name = parameters[0]
    ml = self.SI.getMultiList(name)
    if self.SI.checkIfOne(name) and '{' not in name:
      self.__AddToOutput(self.SI.getCharacter(message.author.id,name))
      return
    elif '{' in name:
      characterID = -1
      self.__AddToOutput('Characters with the name' + name + ':')
      for j in ml:
        if j[0] == name:
          characterID = j[1]
        if characterID == -1:
            self.__AddToOutput('No characters with the name' + name + 'found.')
        return
      self.__AddToOutput(self.SI.getIDChar(characterID))
      return
    elif len(ml)>1:
      formatted = ''
      for i in ml:
        formatted = formatted + i[0] + '\n'
    else:
      self.__AddToOutput(self.SI.getList(parameters[0]))
    return
  def list(self, message, parameters):
    """
    ssw.list(message, parameters) Lists all characters in the database
    """
    self.__AddToOutput(self.SI.getList(parameters[0]))

  def help(self):
    """
    ssw.help() Prints out the help menu
    """
    self.__AddToOutput("--\nTo add a character use\n **!addchar <name>\n<description>**\n--\n"+
             "To delete a character use\n **!delchar <name>**\n--\n" +
            "To list a character use\n **!char <name>**\n--" +
            "\nTo list all your characters in the bot use\n **!List**\n--\ ")
  def addUser(self, message, parameters):
    """
    checks if they exist, adds them or updates their name if anything is out of date
    """
    if not self.SI.CheckIfPersonExists(message.author.id):
      self.SI.CreatePerson(message.author.id, message.author.name)
      return
    self.SI.UpdateUsername(message.author.id, message.author.name)
#TODO:
#ssw.addUser(message, parameters) checks if they exist, adds them or updates their name if anything is out of date

  #private Methods
  def __getCLID(self,message):
    """gets the linking ID"""
    return(self.SI.getID(message.author.id))

  def __AddToOutput(self,text):
    """Adds text to the output queue"""
    self.__output.append(text)