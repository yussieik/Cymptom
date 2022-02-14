#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 10:39:11 2022

@author: Yossi Eikelman
"""
from dataextractor import ConnectDB
from instance import Instance
from utils import get_logger
import pprint


logger = get_logger('MAIN')

if __name__ == "__main__":
    logger.info("Program started")
    answer = ''
    while answer != 'Q':
        try:
            access_key = input("Access key: ")
            secret_key = input("Secret access key: ")
            logger.info(
                f"Trying connect to database with access key: {'*' * len(access_key)}\nsecret key: {'*' * len(secret_key)}")
            db = ConnectDB(access_key, secret_key)
            db.upload_db()
            df_out = db.get_df
            instances = {}
            for k, v in df_out.items():
                inst = Instance(k, v)
                instances[k] = inst

            while answer != 'Q':

                kws = "".join(
                    [f"\n{inst}" for inst in list(enumerate(instances))])
                try:
                    answer = input(
                        f"Available instances:{kws}\nChoose...or press Q ").upper()
                    instances_keys = list(instances)
                    if answer.isnumeric():
                        if int(answer) <= len(instances):
                            choice_instance = instances[instances_keys[int(
                                answer)]]
                            while answer != 'Q':
                                choice = input(
                                    f" [0] ids\n [1] os_platform\n [2] NetworkStats\n [3] Status\n [4] Description\n [5] Launch_time\n [6] Tags\n [7] Specs\n [8] Security Groups\n [9] Tokens\n OR 'Q' for main menu\n Choice:  ")
                                if choice.isnumeric():
                                    choice = int(choice)
                                    if 0 <= choice <= 9:

                                        if choice == 0:
                                            pprint.pprint(choice_instance.ids)
                                        if choice == 1:
                                            pprint.pprint(
                                                choice_instance.os_platform)
                                        if choice == 2:
                                            pprint.pprint(
                                                choice_instance.network_sets)
                                        if choice == 3:
                                            pprint.pprint(
                                                choice_instance.status)
                                        if choice == 4:
                                            pprint.pprint(
                                                choice_instance.description)

                                        if choice == 5:
                                            pprint.pprint(
                                                choice_instance.launch_time)
                                        if choice == 6:
                                            pprint.pprint(choice_instance.tags)
                                        if choice == 7:
                                            pprint.pprint(
                                                choice_instance.specs)
                                        if choice == 8:
                                            pprint.pprint(
                                                choice_instance.security_groups)
                                        if choice == 9:
                                            pprint.pprint(
                                                choice_instance.tokens)

                                        continue

                                elif choice.upper() == 'Q':
                                    break

                                else:
                                    print("Wrong choice, try again")
                                    continue
                except Exception:
                    continue
        except Exception:
            continue

print("FINISHED")
logger.info("Program terminated by user")
