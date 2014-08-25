# -*- coding: utf-8 -*-

# subject.py
# Visual Cognitive Neuroscience Lab
# Brock University
#
# Created by Thomas Nelson on 2013-10-24
#
# This library was developed for use by the Visual Cognitive
# Neuroscience Lab at Brock University.

class Subject:
    """This class consists of all collective information regarding test
    subjects for the experiment.
    
    """
    
    def __init__(self, expName="", subjNum=999, subjAge=0, subjSex='', subjHand=''):
        """This is the default constructor function for the Subject class and is
        used to initialize the subject information.
        
        :param expName: The name of the experiment.
        :type expName: string
        :param subjNum: The subject number. Default is '999' for testing.
        :type subjNum: integer
        :param subjAge: The subject age. Default is '0'.
        :type subjAge: integer
        :param subjSex: The subject gender. Default is empty.
        :type subjSex: character
        :param subjHand: The subject handedness. Default is empty.
        :type subjHand: character
        :param notes: Any extra notes regarding the subject. Default is empty.
        :type notes: string
        
        """
        
        self.expName  = expName
        self.subjNum  = subjNum
        self.subjAge  = subjAge
        self.subjSex  = subjSex
        self.subjHand = subjHand
        self.notes    = notes
        self.fileName = expName + '_' + subjNum + '.csv'
    # end def __init__
    
    def getSubject(self):
        """This public function is used to get the subject number.
        
        :returns: The subject number.
        
        """
        
        return self.subjNum
    # end def getSubject
    
    def getFileName(self):
        """This public function is used to get the subject file name.
        
        :returns: The subject file name.
        
        """
        
        return self.fileName
    # end def getFileName
    
    def getsubjAge(self):
        """This public function is used to get the subject age.
        
        :returns: The subject age.
        
        """
        
        return self.subjAge
    # end def getsubjAge
    
    def getsubjSex(self):
        """This public function is used to get the subject gender.
        
        :returns: The subject gender.
        
        """
        
        return self.subjSex
    # end def getsubjSex
    
    def getsubjHand(self):
        """This public function is used to get the subject handedness.
        
        :returns: The subject handedness.
        
        """
        
        return self.subjHand
    # end def getsubjHand
    
    def getsubjNotes(self):
        """This public function is used to get the subject notes.
        
        :returns: The subject notes.
        
        """
        
        return self.notes
    # end def getsubjNotes
    
# end class Subject