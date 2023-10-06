# import json
import copy
from textsum.summarize import Summarizer
from confluent_kafka import Producer,Consumer

class CiGi_Summarizer():
    def __init__(self, input_message):
        self.model = None
        self.output_data = None
        self.consumed_data = None
        self.input_message = input_message

    def digest_input(self):
        self.consumed_data = self.input_message
        ## CHECK IF LOADED INPUT HAS JSON/DICT FORMAT
        if type(self.consumed_data) is not dict:
            # print(self.consumed_data)
            return "not_dict"

        ## CHECK IF ANY JSON FIELDS ARE MISSING
        correct_keys = ["metadata_id","text","part","chapter","summary_length","word_count","language","algorithm"]
        existing_keys = list(self.consumed_data.keys())
        missing_keys = list(set(correct_keys) - set(existing_keys))
        if missing_keys:
            return missing_keys

        ## CHECK IF ANY JSON FIELDS ARE EMPTY
        empty_keys = []
        for key,value in self.consumed_data.items():
            if value==None or value=="":
                empty_keys.append(key)
        if empty_keys:
            return empty_keys

        ## CHECK IF INPUTS ARE OF CORRECT TYPE
        correct_data_types = {
            "metadata_id": str,
            "text": str,
            "part": int,
            "chapter": str,
            "summary_length": int,
            "word_count": int,
            "language": str,
            "algorithm": str
        }
        wrong_data_types = {}
        for key,value in self.consumed_data.items():
            data_type = correct_data_types[key]
            if not isinstance(value, data_type):
                wrong_data_types[key] = str(type(value))
                # wrong_data_types[key] = type(value)
        if wrong_data_types:
            return wrong_data_types

        return True

    def initialize_summarizer(self):
        #pszemraj/long-t5-tglobal-base-16384-booksum-V12
        #pszemraj/long-t5-tglobal-base-16384-booksci-summary-v1
        #long-t5-tglobal-base-16384-booksci-summary-v1
        self.model = Summarizer(model_name_or_path="./models/long-t5-tglobal-base-16384-booksci-summary-v1",token_batch_length=4096,use_cuda=True, min_length=self.consumed_data["summary_length"]-50, max_length=self.consumed_data["summary_length"]+50, repetition_penalty=3.0,num_beams=4)  # loads default model and parameters
        return str(self.model.model.device)

    def summarize(self):
        try:
            summary = self.model.summarize_string(self.consumed_data["text"])
        except Exception as e:
            return e
        self.output_data = copy.deepcopy(self.consumed_data)
        self.output_data["text"] = summary
        return summary

    def output_data(self):
        return self.output_data


