#!/usr/bin/env python3

from client_query_manager import custom_style_3
from pprint import pprint
from PyInquirer import prompt

class Helper_class:
    def getKey_from_dict(self, in_dict, value):
        for key, val in in_dict:
            if val == value:
                return key
        return None
    
    def getAnswersFromQuestionSet(self, question_set):
        response = prompt( question_set, style = custom_style_3 )
        name = question_set['name']
        return response[ name ]

    def getAsnwerFromPrompt(self, Type, name, message, choices, Filter = None):
        question = [
            {
                'type' : Type,
                'name' : name,
                'message' : message,
                'choices' : choices,
                'filter' : Filter
            }
        ]

        response = prompt( question, style = custom_style_3 )

        return response[ name ]