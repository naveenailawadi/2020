import pandas as pd
import json
import time


class ConfigManager:
    def __init__(self, filepath):
        self.filepath = filepath

        # load the file
        self.information = json.loads(filepath)

    def update_key(self, config_key, value):
        self.information[config_key] = value

        # export the file
        self.export_file(self.information)

    def export_file(self, dictionary):
        dumpable = json.dumps(dictionary)

        with open(self.filepath, 'w') as outfile:
            outfile.write(dumpable)


class RecordManager:
    def __init__(self, sent_file, friends_file):
        self.sent_file = sent_file
        self.friends_file = friends_file

        # load the dataframes
        self.old_df = pd.read_csv(self.sent_file, header=0)
        self.header_row = self.old_df.columns

        self.friends_df = pd.read_csv(self.friends_file, header=0)

    def get_removables(self, start_time_utc, stop_time_utc):
        # get removables from the old df
        removables_df = self.old_df[self.old_df['sent_time'] > start_time_utc][self.old_df['sent_time'] < stop_time_utc]
        removables = set(removables_df['gamertag'])

        # get removables from the friends df
        friends_df = pd.read_csv(self.friends_file, header=0)
        friends = set(friends_df['gamertag'])
        removables = removables | friends

        return removables

    # create a function to add new records to he old dataframe
    def add_records(self, to_send, message):
        send_time = time.time()
        data = [[recipient, message, send_time] for recipient in to_send]
        appendable_df = pd.DataFrame(data, columns=self.header_row)
        output_df = self.old_df.append(appendable_df, ignore_index=True)
        output_df.to_csv(self.sent_file, index=False)
