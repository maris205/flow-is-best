#!/usr/bin/env python3
#coding=utf-8
#########################################################################
# Author: @maris
# Created Time: May 18  2017 18:55:41 PM CST
# File Name:spider.py
# Description:create flow account
# SPDX-License-Identifier: MIT
#########################################################################
import sys
import re
import json
import time
import io
import os
from subprocess import Popen, PIPE


config = "flow.json"
#param
PARAM = " -f {} --signer emulator-account ".format(config)

def test():
    com = "flow status -f {}".format(config)
    val = Popen(com, stdout=PIPE, shell=True)
    val.wait()
    print(str(val.stdout.read()))

"""
功能：get secret key
输入：
返回：private_key,public_key
"""
def get_key():
    com = "flow keys generate -o json"
    val = os.popen(com)
    item = val.read()
    data = json.loads(item)

    private_key = data["private"]
    public_key = data["public"]
    return private_key, public_key

"""
功能：生成账号
输入：public_key
返回：address, 钱包地址
"""
def create_account(public_key):
    com = "flow accounts create --key {} {}  -o json".format(public_key, PARAM)
    val = os.popen(com)
    item = val.read()
    data = json.loads(item)
    address = data["address"]
    return address


"""
功能：发flow token
输入：address， to 的地址
输入：amount，数量
返回：transaction_id, 交易id
"""
def send_flow(address, amount=1.0):
    com = 'flow transactions send transfer_flow_tokens.cdc {} "{}" {} -o json'.format(amount, address, PARAM)

    val = os.popen(com)
    item = val.read()
    data = json.loads(item)
    transaction_id = data["id"]
    return transaction_id


#初始新用户
def ini_new_user_account():
    #step 1 ,生成key
    private_key, public_key = get_key()

    #step 2,创建flow账号
    address = create_account(public_key)

    #step 3, 发送10个token
    # transaction_id = send_flow(address)

    # #step 4, 增加到用户配置文件
    # user_name = "user_" + address
    # com = 'flow config add account --name "{}" --address "{}" --private-key "{}"'.format(
    #     user_name, address, private_key
    # )
    # val = os.popen(com)
    # sys.stdout.flush()
    # time.sleep(5)
    return private_key, public_key, address, ""

if __name__=="__main__":
    for i in range(0, 1000):
        private_key, public_key, address, transaction_id = ini_new_user_account()
        #print(private_key, public_key, address, transaction_id)
        print(address, private_key, public_key)



