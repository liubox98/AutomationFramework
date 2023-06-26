import subprocess
from multiprocessing import Process
from tools.TestApi import start_wda, start_test
from script.payment import enter_customs_purchase_five_step_payment

DEVICE_LIST = ['a5e139b146e0e2d737b0f721d0452393982b44e7']


def execution_use_case():
    # 进关购买五步支付脚本
    enter_customs_purchase_five_step_payment()


def main():
    wda_devices_dict = {}
    queue = []
    port = 8300
    use_port = port
    for uuid in DEVICE_LIST:
        process = start_wda(uuid, port)
        wda_devices_dict[uuid] = {"process": process, "port": port}
        print(f'uuid:{uuid}\tport:{port}')
        t = Process(target=start_test, args=(uuid, port,))
        queue.append(t)
        port += 100
    try:
        for i in queue:
            i.start()
        for i in queue:
            i.join()
    finally:
        for process in range(len(queue)):
            try:
                command = "netstat -ano | findstr :{}".format(use_port)
                output = subprocess.check_output(
                    command, shell=True).decode("utf-8").strip()
                if output:
                    process_id = output.split()[-1]
                    subprocess.run(
                        f"taskkill /F /PID {process_id}", shell=True, check=True)
            except subprocess.CalledProcessError:
                print(f"无法终止端口 {use_port} 的进程。")
            use_port += 100


if __name__ == '__main__':
    main()
