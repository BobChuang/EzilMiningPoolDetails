import requests
import os
import time
import prettytable as pt

PATH = os.getcwd() + "\\Data\\"


def make_file(name, config_dict, type_conf, path=PATH):
    with open(path + name + "." + type_conf, "a+") as file:
        for keys, values in zip(config_dict.keys(), config_dict.values()):
            file.write(f"{keys}={values}\n")

def as_num(x):
    y='{:.18f}'.format(x)
    return(y)

class API:
    def __init__(self, eth_address, zil_address, check_time, coin="eth"):
        self.check_time = check_time
        self.coin = coin
        self.bot_running = True
        self.worker_data = {}
        self.session = requests
        self.url_balance = f"https://billing.ezil.me/balances/{eth_address}.{zil_address}"
        self.url_hashrate = f"https://stats.ezil.me/current_stats/{eth_address}.{zil_address}/reported"
        self.url_workers = f"https://stats.ezil.me/current_stats/{eth_address}.{zil_address}/workers"  
        self.personal_stats = f"https://calculator.ezil.me/api/ezil_calculator?hashrate=431922591&scale=1"  
        self.rates = f"https://billing.ezil.me/rates"
        self.eth_reward = f"https://billing.ezil.me/rewards/{eth_address}.{zil_address}?per_page=20&coin=eth&page="
        self.zil_reward = f"https://billing.ezil.me/rewards/{eth_address}.{zil_address}?per_page=10&coin=zil&page="
        if not os.path.isdir(PATH):
            os.mkdir(PATH)

    def get_data(self):
        time_dict = {"1": int(time.time())}
        while self.bot_running:
            data_workers = {}

            try:
                balance_data = self.session.get(self.url_balance).json()
                # print(balance_data)
                hashrate_data = self.session.get(self.url_hashrate).json()
                # print(hashrate_data)
                worker_data = self.session.get(self.url_workers).json()
                # print(worker_data)
                rates_data = self.session.get(self.rates).json()
                # print(rates_data)
                personal_data = self.session.get(self.personal_stats).json()
                # print(personal_data)

                current_time = str(int(time.time()))
                time_dict["2"] = int(current_time)
                # delta_time = time_dict["2"] - time_dict["1"]
                # print(f"Getting Data; Time Difference: {delta_time}; Time Stamp: {current_time}")

                #-----------------Today, Yestoday ETH Reward--------------------
                eth_page = 0
                today_eth_reward_list = []
                yestoday_eth_reward_list = []
                is_break = 0
                while True:
                    eth_page += 1
                    eth_reward_data = self.session.get(f"{self.eth_reward}{eth_page}").json()
                    # print(eth_reward_data)
                    for eth_reward in eth_reward_data:
                        time_stap = time.strftime("%Y-%m-%d", time.localtime(int(time.mktime(time.strptime(eth_reward['created_at'], "%Y-%m-%dT%H:%M:%SZ"))) + 60*60*8))
                        if time_stap == time.strftime("%Y-%m-%d", time.localtime()):
                            today_eth_reward_list.append(as_num(eth_reward['amount']))
                        if time_stap == time.strftime("%Y-%m-%d", time.localtime(int(time.time()) - 60*60*24)):
                            yestoday_eth_reward_list.append(as_num(eth_reward['amount']))
                        if time_stap == time.strftime("%Y-%m-%d", time.localtime(int(time.time()) - 60*60*24*2)):
                            is_break = 1
                            break
                    if is_break == 1:
                        break
                    print(f'ETH Page {eth_page} finish')
                # print(today_eth_reward_list)
                # print(yestoday_eth_reward_list)
                today_eth_rewards = 0
                for today_eth_reward in today_eth_reward_list:
                    today_eth_rewards += float(today_eth_reward)
                # print(today_eth_rewards)
                yestoday_eth_rewards = 0
                for yestoday_eth_reward in yestoday_eth_reward_list:
                    yestoday_eth_rewards += float(yestoday_eth_reward)
                # print(yestoday_eth_rewards)
                #-----------------Today, Yestoday ZIL Reward--------------------
                zil_page = 0
                today_zil_reward_list = []
                yestoday_zil_reward_list = []
                is_break = 0
                while True:
                    zil_page += 1
                    zil_reward_data = self.session.get(f"{self.zil_reward}{zil_page}").json()
                    # print(zil_reward_data)
                    for zil_reward in zil_reward_data:
                        time_stap = time.strftime("%Y-%m-%d", time.localtime(int(time.mktime(time.strptime(zil_reward['created_at'], "%Y-%m-%dT%H:%M:%SZ"))) + 60*60*8))
                        if time_stap == time.strftime("%Y-%m-%d", time.localtime()):
                            today_zil_reward_list.append(as_num(zil_reward['amount']))
                        if time_stap == time.strftime("%Y-%m-%d", time.localtime(int(time.time()) - 60*60*24)):
                            yestoday_zil_reward_list.append(as_num(zil_reward['amount']))
                        if time_stap == time.strftime("%Y-%m-%d", time.localtime(int(time.time()) - 60*60*24*2)):
                            is_break = 1
                            break
                    if is_break == 1:
                        break
                    print(f'ZIL Page {zil_page} finish')
                # print(today_zil_reward_list)
                # print(yestoday_zil_reward_list)
                today_zil_rewards = 0
                for today_zil_reward in today_zil_reward_list:
                    today_zil_rewards += float(today_zil_reward)
                # print(today_zil_rewards)
                yestoday_zil_rewards = 0
                for yestoday_zil_reward in yestoday_zil_reward_list:
                    yestoday_zil_rewards += float(yestoday_zil_reward)
                # print(yestoday_zil_rewards)
                #-----------------------Log--------------------------
                data_workers['time_stamp'] = current_time
                data_workers['eth'] = balance_data['eth']  # eth balance
                data_workers['zil'] = balance_data['zil']
                data_workers['pool_current_hashrate'] = round(float(hashrate_data['eth']['current_hashrate']/1000000), 3)  # 30 min average hashrate
                data_workers['pool_average_hashrate'] = round(float(hashrate_data['eth']['average_hashrate']/1000000), 3)   # 3 hour average hashrate
                data_workers['pool_reported_hashrate'] = round(float(hashrate_data['reported_hashrate']/1000000), 3)   # reported hashrate
                data_workers['eth_price'] = float(rates_data['ETH']['USD'])
                data_workers['zil_price'] = float(rates_data['ZIL']['USD'])
                data_workers['day_eth_coin'] = float(personal_data['eth']['only_eth'])
                data_workers['week_eth_coin'] = data_workers['day_eth_coin']*7
                data_workers['month_eth_coin'] = data_workers['day_eth_coin']*30
                data_workers['day_zil_coin'] = float(personal_data['eth']['zil'])
                data_workers['week_zil_coin'] = data_workers['day_zil_coin']*7
                data_workers['month_zil_coin'] = data_workers['day_zil_coin']*30
                data_workers['day_eth_reward'] = data_workers['eth_price'] * float(personal_data['eth']['only_eth'])
                data_workers['week_eth_reward'] = data_workers['day_eth_reward'] * 7
                data_workers['month_eth_reward'] = data_workers['day_eth_reward'] * 30
                data_workers['day_zil_reward'] = float(rates_data['ZIL']['USD']) * data_workers['day_zil_coin']
                data_workers['week_zil_reward'] = data_workers['day_zil_reward'] * 7
                data_workers['month_zil_reward'] = data_workers['day_zil_reward'] * 30
                data_workers['least_eth_reward'] = 0.05
                data_workers['least_zil_reward'] = 30
                data_workers['need_eth_reward_time'] = '%.1f' % ((data_workers['least_eth_reward'] - balance_data['eth'])/data_workers['day_eth_coin'])
                data_workers['need_zil_reward_time'] = '%.1f' % ((data_workers['least_zil_reward'] - balance_data['zil'])/data_workers['day_zil_coin'])
                data_workers['today_eth_reward_coin'] = today_eth_rewards
                data_workers['yestoday_eth_reward_coin'] = yestoday_eth_rewards
                data_workers['today_eth_reward_money'] = today_eth_rewards * data_workers['eth_price']
                data_workers['yestoday_eth_reward_money'] = yestoday_eth_rewards * data_workers['eth_price']
                data_workers['today_zil_reward_coin'] = today_zil_rewards
                data_workers['yestoday_zil_reward_coin'] = yestoday_zil_rewards
                data_workers['today_zil_reward_money'] = today_zil_rewards * data_workers['zil_price']
                data_workers['yestoday_zil_reward_money'] = yestoday_zil_rewards * data_workers['zil_price']

                
                for worker in worker_data:
                    worker_name = worker["worker"]
                    data_workers[f"current_hashrate_{worker_name}"] = worker["current_hashrate"]
                    data_workers[f"average_hashrate_{worker_name}"] = worker["average_hashrate"]
                    data_workers[f"reported_hashrate_{worker_name}"] = worker["reported_hashrate"]
                
                #-----------------------Output File--------------------------
                make_file("Worker_Data", {"Data": data_workers}, "Data")
                #-----------------------Output Log--------------------------
                print('---------------------')
                print(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()))
                hash = pt.PrettyTable()
                hash.field_names = [" ", "HASHRATE"]
                hash.add_row(["current", f"{data_workers['pool_current_hashrate']} MH/s"])
                hash.add_row(["average", f"{data_workers['pool_average_hashrate']} MH/s"])
                hash.add_row(["reported", f"{data_workers['pool_reported_hashrate']} MH/s"])
                print(hash)
                coin = pt.PrettyTable()
                coin.field_names = ["Estimated Coin Mining", "Daily Mining", "Weekly Mining", "Monthly Mining"]
                coin.add_row(["ETH", '%.4f' % data_workers['day_eth_coin'], '%.4f' % data_workers['week_eth_coin'], '%.4f' % data_workers['month_eth_coin']])
                coin.add_row(["ZIL", '%.4f' % data_workers['day_zil_coin'], '%.4f' % data_workers['week_zil_coin'], '%.4f' % data_workers['month_zil_coin']])
                print(coin)
                estimate_reward = pt.PrettyTable()
                estimate_reward.field_names = ["Estimated Money", "Daily Money", "Weekly Money", "Monthly Money"]
                estimate_reward.add_row(["ETH", f"${'%.2f' % data_workers['day_eth_reward']}", f"${'%.2f' % data_workers['week_eth_reward']}", f"${'%.2f' % data_workers['month_eth_reward']}"])
                estimate_reward.add_row(["ZIL", f"${'%.2f' % data_workers['day_zil_reward']}", f"${'%.2f' % data_workers['week_zil_reward']}", f"${'%.2f' % data_workers['month_zil_reward']}"])
                estimate_reward.add_row(["TOTAL", f"${'%.2f' % (data_workers['day_eth_reward'] + data_workers['day_zil_reward'])}", f"${'%.2f' % (data_workers['week_eth_reward'] + data_workers['week_zil_reward'])}", f"${'%.2f' % (data_workers['month_eth_reward'] + data_workers['month_zil_reward'])}"])
                print(estimate_reward)
                reward = pt.PrettyTable()
                reward.field_names = [f"{time.strftime('%m-%d', time.localtime())}Real Income", "Yestoday Coin Mining", "Yestoday Income", "Today Coin Mining", "Today Income"]
                reward.add_row(["ETH", data_workers['yestoday_eth_reward_coin'], f"${'%.2f' % data_workers['yestoday_eth_reward_money']}", data_workers['today_eth_reward_coin'], f"${'%.2f' % data_workers['today_eth_reward_money']}"])
                reward.add_row(["ZIL", data_workers['yestoday_zil_reward_coin'], f"${'%.2f' % data_workers['yestoday_zil_reward_money']}", data_workers['today_zil_reward_coin'], f"${'%.2f' % data_workers['today_zil_reward_money']}"])
                reward.add_row(["TOTAL", "", f"${'%.2f' % (data_workers['yestoday_zil_reward_money'] + data_workers['yestoday_eth_reward_money'])}", " ", f"${'%.2f' % (data_workers['today_zil_reward_money'] + data_workers['today_eth_reward_money'])}"])
                print(reward)
                own = pt.PrettyTable()
                own.field_names = ["BALANCE", "Coin", "Coin Price", "Total Revenue", "Min Payout", "Remaining Time"]
                own.add_row(["ETH", balance_data['eth'], f"${data_workers['eth_price']}", f"${'%.2f' % (balance_data['eth']*data_workers['eth_price'])}", data_workers['least_eth_reward'], f"{data_workers['need_eth_reward_time']}Day"])
                own.add_row(["ZIL", balance_data['zil'], f"${data_workers['zil_price']}", f"${'%.2f' % (balance_data['zil']*data_workers['zil_price'])}", data_workers['least_zil_reward'], f"{data_workers['need_zil_reward_time']}Day"])
                print(own)
                time_dict["1"] = time_dict["2"]
            except Exception:
                print("No Workers Found")

            # print(f"Sleeping {self.check_time} Seconds")
            time.sleep(self.check_time)


if __name__ == "__main__":
    a = API("0x426a77C7F2d74331e328B53281234fB6803D18F7", "zil1d5x96nvdl6fy2l3yk92uppj3tle6us73apvluc", 60)
    a.get_data()

