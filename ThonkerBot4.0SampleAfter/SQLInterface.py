import json

import pyodbc as po


class SQL_Connection:
    "Interfaces with SSMS"

    def __init__(self) -> None:
        with open("SQLInfo.Json", "r") as JsonHold:
            __JS = json.load(JsonHold)

        self.__connectionString = po.connect(
            DRIVER=__JS["driver"],
            SERVER=__JS["server"],
            DATABASE=__JS["database"],
            UID=__JS["username"],
            PWD=__JS["password"],
        )
        self.__connectionString.setdecoding(po.SQL_CHAR, encoding="latin1")

    def getCharacter(self, user_id: int, character_name: str) -> po.Row:
        """Retrieves a character's page

        Parameters
        ----------
        user_id : int
            User's Discord ID
        character_name : str
            Character's name

        Returns
        -------
        po.Row
            Character's page
        """
        cursor = self.__getCursor()
        cursor.execute(
            "execute getCharacter @ownerid = ?, @charactername = ?",
            user_id,
            character_name,
        )
        return cursor.fetchone()[0]

    def deleteCharacter(self, user_id: int, character_name: str):
        """Used To Delete Characters

        Parameters
        ----------
        user_id : int
            User's Discord ID
        character_name : str
            Character's name
        """
        cursor = self.__getCursor()
        cursor.execute(
            "execute deleteCharacter @ownerid =?, @charactername =?",
            user_id,
            character_name,
        )

    def updateCharacter(self, user_id: int, character_name: str, description: str):
        """Used to update a character

        Parameters
        ----------
        user_id : int
            User's Discord ID
        character_name : str
            Character's name
        description : str
            Character's description
        """
        cursor = self.__getCursor()
        cursor.execute(
            """
            execute
                updateCharacter @ownerid =?, @charactername =?, @description =?
            """,
            user_id,
            character_name,
            description,
        )

    def createCharacter(self, user_id: int, character_name: str, description: str):
        """Used to create a character

        Parameters
        ----------
        user_id : int
            User's Discord ID
        character_name : str
            Character's name
        description : str
            Character's description
        """
        cursor = self.__getCursor()
        cursor.execute(
            """
            execute
                addCharacter @ownerid =?, @charactername =?, @description =?
            """,
            user_id,
            character_name,
            description,
        )

    def checkIfOne(self, character_name: str) -> bool:
        """Used to check if it's the only character in the database

        Parameters
        ----------
        character_name : str
            Character's name

        Returns
        -------
        bool
            True if it's the only character
        """
        cursor = self.__getCursor()
        cursor.execute(
            "select count(*) from character where charactername = ?",
            character_name,
        )
        return cursor.fetchone()[0] == 1

    def getMultiList(self, charaName: str) -> list[po.Row]:
        """Used To Deal with multiple characters with the same name,
        returns i[listname{number}][characterid]

        Parameters
        ----------
        charaName : str
            The name of the character

        Returns
        -------
        list[po.Row]
            The list of characters
        """
        cursor = self.__getCursor()
        cursor.execute("execute getMultiList @name =?", charaName)
        return cursor.fetchall()

    def getIDChar(self, charaID: int) -> str:
        """Used To Deal with multiple characters with the same ID,
        returns character Information matching the id

        Parameters
        ----------
        charaID : int
            The ID of the character

        Returns
        -------
        str
            description
        """
        cursor = self.__getCursor()
        cursor.execute(
            "select description from character where id = ?",
            charaID,
        )
        return cursor.fetchone()[0]

    def getList(self, wildCard: str) -> str:
        """Gets Similar Names

        Parameters
        ----------
        wildCard : str
            The name to search for

        Returns
        -------
        str
            The list of names
        """
        cursor = self.__getCursor()
        cursor.execute("Execute getSimilarList @wc=?", wildCard)
        names = [row[0] for row in cursor.fetchall()]
        return "\n".join(names) if len(names) <= 50 else "Be more specific"

    def __getCursor(self):
        """Returns a cursor to the SQL Server"""
        return self.__connectionString.cursor()
