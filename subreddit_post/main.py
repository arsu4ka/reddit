from models.redditClass import RedditProfile
from multiprocessing import Process
from funcs import *


def main():
    config_dict = dict(read_json(input("Config.json path >>> ")))
    keys = tuple(config_dict.keys())
    config_copy = config_dict.copy()
    for key in keys:
        config_dict[key] = read_json(config_dict[key])
    
    profiles = []    
    for profile in config_dict["profiles"]:
        profiles.append(RedditProfile(
            id=profile["client_id"],
            secret=profile["client_secret"],
            username=profile["username"],
            password=profile["password"]
        ))
    
    for weekday in keys[1::]:
        for community in config_dict[weekday]["community"]:
            try:
                if community["flair_id"] == None:
                    community["flair_id"] = choose_flair(random.choice(profiles), community["name"], weekday)
            except:
                continue
            
        write_json(config_copy[weekday], config_dict[weekday])
    
    while True:
        weekday = get_weekday()
        data_list = config_dict[weekday["string"]]
        print(f"\nHi! Today is {weekday['string']} working on reddit!")
        
        procs = []
        for community in data_list["community"]:
            proc = Process(
                target=post, 
                args=(random.choice(profiles), community, data_list)
            )
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()
        
        print(f"\nEverything is done for {weekday['string']}, waiting for tomorrow!")
        while get_weekday()["integer"] == weekday["integer"]:
            time.sleep(30)
    

if __name__ == "__main__":
    main()